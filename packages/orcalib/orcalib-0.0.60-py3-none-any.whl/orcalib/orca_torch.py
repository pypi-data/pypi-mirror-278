import itertools
import logging
import time
from collections import defaultdict, deque
from typing import Any, Callable, Iterable, Iterator, Optional, TypeVar, cast, final
from uuid import UUID

import torch
import torch.nn as nn
import torch.nn.functional as F
from orca_common import ColumnName
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
from typing_extensions import deprecated

from orcalib.batched_scan_result import BatchedScanResult
from orcalib.client import OrcaClient
from orcalib.constants import EXACT_MATCH_THRESHOLD
from orcalib.database import OrcaDatabase
from orcalib.orca_expr import ColumnHandle
from orcalib.orca_torch_mixins import (
    ClassificationMode,
    CurateSettingsMixin,
    DropExactMatchOption,
    FeedbackKind,
    LabelColumnNameMixin,
    LookupSettingsMixin,
    OrcaMetadataDict,
    PostInitMixin,
    PreForwardMixin,
    ProjectionMode,
)
from orcalib.table import TableHandle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


########################
### Orca PyTorch Layers
########################

MODULE_TYPE = TypeVar("MODULE_TYPE", bound="OrcaModule")


class OrcaModule(nn.Module, CurateSettingsMixin):
    """OrcaModule is for PyTorch modules that support Curate tracking. It is the base class for all Orca PyTorch layers.

    NOTE: Curate setting propagation is handled by the OrcaModel (model, not module) class, which recursively sets the
    curate settings for all children of the model to use the same instance of the curate settings object.
    """

    def __init__(
        self,
        curate_database: OrcaDatabase | str | None = None,
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        metadata: Optional[OrcaMetadataDict] = None,
        curate_enabled: bool = False,
        tags: Optional[Iterable[str]] = None,
    ):
        """Initializes the module with the specified Curate settings.
        :param curate_database: The OrcaDatabase instance to use for Curate tracking. (default: None)
        :param model_id: The ID of the model. (default: None)
        :param model_version: The version of the model. (default: None)
        :param metadata: The metadata to be stored with Curate runs. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param tags: The tags to be included in Curate runs. (default: None)
        """
        nn.Module.__init__(self)
        CurateSettingsMixin.__init__(
            self,
            curate_database=curate_database,
            model_id=model_id,
            model_version=model_version,
            metadata=metadata,
            curate_enabled=curate_enabled,
            tags=tags,
        )

    def __hash__(self):
        return id(self)

    def get_orca_modules_recursively(
        self,
        max_depth: Optional[int] = None,
        include_self: bool = True,
        filter_type: type[MODULE_TYPE] | None = None,
    ) -> Iterator[MODULE_TYPE]:
        """
        Get all OrcaModule in the model recursively. NOTE: This will search through all children - even
        those that aren't OrcaModule - but it will only return OrcaModule. This allows for a more general
        search of the model.

        :param max_depth: The maximum depth to search. Setting this to 0 will only include this module, setting it
         to 1 will include only this module and its children (default: None). Passing through modules that don't
         match the filter_type will not increment the depth.
        :param skip_self: Whether to include the current OrcaModule in the results. (default: True)
        :param filter_type: The type of module to filter by. (default: OrcaModule)
        :return: An iterator of OrcaModule.
        NOTE: All parent nodes will be processed before their children
        """
        unvisited = deque([self])
        node_depth = dict({self: 0})

        filter_type = filter_type or OrcaModule

        while unvisited:
            parent = unvisited.popleft()
            if isinstance(parent, filter_type) and (include_self or parent != self):
                yield parent

            # We only want to increment the depth if there is no parent or it's an instance of the filter type
            if parent is None or isinstance(parent, filter_type):
                next_depth = node_depth[parent] + 1
            else:
                next_depth = node_depth[parent]

            if max_depth is not None and next_depth > max_depth:
                continue
            for child in parent.children():
                node_depth[child] = next_depth
                unvisited.append(child)  # type: ignore

    def enable_curate(self, recursive: bool = True):
        """
        Enable Curate tracking for the model and (if recursive is True) for all its descendants.
        :param recursive: Whether to enable Curate tracking recursively. (default: True)
        """
        if not recursive:
            self.curate_enabled = True
            return
        for child in self.get_orca_modules_recursively():
            child.curate_enabled = True

    def disable_curate(self, recursive: bool = True):
        """
        Disable Curate tracking for this module and (if recursive is True) for all its descendants.
        :param recursive: Whether to disable Curate tracking recursively. (default: True)
        """
        if not recursive:
            self.curate_enabled = False
            return
        for child in self.get_orca_modules_recursively():
            child.curate_enabled = False

    def update_curate_settings(
        self,
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
        extra_tags: Optional[Iterable[str]] = None,
        metadata: Optional[OrcaMetadataDict] = None,
        extra_metadata: Optional[OrcaMetadataDict] = None,
        batch_size: Optional[int] = None,
        seq_id: Optional[UUID] = None,
        enabled: Optional[bool] = None,
        enable_recursive: bool = True,
    ) -> None:
        """
        Update curate tracking settings for the module and all its children.

        :param model_id: The ID of the model.
        :param model_version: The version of the model.
        :param new_tags: The new tags to be added to the model.
        :param extra_tags: The extra tags to be added to the model.
        :param new_metadata: The new metadata to be added to the model.
        :param extra_metadata: The extra metadata to be added to the model.
        :param batch_size: The batch size to be used for the model.
        :param seq_id: The sequence ID to be used for the model.
        """

        self.curate_model_id = model_id or self.curate_model_id
        self.curate_model_version = model_version or self.curate_model_version
        self.curate_tags = tags if tags is not None else self.curate_tags
        if extra_tags:
            self.curate_tags |= set(extra_tags)
        self.curate_metadata = metadata if metadata is not None else self.curate_metadata
        if extra_metadata:
            self.curate_metadata.update(extra_metadata)
        self.curate_batch_size = batch_size or self.curate_batch_size
        self.curate_seq_id = seq_id or self.curate_seq_id
        if enabled is not None:
            self.curate_enabled = enabled
            if enable_recursive:
                for child in self.get_orca_modules_recursively(include_self=False):
                    child.curate_enabled = enabled

    def _infer_batch_size(*args: Any, **kwargs: Any) -> int:
        """
        Attempts to infer the batch size from the model's input arguments.
        :param args: The positional arguments.
        :param kwargs: The keyword arguments.
        :return: The inferred batch size.
        """
        for arg in itertools.chain(args, kwargs.values()):
            if isinstance(arg, torch.Tensor) and len(arg.shape) > 1:
                return arg.shape[0]
        raise ValueError("Curate batch size could not be inferred. Please set it manually.")

    def _is_curate_enabled_anywhere(self) -> bool:
        """
        Checks if curate tracking is enabled anywhere in the model or its children.
        :return: Whether curate tracking is enabled anywhere in the model or its children.
        """
        return any(child.curate_enabled for child in self.get_orca_modules_recursively())

    def record_next_model_memory_lookups(self, *args, batch_size: Optional[int] = None, **kwargs) -> list[int]:
        """
        Sets up curate tracking for the memory lookups in the next forward pass.
        :param batch_size: The batch size of the next forward pass. (default: None)
        :param args: The positional arguments to the forward pass for inferring the batch size.
        :param kwargs: The keyword arguments to the forward pass for inferring the batch size.
        """
        if self.curate_model_id is None:
            raise AttributeError("A model id must be set before recording memory lookups")
        if self.curate_database is None:
            raise AttributeError("A database must be set before recording memory lookups")

        self.last_curate_run_ids = OrcaClient.init_forward_pass(
            db_name=self.curate_database,
            model_id=self.curate_model_id,
            model_version=self.curate_model_version,
            batch_size=batch_size or self.curate_batch_size or self._infer_batch_size(*args, **kwargs),
            tags=self.curate_tags,
            metadata=self.curate_metadata,
            seq_id=self.curate_seq_id,
        )
        return self.last_curate_run_ids

    @deprecated("use record_model_feedback instead")
    def record_curate_scores(self, scores: list[float] | float) -> None:
        self.record_model_feedback(scores)

    def record_model_feedback(
        self,
        feedback: list[float] | float | int | list[int],
        name: str = "default",
        kind: FeedbackKind = FeedbackKind.CONTINUOUS,
    ) -> None:
        """
        Records feedback for the last model runs for which memory lookups were recorded by curate.
        :param feedback: The feedback to be recorded.
        :param name: The name of the feedback. (default: "default")
        :param kind: The kind of feedback. (default: FeedbackKind.CONTINUOUS)
        """
        if self.last_curate_run_ids is None:
            raise AttributeError("Feedback can only be recorded if the last model run was tracked by curate")
        # Ensure feedback is a list of the right length
        if isinstance(feedback, (float, int)):
            feedback = [feedback]
        if len(feedback) != len(self.last_curate_run_ids):
            raise ValueError(
                f"Feedback length ({len(feedback)}) did not match last recorded run batch size ({len(self.last_curate_run_ids)})"
            )
        # Ensure feedback is a list of correct floats based on the passed kind
        float_feedback: list[float] = []
        for f in feedback:
            float_value = float(f)
            match kind:
                case FeedbackKind.UNARY:
                    if float_value != 1.0:
                        raise ValueError(f"Unary feedback must be 1.0, got {float_value}")
                case FeedbackKind.BINARY:
                    if isinstance(f, bool):
                        float_value = +1.0 if f else -1.0
                    if float_value not in (-1.0, +1.0):
                        raise ValueError(f"Binary feedback must be -1 or +1, got {float_value}")
                case FeedbackKind.CONTINUOUS:
                    if float_value > 1.0 or float_value < -1.0:
                        raise ValueError(f"Continuous feedback must be between -1 and +1, got {float_value}")
                case _:
                    raise ValueError(f"Unsupported feedback kind: {kind}")
            float_feedback.append(float_value)
        # TODO: update api to allow recording several types of feedback with different names
        self.get_curate_database_instance().record_model_scores(self.last_curate_run_ids, float_feedback)

    def record_model_input_output(self, inputs: list[Any] | Any, outputs: list[Any] | Any) -> None:
        """
        Records the inputs and outputs of the last model runs for which memory lookups were recorded by curate.
        :param inputs: The inputs to be recorded.
        :param outputs: The outputs to be recorded.
        """
        if self.last_curate_run_ids is None:
            raise AttributeError("Input and outputs can only be recorded if the last model run was tracked by curate")
        if not isinstance(inputs, list):
            inputs = [inputs]
        if not isinstance(outputs, list):
            outputs = [outputs]
        if not (len(inputs) == len(outputs) == len(self.last_curate_run_ids)):
            raise ValueError(
                f"Inputs length ({len(inputs)}) or output length ({len(outputs)}) did not match last recorded run batch size ({len(self.last_curate_run_ids)})"
            )
        self.get_curate_database_instance().record_model_input_output(self.last_curate_run_ids, inputs, outputs)


class OrcaLookupModule(OrcaModule, LookupSettingsMixin, PostInitMixin):
    """
    OrcaLookupModule is for PyTorch modules that support both Curate tracking AND memory lookups, and is the
    base class for all Orca PyTorch layers that support lookups—either directly or through their children.

    NOTE: Lookup settings are propagated to all children of OrcaLookupModule, which recursively sets the lookup
    settings for all OrcaLookupModule its descendents to use the same instance of the lookup settings object.
    """

    def __init__(
        self,
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        metadata: Optional[OrcaMetadataDict] = None,
        curate_enabled: bool = False,
        tags: Optional[Iterable[str]] = None,
        # Memory Lookup Settings
        memory_index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = None,
        freeze_num_memories: bool = False,
        propagate_lookup_settings: bool = True,
    ):
        """Initializes the module with the specified Curate and memory lookup settings.
        :param database: The OrcaDatabase instance to use for Curate and memory lookups. (default: None)
        :param model_id: The ID of the model. (default: None)
        :param model_version: The version of the model. (default: None)
        :param metadata: The metadata to be stored with Curate runs. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param tags: The tags to be included in Curate runs. (default: None)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param lookup_column_names: The names of the columns to return from the index during a lookup. (default: None)
        :param num_memories: The number of memories to return from the index during a lookup. (default: None)
        :param freeze_num_memories: Whether the number of memories should be frozen. (default: False) When
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        set to True, an error will be raised if an attempt is made to change the number of memories.
        :param propagate_lookup_settings: Whether to propagate lookup settings to all children. (default: False)
        """
        OrcaModule.__init__(
            self,
            model_id=model_id,
            model_version=model_version,
            metadata=metadata,
            curate_enabled=curate_enabled,
            tags=tags,
            curate_database=database,
        )
        LookupSettingsMixin.__init__(
            self,
            lookup_database=database,
            memory_index_name=memory_index_name,
            lookup_column_names=lookup_column_names,
            num_memories=num_memories,
            freeze_num_memories=freeze_num_memories,
            propagate_lookup_settings=propagate_lookup_settings,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
        )

    def post_init(self):
        super().post_init()

        self._propagate_lookup_settings()


class OrcaModel(OrcaLookupModule, PostInitMixin, PreForwardMixin):
    """OrcaModel should be the base class for all PyTorch models that include custom Orca layers.

    This class is responsible for:
      * Propagating Curate and memory lookup settings to all children of the model.
      * Getting curate run ids and preparing tracking before the forward pass.
      * Building layer names for all children of the model.

    This class provides functions to let you:
      * Enable and disable Curate tracking for the model and all its children.
      * Record Curate scores for the last run.
      * Record model input and output for the last run.
      * Enable and disable memory access for the model and all its children.
      * Update Curate tracking settings for the model and all its children.

    When using OrcaModel, you can set global settings for Curate tracking and memory lookups that will be propagated
    to all children of the model. This allows you to set these settings once for the entire model and have them
    automatically applied to all layers.
    """

    def __init__(
        self,
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        model_id: Optional[str] = None,
        model_version: Optional[str] = None,
        metadata: Optional[OrcaMetadataDict] = None,
        curate_enabled: bool = False,
        tags: Optional[Iterable[str]] = None,
        # Memory Lookup Settings
        memory_index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        freeze_num_memories: bool = False,
        propagate_lookup_settings: bool = True,
    ):
        """
        Initializes the model with global settings.
        :param database: The OrcaDatabase instance to use for Curate and memory lookups. (default: None)
        :param model_id: model_id will be included in Curate runs. (default: None)
        :param model_version: model_version will be included in Curate runs. (default: None)
        :param metadata: metadata is a dictionary of additional information to be stored with Curate runs. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param tags: tags is a set of strings to be included in Curate runs. (default: None)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param lookup_column_names: The names of the columns to return from the index during a lookup. (default: None)
        :param num_memories: The number of memories to return from the index during a lookup. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param freeze_num_memories: Whether the number of memories should be frozen after initialization. (default: False) When
        set to True, an error will be raised if an attempt is made to change the number of memories.
        :param propagate_lookup_settings: Whether to propagate lookup settings to all children. (default: False)
        """
        super().__init__(
            database=database,
            model_id=model_id,
            model_version=model_version,
            metadata=metadata,
            curate_enabled=curate_enabled,
            tags=tags,
            memory_index_name=memory_index_name,
            lookup_column_names=lookup_column_names,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=freeze_num_memories,
            propagate_lookup_settings=propagate_lookup_settings,
        )

    def pre_forward(self, *args, **kwargs):
        """Called before the forward pass, this is where we setup curate tracking."""
        if self._is_curate_enabled_anywhere() and not self.training:
            self.record_next_model_memory_lookups(*args, **kwargs)

    def post_init(self) -> None:
        """
        Function that runs after the __init__ method. This is used to apply global settings to the model and build
        the curate layer names. You can override this function to add new post-init behavior in derived classes.

        This will override the curate settings for all children to use the parent's settings.
        NOTE: This means that changing the child's settings will change the parent's settings and vice versa.
        """
        super().post_init()
        OrcaModel._build_layer_names(self)

        for child in self.get_orca_modules_recursively(include_self=False):
            child._orca_curate_settings = self._orca_curate_settings
            child.curate_enabled = self.curate_enabled

    @deprecated("use update_curate_settings instead")
    def init_curate(self, *args, **kwargs) -> None:
        """use update_curate_settings instead"""
        self.update_curate_settings(*args, **kwargs)

    @staticmethod
    def _build_layer_names(inst: nn.Module, root_name: Optional[str] = None) -> None:
        """
        Builds layer names for the model and all its children.
        :param inst: A PyTorch model instance.
        :param root_name: The name of the root layer. (default: None)
        """
        if isinstance(inst, OrcaModule) and getattr(inst, "curate_layer_name", None) is None:
            inst.curate_layer_name = root_name
        for name, child in inst.named_children():
            OrcaModel._build_layer_names(
                child,
                f"{root_name + '.' if root_name is not None else ''}{name}",
            )

    def enable_memory(self) -> None:
        """
        Enables memory access for the model and all its children.
        """
        for child in self.get_orca_modules_recursively():
            if hasattr(child, "_memory_enabled"):
                child._memory_enabled = True

    def disable_memory(self) -> None:
        """
        Disables memory access for the model and all its children.
        """
        for child in self.get_orca_modules_recursively():
            if hasattr(child, "_memory_enabled"):
                child._memory_enabled = False


@final
class _LinearClassificationHead(OrcaModule):
    """A 2-Layer linear classification head generally used for a transformer model.
    Example usage:

    .. code-block:: python

        import torch
        from orcalib import OrcaModule, _LinearClassificationHead

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(10, 10)
                self.classifier = _LinearClassificationHead(10, 5)

            def forward(self, x):
                x = self.linear(x)
                x = self.classifier(x)
                return x

        model = MyModel()
    """

    def __init__(
        self,
        model_dim: int,
        num_labels: int,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
    ):
        """
        :param model_dim: The dimension of the input tensor.
        :param num_labels: The number of labels.
        :param activation: The activation function. (default: F.relu)
        :param dropout: The dropout rate. (default: 0.1)
        """
        super().__init__()

        self.model_dim = model_dim
        self.num_labels = num_labels
        self.activation = activation
        self.dropout = dropout

        self.linear1 = nn.Linear(model_dim, model_dim)
        self.dropout_layer = nn.Dropout(self.dropout)
        self.linear2 = nn.Linear(model_dim, num_labels)

    def forward(self, x) -> torch.Tensor:
        """
        Performs a forward pass through the linear classification head.

        :param x: The input tensor.
        :return: The output tensor.
        """
        x = self.linear1(x)
        x = self.activation(x)
        x = self.dropout_layer(x)
        x = self.linear2(x)
        return x


class OrcaLookupLayer(OrcaLookupModule):
    """A layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    This requires a database to be attached to the model, with the index already created.

    Example usage:

    .. code-block:: python

        import torch
        from orcalib import OrcaModule, OrcaLookupLayer

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(10, 10)
                self.lookup = OrcaLookupLayer("my_index", ["my_label, my_extra_columns"], 10)

            def forward(self, x):
                x = self.linear(x)
                x, meta = self.lookup(x)
                return x, meta

        model = MyModel()

    """

    _cache: dict[tuple, Any] = {}

    def __init__(
        self,
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Memory Lookup Settings
        memory_index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        freeze_num_memories: bool = False,
        cache_ttl: Optional[int] = None,
        layer_name: Optional[str] = None,
    ):
        """
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param lookup_column_names: The names of the columns to return from the index during a lookup. (default: None)
        :param num_memories: The number of memories to return from the index during a lookup. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param freeze_num_memories: Whether the number of memories should be frozen. (default: False)
        :param cache_ttl: The time-to-live for the lookup cache. (default: None)
        """

        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=lookup_column_names,
            num_memories=num_memories,
            freeze_num_memories=freeze_num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            propagate_lookup_settings=False,
        )
        self.curate_layer_name = layer_name
        self.cache_ttl = cache_ttl
        self.use_lookup_cache = self.cache_ttl is not None
        if self.use_lookup_cache and self.curate_enabled:
            # TODO: rethink how to best allow using lookup cache in train mode where curate is disabled
            raise ValueError("Curate tracking cannot be enabled when using the lookup cache")

    def _get_index_info_with_overrides(
        self,
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
    ) -> tuple[OrcaDatabase, str, list[str], int]:
        """
        Returns the index-lookup info, with overrides applied where provided

        :param orca_db_instance: The OrcaDatabase instance to use. (default: None)
        :param index_name: The name of the index to use. (default: None)
        :param lookup_column_names: The names of the columns to return from the index. (default: None)
        :param num_memories: The number of memories to return from the index. (default: None)
        :return: A tuple of (OrcaDatabase, index_name, lookup_column_names, num_memories)

        NOTE: This method should not be called directly. It is used internally.
        """
        orca_db_instance = orca_db_instance or self.get_lookup_database_instance()
        index_name = index_name or self.memory_index_name
        if index_name is None:
            raise ValueError("Index name must be set before lookup or passed to forward()")
        lookup_column_names = lookup_column_names or self.lookup_column_names
        if lookup_column_names is None:
            raise ValueError("Lookup column names must be set before lookup or passed to forward()")
        num_memories = num_memories or self.num_memories
        if num_memories is None or num_memories <= 0:
            raise ValueError("num_memories must be set > 0 before lookup or passed to forward()")
        return orca_db_instance, index_name, lookup_column_names, num_memories

    def _db_lookup(
        self,
        x: torch.Tensor | str | list[str],
        orca_db_instance: OrcaDatabase,
        index_name: str,
        lookup_column_names: list[str],
        num_memories: int,
    ) -> BatchedScanResult:
        """
        Performs the lookup in the OrcaDatabase index.

        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: The OrcaDatabase instance to use.
        :param index_name: The name of the index to use.
        :param lookup_column_names: The names of the columns to return from the index.
        :param num_memories: The number of memories to return from the index.
        :return: The result of the lookup.

        NOTE: This method should not be called directly. It is used internally.
        """
        cache_key = None
        if self.use_lookup_cache:
            cache_key = (
                x,
                orca_db_instance.name,
                index_name,
                lookup_column_names,
                num_memories,
            )
            mem = OrcaLookupLayer._cache.get(cache_key, None)
            if mem is not None:
                result, timestamp = mem
                if timestamp + self.cache_ttl > time.time():
                    return result

        if isinstance(x, str):
            query = [x]
            query_len = 1
        elif isinstance(x, list):
            query = x
            query_len = len(x)
        elif isinstance(x, torch.Tensor):
            query = x.detach().cpu().to(torch.float32).numpy().tolist()
            query_len = x.shape[0]
        else:
            raise ValueError(f"Unsupported input type: {type(x)}")

        do_dropout = (
            self.drop_exact_match == DropExactMatchOption.ALWAYS
            or (self.drop_exact_match == DropExactMatchOption.TRAINING_ONLY and self.training)
            or (self.drop_exact_match == DropExactMatchOption.INFERENCE_ONLY and not self.training)
        )

        if do_dropout:
            req = orca_db_instance.vector_scan_index(
                index_name,
                query,
                drop_exact_match=True,
                exact_match_threshold=self.exact_match_threshold,
            )
        else:
            req = orca_db_instance.vector_scan_index(index_name, query)

        # track this particular lookup using Curate
        if self.last_curate_run_ids:
            if query_len != len(self.last_curate_run_ids):
                raise ValueError(
                    f"The inferred or manually set curate batch size ({len(self.last_curate_run_ids)}) did not match the actual query length ({query_len})."
                )
            assert self.curate_layer_name is not None  # we fill in the layer name in post_init
            req = req.track_with_curate(self.last_curate_run_ids, self.curate_layer_name)

        # execute the lookup (fetch), where meta is a list of additional columns to be returned
        # aside from the index vector matches
        res = req.select(*lookup_column_names).fetch(num_memories)  # type: ignore

        if self.use_lookup_cache:
            OrcaLookupLayer._cache[cache_key] = (res, time.time())  # type: ignore

        if self.shuffle_memories:
            res.shuffle()

        return res

    def forward(
        self,
        x: torch.Tensor | str | list[str],
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        lookup_column_names: Optional[list[str]] = None,
        num_memories: Optional[int] = None,
    ) -> BatchedScanResult:
        """Performs a forward pass

        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: Optional override for the OrcaDatabase instance to use. (default: None)
        :param index_name: Optional override for the name of the index to use. (default: None)
        :param lookup_column_names: Optional override for the names of the columns to return from the index. (default: None)
        :param num_memories: Optional override for the number of memories to return from the index. (default: None)
        :return: A tuple of (memories, extra) where memories is a tensor of shape (batch_size, num_memories, vector_dim) and
            extra is a list of lists of metadata values of shape (batch_size, num_memories, num_meta_columns)
        """
        if num_memories is not None and num_memories <= 0:
            raise ValueError(f"num_memories must be > 0, but is {num_memories}")

        orca_db_instance, index_name, lookup_column_names, num_memories = self._get_index_info_with_overrides(
            orca_db_instance, index_name, lookup_column_names, num_memories
        )

        lookup_column_names = cast(list[str], lookup_column_names)

        res = self._db_lookup(x, orca_db_instance, index_name, lookup_column_names, num_memories)
        # res "shape" is (batch_size, num_memories, num_meta_columns)
        # res[i][j] is a VectorScanResult object, which includes a vector and extra metadata

        assert isinstance(res, BatchedScanResult)
        return res


class OrcaLabelLookupLayer(OrcaLookupLayer, LabelColumnNameMixin):
    """A layer that looks up the embedding and label in an OrcaDatabase index and returns the top k results.

    A layer that looks up a vector in an OrcaDatabase index and returns a tuple of two tensors that contain
    the embedding and label for the top k results.

    This requires a database to be attached to the model, with the index already created.

    Example usage:

    .. code-block:: python

        import torch
        from orcalib import OrcaModule, OrcaLabelLookupLayer

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.linear = torch.nn.Linear(10, 10)
                self.lookup = OrcaLabelLookupLayer(
                                    index_name="my_index",
                                    label_column_name="my_label",
                                    num_memories=10
                                )

            def forward(self, x):
                x = self.linear(x)
                embeddings,labels = self.lookup(x)
                return embeddings,labels

        model = MyModel()
    """

    def __init__(
        self,
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        label_column_name: Optional[ColumnName] = None,
        num_memories: Optional[int] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        freeze_num_memories: bool = False,
    ):
        """Initializes the OrcaLabelLookupLayer.
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param label_column_name: The name of the label column to return from the index. (default: None)
        :param num_memories: The number of memories to return from the index during a lookup. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param freeze_num_memories: Whether the number of memories should be frozen. (default: False) When
        set to True, an error will be raised if an attempt is made to change the number of memories.
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=freeze_num_memories,
            cache_ttl=None,
        )
        self.label_column_name = label_column_name

    def forward(
        self,
        x: torch.Tensor,
        orca_db_instance: Optional[OrcaDatabase] = None,
        index_name: Optional[str] = None,
        label_column_name: Optional[ColumnName] = None,
        num_memories: Optional[int] = None,
    ) -> tuple[Tensor, Tensor]:
        """
        Performs a forward pass

        :param x: The input tensor of shape (batch_size, vector_dim)
        :param orca_db_instance: Optional override for the OrcaDatabase instance to use. (default: None)
        :param index_name: Optional override for the name of the index to use. (default: None)
        :param label_column_name: Optional override for the name of the label column to return from the index. (default: None)
        :param num_memories: Optional override for the number of memories to return from the index. (default: None)
        :return: A tuple of (embeddings, labels) where embeddings is a tensor of shape (batch_size, num_memories, vector_dim) and
            labels is an int64 tensor of shape (batch_size, num_memories)
        """
        label_override = None
        if label_column_name:
            label_override = ["$embedding", label_column_name]

        label_column_name = label_column_name or self.label_column_name
        if label_column_name is None:
            raise ValueError("Label column name must be set before lookup or passed to forward()")
        result = super().forward(x, orca_db_instance, index_name, label_override, num_memories)
        embeddings = result.to_tensor("$embedding", dtype=x.dtype, device=x.device)
        # labels must be int64 because F.one_hot does not support other integer types
        labels = result.to_tensor(label_column_name, dtype=torch.int64, device=x.device).squeeze(-1)
        return embeddings, labels


class OrcaClassificationMemoryGuideLayer(OrcaLookupModule, LabelColumnNameMixin):
    """
    A PyTorch module that implements a memory-guided classification layer.

    This layer biases the output of a classification model towards a set of memories
    The bias is controlled by a weight parameter, which determines how strongly the model should be biased towards the memories.
    """

    def __init__(
        self,
        num_classes: int,
        num_memories: int,
        enable_in_training: bool = False,
        guide_weight: float = 0.1,
        # Shared settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[ColumnName] = None,
    ):
        """
        :param num_classes: The number of classes in the classification task.
        :param num_memories: The number of memories the layer should use.
        :param enable_in_training: Whether to enable the layer during training. (default: False)
        :param guide_weight: The weight of the memory guide. (default: 0.1)
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: The name of the label column to return from the index. (default: None)
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.num_classes = num_classes
        self.enable_in_training = enable_in_training
        self.guide_weight = guide_weight
        self.label_column_name = label_column_name

        # Lookup settings will be propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer(database=database)

    def forward(
        self,
        logits: torch.Tensor,
        memory_key: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        :param logits: Input tensor of shape (N, C), where N is the batch size and C is the number of classes.
        :param memory_key: Memory key tensor of shape (N, D), where K is the number of memory slots and D is the model embedding dimension.
        :param ctx: Memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. If None, the memory context is looked up based on the memory key. (default: None)
        :param labels: Memory Label tensor of shape (N,K), where N is the batch size, and K is the number of memories. If None, the labels are looked up along with the memory context. (default: None)

        :return: Output tensor of shape (N, C), where N is the batch size and C is the number of classes.
        """
        if self.training and not self.enable_in_training:
            return logits

        if ctx is None or labels is None:
            assert labels is None and ctx is None, "Both labels and ctx must be None or neither should be None"
            ctx, labels = self.lookup(memory_key)

        probs = F.softmax(logits, dim=1)
        lhat = F.one_hot(labels, num_classes=self.num_classes).to(logits.dtype)
        weights = torch.bmm(ctx, memory_key.unsqueeze(2)).squeeze(2)
        bias = weights.unsqueeze(-1) * lhat
        bias = torch.sum(bias, dim=1)
        bias = torch.nn.functional.softmax(bias, dim=1)
        logits = probs + self.guide_weight * bias

        return logits


class OrcaClassificationCrossAttentionLayer(OrcaLookupModule, LabelColumnNameMixin):
    """A transformer decoder layer block that does cross attention

    Note that this is Classification-specific, and the labels returned by the lookup layer are used as the value-weights for the cross attention.

    The block contains the typical transformer components: multi-head attention, feed forward, and layer norm.
    The block also contains a lookup layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    These results are used as the memory context for the cross attention.
    """

    def __init__(
        self,
        model_dim: int,
        num_heads: int,
        num_classes: int,
        num_memories: int,
        dropout: float = 0.1,
        activation: Callable[[Tensor], Tensor] = F.relu,
        projection_mode: ProjectionMode = ProjectionMode.LABEL,
        split_retrieval_path: bool = False,
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[ColumnName] = None,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer.
        :param num_classes: (int) The number of classes for the output classification and weights for cross attention.
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param dropout: (float) The dropout rate. (default: 0.1)
        :param activation: (Callable[[Tensor], Tensor]) The activation function. (default: F.relu)
        :param projection_mode: (ProjectionMode) The projection mode to use for the memory labels. (default: ProjectionMode.LABEL)
        :param split_retrieval_path: (bool) Whether to split the retrieval path. (default: False)
        :param database: (OrcaDatabase | str | None) The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: (bool) Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: (Optional[str]) The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: (Optional[float]) Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: (Optional[bool]) Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: (Optional[ColumnName]) The name of the label column to return from the index. (default: None)
        """

        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.model_dim = model_dim
        self.num_heads = num_heads
        self.num_classes = num_classes
        self.dropout = dropout
        self.activation = activation
        self.projection_mode = projection_mode
        self.split_retrieval_path = split_retrieval_path
        self.label_column_name = label_column_name

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer(database=database, num_memories=num_memories)

        self.cross_attention = nn.MultiheadAttention(
            self.model_dim,
            self.num_heads,
            dropout=self.dropout,
            batch_first=True,
            vdim=self.num_classes,
        )
        self.attn_norm = nn.LayerNorm(self.model_dim)

        self.linear1 = nn.Linear(self.model_dim, self.model_dim * 4)
        self.dropout1 = nn.Dropout(self.dropout)
        self.linear2 = nn.Linear(self.model_dim * 4, self.model_dim)
        self.dropout2 = nn.Dropout(self.dropout)
        self.ff_norm = nn.LayerNorm(self.model_dim)

    def forward(
        self,
        x: torch.Tensor,  # Shape (batch_size, vector_dim)
        ctx: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, vector_dim)
        labels: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, meta_column_count)
        memory_key: Optional[torch.Tensor] = None,  # Shape (batch_size, vector_dim)
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        x, ctx, labels act as Q, K, V for the cross attention layer.

        When ctx is None:

        * If split_retrieval_path is False, x is used as both Q and K.
        * If split_retrieval_path is True, memory_key is used as K (instead of x)

        When ctx is not None:

        * values

        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param labels: The memory label tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        """
        if ctx is None or labels is None:
            if self.split_retrieval_path and memory_key is None:
                raise ValueError("Split retrieval path requires either a memory key or context to be passed in")
            assert labels is None and ctx is None, "Both labels and ctx must be None or neither should be None"
            # Shape of ctx: (batch_size, num_memories, vector_dim)
            # Shape of labels: (batch_size, num_memories)
            ctx, labels = self.lookup(memory_key) if self.split_retrieval_path else self.lookup(x)

        x = x.unsqueeze(1)  # N x 1 x D

        if self.projection_mode == ProjectionMode.POSITIONAL:
            labels = torch.arange(self.num_memories).repeat(x.shape[0], 1)

        """
        K = num memories; C = num classes (for positional projection mode C == K); D = embedding dimension

        The attention layer (across all its heads) projects the one-hot encoded labels (these can be
        either class labels or positional labels depending on the projection mode) into the
        embedding space (K x C -> D). Then it compares the input embedding with the K neighbors'
        embeddings, to derive something like a similarity score for each neighbor. These similarity
        scores are then used to combine the projected labels into a single vector in the model dimension
        space, which is returned. This is akin to a weighted average, but with learned weights.

        The return value of the cross-attention layer is a representation of the positional or class
        **labels** of similar memories in the **embedding space**. These are then fed into a feedforward
        network before they are returned to the outer model. If the outer classification head uses
        `deep_residuals` (default), the output of this layer will thus be used to alter the input
        embedding based on the positional or class **labels** of similar memories.
        """
        values = F.one_hot(labels, self.num_classes).to(x.dtype).to(x.device)  # N x K x C
        x, _ = self.cross_attention(x, ctx, values)  # N x 1 x D
        x = x.squeeze(1)  # N x D
        x = self.attn_norm(x)  # N x D

        y = self.linear1(x)  # N x D*4
        y = self.activation(y)
        y = self.dropout1(y)
        y = self.linear2(y)  # N x D
        y = self.dropout2(y)
        x = self.ff_norm(y + x)  # N x D

        return x


class OrcaMemoryBindingLayer(OrcaLookupModule, LabelColumnNameMixin):
    """
    Memory binding layer that transforms positional logits (which describe the memories that the model
    predicted to be relevant) into regular logits, which describe the class the model predicts.
    """

    def __init__(
        self,
        num_memories: int,
        num_classes: int,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[ColumnName] = None,
    ):
        """
        :param num_memories: The number of memory vectors to be returned from the lookup.
        :param num_classes: The number of classes for the output classification and weights for cross attention.
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: The name of the label column to return from the index. (default: None)
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.num_classes = num_classes
        self.label_column_name = label_column_name

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer(
            database=database,
            num_memories=num_memories,
            freeze_num_memories=True,
        )

    def forward(
        self,
        logits: torch.Tensor,
        memory_key: Optional[torch.Tensor] = None,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        :param logits: Input tensor with positional logits of shape (N, K), where N is the batch size and K is the number of memories.
        :param memory_key: Memory key tensor of shape (N, D), where K is the number of memory slots and D is the model embedding dimension. (default: None)
        :param ctx: Memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. If None, the memory context is looked up based on the memory key. (default: None)
        :param labels: Memory Label tensor of shape (N, K), where N is the batch size, and K is the number of memories. If None, the labels are looked up along with the memory context. (default: None)
        :return: Output tensor of shape (N, C), where N is the batch size and C is the number of classes.
        """
        if ctx is None or labels is None:
            assert labels is None and ctx is None, "Both labels and ctx must be None or neither should be None"
            if memory_key is None:
                raise ValueError("Memory key must be provided if ctx and labels are not")
            _, labels = self.lookup(memory_key)

        mem_labels = F.one_hot(labels, num_classes=self.num_classes).to(logits.dtype).to(logits.device)  # N x K x C
        return torch.bmm(logits.unsqueeze(1), mem_labels).squeeze()  # N x C


class OrcaKnnClassifier(OrcaLookupModule):
    """
    A simple KNN layer that returns the average label of the K nearest memories to the input vector.

    Example usage:

    .. code-block:: python

        import torch
        from orcalib import OrcaModule, OrcaKnnClassifier

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.lookup = OrcaKnnClassifier(
                    index_name="my_index",
                    label_column_name="my_label",
                    num_memories=10,
                    num_classes=5
                )

            def forward(self, x):
                logits = self.lookup(x)
                return logits
    """

    def __init__(
        self,
        num_classes: int,
        num_memories: int,
        label_column_name: ColumnName,
        weigh_memories: bool = True,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = DropExactMatchOption.TRAINING_ONLY,
        exact_match_threshold: Optional[float] = None,
    ):
        """
        :param num_classes: The size of the output vector.
        :param num_memories: The number of memory vectors to be returned from the lookup.
        :param weigh_memories: Whether to weigh the memories by their scores. (default: True)
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups.
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param label_column_name: The name of the label column to return from the index.
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.num_classes = num_classes
        self.label_column_name = label_column_name
        self.weigh_memories = weigh_memories

        self.lookup = OrcaLookupLayer(
            lookup_column_names=["$score", label_column_name] if weigh_memories else [label_column_name],
            memory_index_name=memory_index_name,
        )

    def forward(
        self,
        x: Optional[Tensor] = None,
        labels: Optional[Tensor] = None,
        scores: Optional[Tensor] = None,
    ):
        """
        :param x: The input tensor of shape (N, D), where N is the batch size and D is the embedding dimension, can be omitted if labels and scores are provided directly.
        :param labels: The memory label tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param scores: The memory score tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :return: The output tensor of shape (N, C), where N is the batch size and C is the number of classes,
            if neither x nor scores are provided the dtype will be float32, otherwise it will be the same as the scores or input tensor.
        """
        if labels is None or scores is None:
            assert labels is None and scores is None, "Both labels and scores must be None or neither should be None"
            if x is None:
                raise ValueError("Input tensor must be provided if labels abd scores are not")
            result = self.lookup(x)
            labels = result.to_tensor(self.label_column_name, dtype=torch.int64, device=x.device).squeeze(-1)
            assert isinstance(labels, torch.Tensor)
            if self.weigh_memories:
                scores = result.to_tensor("$score", dtype=x.dtype, device=x.device).squeeze(-1)

        with torch.no_grad():
            if self.weigh_memories:
                if scores is None:
                    raise ValueError("Labels and scores must be provided when weighing memories")
                logits = torch.zeros(
                    scores.shape[0], self.num_classes, device=scores.device, dtype=scores.dtype
                )  # N x C
                logits.scatter_add_(1, labels, scores)
                logits /= logits.sum(dim=1, keepdim=True)
            else:
                one_hot_labels = (
                    F.one_hot(labels, num_classes=self.num_classes)
                    .to(x.dtype if x is not None else torch.float32)
                    .to(labels.device)
                )  # N x K x C
                logits = one_hot_labels.sum(dim=1) / torch.tensor(self.num_memories, device=labels.device)  # N x C
            return logits


class OrcaClassificationHead(
    OrcaLookupModule, LabelColumnNameMixin
):  # Input: single vector of size hidden_size, optional memory context (otherwise looked up), Output: single vector of size num_labels
    """
    A transformer decoder layer block that does cross attention with memory lookup

    Example usage:

    .. code-block:: python

        import torch
        from orcalib.orca_torch import OrcaModule, OrcaClassificationHead

        class MyModule(OrcaModule):
            def __init__(self):
                super().__init__()
                self.trunk = torch.nn.Linear(10, 10)
                self.classifier = OrcaClassificationHead(model_dim=10, num_classes=5, "my_index", "my_label", num_memories=10)

            def forward(self, x):
                x = self.trunk(x) # N x 10
                x = self.classifier(x)
                return x # N x 5, e.g., where each row may become logits for a softmax
    """

    def __init__(
        self,
        model_dim: int,
        num_classes: int,
        num_memories: int,
        num_layers: int = 1,
        num_heads: int = 8,
        classification_mode: ClassificationMode = ClassificationMode.DIRECT,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        deep_residuals: bool = True,
        split_retrieval_path: bool = False,
        memory_guide_weight: float = 0.0,
        single_lookup: bool = True,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[ColumnName] = None,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_classes: (int) The size of the output vector.
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param num_layers: (int) The number of attention blocks to be used, copies of OrcaClassificationCrossAttentionLayer. (default: 1)
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer. (default: 8)
        :param classification_mode: (ClassificationMode) The mode of classification to be used. (default: ClassificationMode.DIRECT)
        :param activation: (Callable[[Tensor], Tensor]) The activation function. (default: F.relu)
        :param dropout: (float) The dropout rate. (default: 0.1)
        :param deep_residuals: (bool) Whether to use deep residuals. (default: True)
        :param split_retrieval_path: (bool) Whether to split the retrieval path. (default: False)
        :param memory_guide_weight: (float) The weight of the memory guide. (default: 0.0)
        :param single_lookup: (bool) Whether to use a single lookup. (default: True)
        :param database: (OrcaDatabase | str | None) The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: (bool) Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: (Optional[str]) The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: (Optional[float]) Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: (Optional[bool]) Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: (Optional[ColumnName]) The name of the label column to return from the index. (default: None)
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.classification_mode = classification_mode
        self.model_dim = model_dim
        self.num_classes = num_classes
        self.activation = activation

        self.dropout = dropout
        self.deep_residuals = deep_residuals
        self.split_retrieval_path = split_retrieval_path
        self.memory_guide_weight = memory_guide_weight
        self.single_lookup = single_lookup
        self.label_column_name = label_column_name

        if classification_mode == ClassificationMode.MEMORY_BOUND:
            self.projection_mode = ProjectionMode.POSITIONAL
            # Lookup settings will be automatically propagated to the lookup layer
            self.memory_binding = OrcaMemoryBindingLayer(
                num_memories=num_memories,
                num_classes=num_classes,
            )
            if num_memories is None:
                raise ValueError("must provide num_memories for memory-bound classification mode")
            self.inner_classes = self.num_memories
        elif classification_mode == ClassificationMode.DIRECT:
            self.projection_mode = ProjectionMode.LABEL
            self.memory_binding = torch.nn.Identity()
            self.inner_classes = self.num_classes
        else:
            raise ValueError(f"Unrecognized classification mode: {self.classification_mode}")

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer()

        self.classification_mode = classification_mode

        self.memory_layers = nn.ModuleList(
            (
                # Lookup settings will be automatically propagated this layer
                OrcaClassificationCrossAttentionLayer(
                    model_dim=model_dim,
                    num_heads=num_heads,
                    num_classes=self.inner_classes,
                    num_memories=num_memories,
                    dropout=dropout,
                    activation=activation,
                    projection_mode=self.projection_mode,
                    split_retrieval_path=split_retrieval_path,
                    database=database,
                )
                for _ in range(num_layers)
            )
        )

        self.num_layers = num_layers
        self.classifier = _LinearClassificationHead(
            model_dim=model_dim, num_labels=self.inner_classes, activation=activation, dropout=dropout
        )

        self._memory_enabled = True
        # Lookup settings will be automatically propagated to the lookup layer
        self.guide = OrcaClassificationMemoryGuideLayer(
            num_classes=num_classes,
            num_memories=num_memories,
            guide_weight=memory_guide_weight,
            database=database,
        )

    def forward(
        self,
        x: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        memory_key: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param labels: The memory label tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, C), where N is the batch size and C is the number of classes.
        """
        if (ctx is None or labels is None) and self.single_lookup:
            assert labels is None and ctx is None, "Both labels and ctx must be None or neither"
            if memory_key is None:
                memory_key = x
            ctx, labels = self.lookup(memory_key)
        inpt = x
        if self._memory_enabled:
            for layer in self.memory_layers:
                y = layer(x, ctx, labels, memory_key)
                if self.deep_residuals:
                    x = y + x
                else:
                    x = y
        x = self.classifier(x)
        if self.classification_mode == ClassificationMode.MEMORY_BOUND:
            x = self.memory_binding(x, inpt, ctx, labels)
        if self.memory_guide_weight > 0.0:
            x = self.guide(x, memory_key or inpt, ctx, labels)
        return x

    def _orca_memory_toggle(self, enable: bool) -> None:
        """
        Toggles the memory guide layer on or off.

        :param enable: Whether to enable the memory guide layer.

        NOTE: This method should not be called directly. It is used internally.
        """
        self._memory_enabled = enable


class OrcaLLMMemoryGuideLayer(OrcaLookupModule, LabelColumnNameMixin):
    """
    A PyTorch module that implements a memory-guided generation layer for Language Models.

    This layer biases the output distribution of the model towards a set of memories.
    """

    def __init__(
        self,
        num_memories: int,
        alpha: float,
        beta: float,
        vocab_size: int,
        tokenizer: Callable[[str | list[str]], list[int] | list[list[int]]],
        S_min: int = 3,
        S_max: int = 10,
        enable_in_training: bool = False,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[str] = None,
    ):
        """
        :param num_memories: The number of memories.
        :param alpha: The alpha parameter for the memory guide.
        :param beta: The beta parameter for the memory guide.
        :param vocab_size: The size of the vocabulary.
        :param tokenizer: The tokenizer function.
        :param S_min: The minimum length of the suffixes to search for. (default: 3)
        :param S_max: The maximum length of the suffixes to search for. (default: 10)
        :param enable_in_training: Whether to enable the memory guide layer during training. (default: False)
        :param database: The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: The name of the label column to return from the index. (default: None)
        """

        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.alpha = alpha
        self.beta = beta
        self.vocab_size = vocab_size
        self.tokenizer = tokenizer
        self.S_min = S_min
        self.S_max = S_max
        self.enable_in_training = enable_in_training
        self.label_column_name = label_column_name

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLookupLayer()

    def _compute_lps_array(self, pattern) -> list[int]:
        """
        Compute the longest prefix that is also a suffix (lps) array used in KMP algorithm.

        :param pattern: The pattern to compute the lps array for.
        :return: The lps array.

        NOTE: This method should not be called directly. It is used internally.
        """
        lps = [0] * len(pattern)
        length = 0  # length of the previous longest prefix suffix

        # Loop calculates lps[i] for i = 1 to M-1
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                    # Note that we do not increment i here
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def _find_suffixes_in_sequence(self, S, M, S_min, S_max) -> list[tuple[int, int, str]]:
        """
        Find the starting indexes where the suffixes of S of lengths between S_min and S_max are contained in M.

        :param S: The sequence to search for suffixes in M.
        :param M: The sequence to search for suffixes of S.
        :param S_min: The minimum length of the suffixes to search for.
        :param S_max: The maximum length of the suffixes to search for.
        :return: A list of tuples containing the starting index of the suffix in M, the length of the suffix, and the next token in M after the suffix.

        NOTE: This method should not be called directly. It is used internally.
        """
        occurrences = []

        # Iterate through the range of lengths for suffixes of S
        for suffix_length in range(S_min, S_max + 1):
            # Get the suffix of S of length suffix_length
            suffix = S[-suffix_length:]

            # Preprocess the suffix to get the lps array
            lps = self._compute_lps_array(suffix)

            # Start searching for the suffix in M
            i = j = 0  # i is index for M, j is index for suffix
            while i < len(M):
                if suffix[j] == M[i]:
                    i += 1
                    j += 1

                if j == len(suffix):
                    # If we found a complete match, record the index where it starts in M
                    if i < len(M):
                        occurrences.append((i - j, len(suffix), M[i]))
                    else:
                        occurrences.append((i - j, len(suffix), None))
                    j = lps[j - 1]

                # Mismatch after j matches
                elif i < len(M) and suffix[j] != M[i]:
                    # Do not match lps[0..lps[j-1]] characters, they will match anyway
                    if j != 0:
                        j = lps[j - 1]
                    else:
                        i += 1

        return occurrences

    def _extract_occurance_ranks(self, occurrences, ref_length) -> dict[int, float]:
        """
        Extract the occurance ranks from the occurrences.

        :param occurrences: The occurrences to extract the ranks from.
        :param ref_length: The length of the reference sequence.
        :return: A dictionary of token to occurance rank.

        NOTE: This method should not be called directly. It is used internally.
        """
        scores = defaultdict(int)
        for _, length, next_token in occurrences:
            if next_token is None:
                continue
            if length > scores[next_token]:
                scores[next_token] = length / ref_length
        return dict(scores)

    def _bag_of_words_probs(self, bag_of_words: list[tuple[list[int], float]]) -> torch.Tensor:
        """
        Compute the bag of words probabilities.

        :param bag_of_words: The bag of words to compute the probabilities for.
        :return: The bag of words probabilities.

        NOTE: This method should not be called directly. It is used internally.
        """
        res = torch.zeros(self.vocab_size)
        for bag, score in bag_of_words:
            for token in bag:
                res[token] += score
        return torch.Tensor(res).softmax(dim=-1)

    def _weighted_next_tokens_from_memory(
        self, memory_key: torch.Tensor, q_tokens: list[int]
    ) -> tuple[
        dict[int, float], list[tuple[list[int], float]]
    ]:  # suffix max dict (token -> score), bag_of_words list (token list, score)
        """
        Compute the weighted next tokens from memory.

        :param memory_key: The memory key to use for memory lookup.
        :param q_tokens: The input tokens.
        :return: A tuple containing the weighted next tokens from the memory and the bag of words.

        NOTE: This method should not be called directly. It is used internally.
        """
        result = self.lookup(memory_key)
        ctx = result.to_tensor("$embedding", dtype=memory_key.dtype, device=memory_key.device)
        candidates: list[str] = result[0, :, self.label_column_name].to_list()
        semantic_scores: list[float] = (ctx.squeeze() @ memory_key.squeeze()).tolist()
        tokens_and_weights: dict[int, float] = {}
        for candidate, semantic_score in zip(candidates, semantic_scores):
            tokens = self.tokenizer(candidate)
            suffixes = self._find_suffixes_in_sequence(q_tokens[0], tokens, self.S_min, self.S_max)
            scores = self._extract_occurance_ranks(suffixes, len(tokens))
            for token, score in scores.items():
                if token not in tokens_and_weights or score > tokens_and_weights[token]:
                    tokens_and_weights[token] = score * semantic_score
        bag_of_words_tokens: list[list[int]] = cast(list[list[int]], self.tokenizer(candidates))
        return {token: score for token, score in tokens_and_weights.items()}, list(
            zip(
                bag_of_words_tokens,
                [x / len(candidates) for x in semantic_scores],
                strict=True,
            )
        )

    def forward(self, memory_key: torch.Tensor, logits: torch.Tensor, inpt_tokens: list[int]) -> torch.Tensor:
        """
        Forward pass.

        :param memory_key: The memory key to use for memory lookup.
        :param logits: The original model logits.
        :param inpt_tokens: The input tokens.
        :return: The updated logits.
        """
        if self.training and not self.enable_in_training:
            return logits

        probs = torch.softmax(logits, dim=-1)
        candidates, bag_of_words = self._weighted_next_tokens_from_memory(memory_key, inpt_tokens)

        if self.alpha > 0.0:
            for token, score in candidates.items():
                probs[0][token] += self.alpha * score

        if self.beta > 0.0:
            probs[0] += self.beta * self._bag_of_words_probs(bag_of_words).to(probs.device)
        return probs


class OrcaRankingCrossAttentionLayer(OrcaLookupModule, LabelColumnNameMixin):
    """A transformer decoder layer block that does cross attention for rankings.

    Note that this is Ranking-specific, and the rankings returned by the lookup layer are used as the value-weights for the cross attention.

    The block contains the typical transformer components: multi-head attention, feed forward, and layer norm.
    The block also contains a lookup layer that looks up a vector in an OrcaDatabase index and returns the top k results.
    These results are used as the memory context for the cross attention.
    """

    def __init__(
        self,
        model_dim: int,
        num_heads: int,
        num_memories: int,
        num_ranks: int,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        split_retrieval_path: bool = False,
        projection_mode: ProjectionMode = ProjectionMode.LABEL,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[str] = None,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer.
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param num_ranks: (int) The number of ranks to be used for the memory context.
        :param activation: (Callable[[Tensor], Tensor]) The activation function. (default: F.relu)
        :param dropout: (float) The dropout rate. (default: 0.1)
        :param split_retrieval_path: (bool) Whether to split the retrieval path. (default: False)
        :param projection_mode: (ProjectionMode) The mode of projection to be used. (default: ProjectionMode.LABEL)
        :param database: (OrcaDatabase | str | None) The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: (bool) Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: (Optional[str]) The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: (Optional[float]) Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: (Optional[bool]) Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: (Optional[ColumnName]) The name of the label column to return from the index. (default: None)

        This is used when the memory key is different from the input vector
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.model_dim = model_dim
        self.num_heads = num_heads
        self.num_ranks = num_ranks
        self.activation = activation
        self.dropout = dropout
        self.split_retrieval_path = split_retrieval_path
        self.projection_mode = projection_mode
        self.label_column_name = label_column_name

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer()

        self.cross_attention = nn.MultiheadAttention(
            self.model_dim,
            self.num_heads,
            dropout=self.dropout,
            batch_first=True,
        )
        self.attn_norm = nn.LayerNorm(self.model_dim)

        self.linear1 = nn.Linear(self.model_dim, self.model_dim * 4)
        self.dropout1 = nn.Dropout(self.dropout)
        self.linear2 = nn.Linear(self.model_dim * 4, self.model_dim)
        self.dropout2 = nn.Dropout(self.dropout)
        self.ff_norm = nn.LayerNorm(self.model_dim)

    def forward(
        self,
        x: torch.Tensor,  # Shape (batch_size, vector_dim)
        ctx: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, vector_dim)
        ranks: Optional[torch.Tensor] = None,  # Shape (batch_size, num_memories, meta_column_count)
        memory_key: Optional[torch.Tensor] = None,  # Shape (batch_size, vector_dim)
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """x, ctx, ranks act as Q, K, V for the cross attention layer.

        When ctx is None:

        * If split_retrieval_path is False, x is used as both Q and K.
        * If split_retrieval_path is True, memory_key is used as K (instead of x)

        When ctx is not None:

        * ranks

        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param ranks: The memory rank tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        """
        if ctx is None or ranks is None:
            if self.split_retrieval_path and memory_key is None:
                raise ValueError("Split retrieval path requires either a memory key or context to be passed in")
            assert ranks is None and ctx is None, "Both ctx and ranks must be None or neither"
            # Shape of ctx: (batch_size, num_memories, vector_dim)
            ctx, ranks = self.lookup(memory_key) if self.split_retrieval_path else self.lookup(x)

        x = x.unsqueeze(1)  # x goes from N x D --> N x 1 x D

        # setup the values for the cross attention based on normalizing the ranks from the memory contexts
        # higher rank means higher value
        normalized_ranks = ranks / self.num_ranks  # type: ignore

        values = normalized_ranks.unsqueeze(-1).expand(-1, -1, x.shape[-1])

        x, _ = self.cross_attention(x, ctx, values)  # N x 1 x D
        # x, _ = self.cross_attention(x, ctx, ctx)  # N x 1 x D

        x = x.squeeze(1)  # N x D
        x = self.attn_norm(x)  # N x D

        y = self.linear1(x)  # N x D*4
        y = self.activation(y)
        y = self.dropout1(y)
        y = self.linear2(y)  # N x D
        y = self.dropout2(y)
        x = self.ff_norm(y + x)  # N x D

        return x


class OrcaRankingHead(OrcaLookupModule, LabelColumnNameMixin):
    # Input: single vector of size hidden_size, optional memory context (otherwise looked up), Output: single element of size 1
    """A transformer decoder layer block that does cross attention with memory lookup for ranking problems"""

    def __init__(
        self,
        model_dim: int,
        num_memories: int,
        num_ranks: int,
        num_layers: int = 1,
        num_heads: int = 8,
        activation: Callable[[Tensor], Tensor] = F.relu,
        dropout: float = 0.1,
        split_retrieval_path: bool = False,
        projection_mode: ProjectionMode = ProjectionMode.LABEL,
        memory_guide_weight: float = 0.0,
        single_lookup: bool = True,
        deep_residuals: bool = False,
        # Shared Settings
        database: OrcaDatabase | str | None = None,
        # Curate Settings
        curate_enabled: bool = False,
        # Lookup Settings
        memory_index_name: Optional[str] = None,
        drop_exact_match: Optional[DropExactMatchOption] = None,
        exact_match_threshold: Optional[float] = None,
        shuffle_memories: Optional[bool] = False,
        label_column_name: Optional[str] = None,
    ):
        """
        :param model_dim: (int) The dimension of the input vector and hidden layers.
        :param num_memories: (int) The number of memory vectors to be returned from the lookup.
        :param num_ranks: (int) The number of ranks to be used for the memory context.
        :param num_layers: (int) The number of attention blocks to be used, copies of OrcaClassificationCrossAttentionLayer. (default: 1)
        :param num_heads: (int) The number of heads to be used in the multi-head attention layer. (default: 8)
        :param activation: (Callable[[Tensor], Tensor]) The activation function. (default: F.relu)
        :param dropout: (float) The dropout rate. (default: 0.1)
        :param split_retrieval_path: (bool) Whether to split the retrieval path. (default: False)
        :param projection_mode: (ProjectionMode) The mode of projection to be used. (default: ProjectionMode.LABEL)
        :param memory_guide_weight: (float) The weight of the memory guide. (default: 0.0)
        :param single_lookup: (bool) Whether to use a single lookup. (default: True)
        :param deep_residuals: (bool) Whether to use deep residuals. (default: False)
        :param database: (OrcaDatabase | str | None) The OrcaDatabase instance to use for lookups and curate tracking. (default: None)
        :param curate_enabled: (bool) Whether Curate tracking is enabled. (default: False)
        :param memory_index_name: (Optional[str]) The name of the index to use for lookups. (default: None)
        :param drop_exact_match: Choose to drop the exact match (if found) always, never, or only during training
        or inference. (default: NEVER)
        :param exact_match_threshold: (Optional[float]) Minimum similarity score for something to be considered the exact match (default: 0.9999)
        :param shuffle_memories: (Optional[bool]) Whether to shuffle the memories before returning them. (default: False)
        :param label_column_name: (Optional[ColumnName]) The name of the label column to return from the index. (default: None)
        """
        super().__init__(
            database=database,
            curate_enabled=curate_enabled,
            memory_index_name=memory_index_name,
            lookup_column_names=None,
            num_memories=num_memories,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
            freeze_num_memories=True,
            propagate_lookup_settings=True,
        )

        self.model_dim = model_dim
        self.num_heads = num_heads
        self.activation = activation
        self.dropout = dropout
        self.split_retrieval_path = split_retrieval_path
        self.projection_mode = projection_mode
        self.num_layers = num_layers
        self.memory_guide_weight = memory_guide_weight
        self.single_lookup = single_lookup
        self.deep_residuals = deep_residuals
        self.label_column_name = label_column_name

        self._memory_enabled = True

        # Lookup settings will be automatically propagated to the lookup layer
        self.lookup = OrcaLabelLookupLayer()

        self.memory_layers = nn.ModuleList(
            [
                # Lookup settings will be automatically propagated to this layer
                OrcaRankingCrossAttentionLayer(
                    model_dim=model_dim,
                    num_heads=num_heads,
                    num_memories=num_memories,
                    num_ranks=num_ranks,
                    activation=activation,
                    dropout=dropout,
                    split_retrieval_path=split_retrieval_path,
                    projection_mode=projection_mode,
                    database=database,
                )
                for _ in range(self.num_layers)
            ]
        )

        self.classifier = _LinearClassificationHead(
            model_dim=model_dim, num_labels=1, activation=activation, dropout=dropout
        )

    def forward(
        self,
        x: torch.Tensor,
        ctx: Optional[torch.Tensor] = None,
        ranks: Optional[torch.Tensor] = None,
        memory_key: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:  # x is the input vector N x D, ctx is the memory context N x K x D
        """
        Forward pass

        :param x: The input tensor of shape (N, D), where N is the batch size and D is the model embedding dimension.
        :param ctx: The memory context tensor of shape (N, K, D), where N is the batch size, K is the number of memories, and D is the model embedding dimension. (default: None)
        :param ranks: The memory rank tensor of shape (N, K), where N is the batch size and K is the number of memories. (default: None)
        :param memory_key: The memory key tensor of shape (N, D), where N is the batch size and D is the model embedding dimension. (default: None)
        :return: The output tensor of shape (N, 1), where N is the batch size. The output is the rank of the input vector.
        """
        if (ctx is None or ranks is None) and self.single_lookup:
            assert ranks is None and ctx is None, "Both ctx and ranks must be None or neither"
            if memory_key is None:
                memory_key = x
            ctx, ranks = self.lookup(memory_key)
        if self._memory_enabled:
            for layer in self.memory_layers:
                y = layer(x, ctx, ranks, memory_key)
                if self.deep_residuals:
                    x = y + x
                else:
                    x = y
        x = self.classifier(x)
        return x

    def _orca_memory_toggle(self, enable: bool) -> None:
        """
        Toggles the memory layer on or off.

        :param enable: (bool) Whether to enable the memory layer.

        NOTE: This method should not be called directly. It is used internally.
        """
        self._memory_enabled = enable


###################
### Training Utils
###################
class OrcaMemoryDataset(Dataset):
    """
    A PyTorch dataset that pulls the entire index on demand from an OrcaDatabase to be used locally
    for training Orca-based layers and models. This is useful for small datasets that can
    fit in memory, or for debugging purposes.

    The dataset consists of a list of tuples, where each tuple contains:

    * The item vector: a Tensor of shape (vector_dim,)
    * The item metadata: a list of arbitrary metadata values
    * The topk memory vectors: a Tensor of shape (num_memories, vector_dim)
    * The topk memory metadata: a list of lists of arbitrary metadata values

    Example usage:

    .. code-block:: python

        import torch
        from orcalib.orca_torch import OrcaMemoryDataset

        dataset = OrcaMemoryDataset(db, index="my_index",
                                        columns="my_label",
                                        memory_index="my_index",
                                        mem_columns="my_label",
                                        num_memories=10,
                                        page_size=1000)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
        for batch in dataloader:
            item_vectors, item_metadata, memory_vectors, memory_metadata, scores = batch
            # do something with the batch

    See also: integration_tests/news_classification_integration_test.py
    """

    def __init__(
        self,
        db: OrcaDatabase,
        index: str,
        columns: list[str | ColumnHandle] | str | ColumnHandle,
        memory_index: str,
        mem_columns: list[str | ColumnHandle] | str | ColumnHandle,
        num_memories: int,
        *,
        page_size: int = 1000,
        verbose: bool = False,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        shuffle_memories: bool = False,
    ):
        """
        :param db: The OrcaDatabase to fetch the index data from.
        :param index: The name of the index to fetch the data from.
        :param columns: The columns to fetch from the index. Can be a single column name, or a list of column names.
        :param memory_index: The name of the memory index to fetch the data from. (Generally the same as the index)
        :param mem_columns: The columns to fetch from the memory index. Can be a single column name, or a list of column names.
        :param num_memories: The number of memory vectors to fetch for each item vector.
        :param page_size: (Optional) The page size to use when fetching the data from the database. (default: 1000)
        :param verbose: (Optional) Whether to print verbose logging information. (default: False)
        """
        self.db = db
        self.index = index
        self.memory_index = memory_index
        self.num_memories = num_memories
        self.columns = columns
        self.mem_columns = mem_columns
        self.num_memories = num_memories
        self.verbose = verbose
        self.drop_exact_match = drop_exact_match
        self.exact_match_threshold = exact_match_threshold
        self.shuffle_memories = shuffle_memories

        print(f"Fetching index-join page 0 for index {index}")

        first_page = self.db.full_vector_memory_join(
            index_name=index,
            memory_index_name=memory_index,
            num_memories=num_memories,
            query_columns=columns,  # type: ignore
            page_size=page_size,
            page_index=0,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
        )

        print(f"Fetching vectors for memory index {memory_index}")

        self.memory_vectors = self.db._get_index_values_paginated(memory_index, page_size=page_size)

        print(f"Fetching memory data for memory index {memory_index} with columns {mem_columns}")

        mem_table: TableHandle = cast(TableHandle, db._get_index_table(memory_index))

        self.mem_data = dict(
            cast(
                list[tuple[int, dict[str, Any]]],
                mem_table.select(*self.__ensure_list(mem_columns)).fetch(include_ids=True),
            )
        )

        self.length: int = int(first_page["total_size"])  # type: ignore
        self.num_pages = first_page["num_pages"]
        self.page_size = first_page["page_size"]

        assert first_page["page_index"] == 0

        self.pages = {0: first_page}

    def __get_page_for_index(self, i: int) -> dict[str, Any]:
        """
        Get the page for the given index.

        :param i: The index to get the page for.
        :return: The page for the given index.
        """
        page_index = i // self.page_size  # type: ignore

        if page_index in self.pages:
            return self.pages[page_index]

        if self.verbose:
            print(
                f"Fetching index-join page {page_index} of {self.num_pages} for index {i} of {self.length} (query index: {self.index}, memory_index: {self.memory_index})"
            )

        page = self.db.full_vector_memory_join(
            index_name=self.index,
            memory_index_name=self.memory_index,
            num_memories=self.num_memories,
            query_columns=self.columns,  # type: ignore
            page_size=self.page_size,  # type: ignore
            page_index=page_index,
            drop_exact_match=self.drop_exact_match,
            exact_match_threshold=self.exact_match_threshold,
            shuffle_memories=self.shuffle_memories,
        )
        self.pages[page_index] = page
        return page

    def __ensure_list(self, x: Any) -> list[Any]:
        """
        Ensure that the given value is a list.

        :param x: The value to ensure is a list.
        :return: The value as a list.
        """
        if isinstance(x, list):
            return x
        return [x]

    def __get_column_name(self, column: str | ColumnHandle) -> str:
        """
        Get the column name from the given column handle.

        :param column: The column handle to get the column name from.
        :return: The column name.
        """
        if isinstance(column, ColumnHandle):
            return column.column_name
        return column

    def __get_dict_values(
        self,
        d: dict[str, Any],
        keys: list[str | ColumnHandle] | str | ColumnHandle,
    ) -> list[Any]:
        """
        Get the values from the given dictionary for the given keys.

        :param d: The dictionary to get the values from.
        :param keys: The keys to get the values for.
        :return: The values from the dictionary for the given keys.
        """
        if isinstance(keys, list):
            col_names = [self.__get_column_name(column) for column in keys]
            return [d[col_name] for col_name in col_names]
        else:
            col_name = self.__get_column_name(keys)
            return d[col_name]

    def __getitem__(self, index: int) -> tuple[Tensor, list[Any] | Any, Tensor, list[Any], Tensor]:
        """returns: item vector, item metadata, topk memory vectors, topk memory metadata
        If the item is in a "page" already in memory, it is retrieved from the page.
        Otherwise, the page is fetched from the database and stored in memory.

        :param index: The index of the item to get.
        :return: A tuple containing the item vector, item metadata, topk memory vectors, and topk memory metadata.
        """

        if index >= cast(int, self.length):
            raise IndexError(f"Index {index} out of range for dataset of size {self.length}")
        page = self.__get_page_for_index(index)
        sub_index = index % self.page_size  # type: ignore
        item = page["items"][sub_index]
        item_vector = Tensor(item["query_vector"])
        item_metadata = item["query_payload"]
        scores = Tensor(item["scores"])

        if not isinstance(self.columns, list) or (isinstance(self.columns, list) and len(self.columns) == 1):
            item_metadata = item_metadata[0]

        mem_vectors = Tensor([self.memory_vectors[mem] for mem in item["top_memories"]])

        mem_metadata = [self.__get_dict_values(self.mem_data[mem], self.mem_columns) for mem in item["top_memories"]]

        return item_vector, item_metadata, mem_vectors, mem_metadata, scores

    def __len__(self) -> int:
        """Returns the length of the dataset"""
        return self.length

    def get_dict(self, index: int) -> dict:
        """
        Returns the dictionary for the item at the given index

        :param index: The index of the item to get the dictionary for.
        :return: The dictionary for the item at the given index.
        """
        page = self.__get_page_for_index(index)
        sub_index = index % self.page_size  # type: ignore
        return page["items"][sub_index]

    def get_score(self) -> float:
        """Classification score for the dataset, which is the product of the hit rate and the correct rate.

        This is a measure of how well the memory vectors are able to classify the items in the dataset.

        :return: The classification score for the dataset.
        """
        total = 0
        contains_correct = 0
        count_correct = 0
        count_wrong = 0
        total_mems = 0
        for record in tqdm(self):  # type: ignore
            columns = record[1]
            if not isinstance(columns, list):
                label = columns
            else:
                # TODO: This is brittle, because it assumes the position of the label in the columns
                label = columns[1]
            # label = record[1][1]
            mem_labels = record[3]
            total += 1
            if label in mem_labels:
                contains_correct += 1
            for mem_label in mem_labels:  # type: ignore
                total_mems += 1
                if mem_label == label:
                    count_correct += 1
                else:
                    count_wrong += 1

        correct_rate = count_correct / total_mems
        hit_rate = contains_correct / total
        return correct_rate * hit_rate


class OrcaTextClassificationTrainer:
    """A simple trainer class for Text Classification Problems with Orca. Intended for quick prototyping, not to outperform a custom training loop."""

    def __init__(
        self,
        model,
        tokenizer,
        trainloader: DataLoader,
        testloader: DataLoader,
        use_memory: bool = True,
        memory_dropout: float = 0.0,
        device_override: str | None = None,
        param_groups: None | list[dict[str, Any]] = None,
        verbosity: int = 0,
    ):
        """
        :param model: The model to train.
        :param tokenizer: The tokenizer to use for encoding the input data.
        :param trainloader: The DataLoader for the training data.
        :param testloader: The DataLoader for the test data.
        :param use_memory: Whether to use memory for the model.
        :param memory_dropout: The dropout rate to use for the memory.
        :param device_override: (Optional) The device to use for training. If None, the device will be automatically selected based on the availability of CUDA. (default: None)
        :param param_groups: (Optional) The parameter groups to use for training. If None, the model parameters will be used. (default: None)
        :param verbosity: (Optional) The verbosity level to use for training. (default: 0)
        """
        self.model = model
        self.tokenizer = tokenizer
        self.trainloader = trainloader
        self.testloader = testloader
        self.use_memory = use_memory
        self.verbosity = verbosity
        if memory_dropout < 0.0 or memory_dropout > 1.0:
            raise ValueError("memory_dropout must be between 0.0 and 1.0")
        self.memory_dropout = memory_dropout
        if device_override is not None:
            self.device = torch.device(device_override)
            self.dtype = torch.float32
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.dtype = torch.bfloat16
        elif torch.backends.mps.is_available():  # type: ignore
            self.device = torch.device("mps")
            self.dtype = torch.float32
        else:
            self.device = torch.device("cpu")
            self.dtype = torch.float32
        self.param_groups = param_groups
        self.model = self.model.to(self.device, dtype=self.dtype)
        self.criterion = torch.nn.CrossEntropyLoss()
        if param_groups is None:
            param_groups = model.parameters()
        self.optimizer = torch.optim.Adam(param_groups, lr=0.001)  # type: ignore

    def _get_accuracy(self, logits, labels) -> float:
        """
        Computes and returns the accuracy of the model.

        :param logits: The logits from the model.
        :param labels: The labels for the data.
        :return: The accuracy of the model.

        NOTE: This method should not be called directly. It is used internally.
        """
        _, preds = torch.max(logits, 1)
        return (preds == labels).float().mean().item()

    def get_test_accuracy(self, testloader_override: DataLoader | None = None) -> float:
        """
        Computes and returns the average accuray of the model either on the main testset (from the constructor) or on the provided testloader_override.

        :param testloader_override: (Optional) The DataLoader to use for the testset. If None, the main testset will be used. (default: None)
        :return: The average accuracy of the model on the testset.
        """
        self.model.eval()
        if testloader_override is not None:
            testloader = testloader_override
        else:
            testloader = self.testloader
        with torch.no_grad():
            test_acc = 0.0
            test_steps = 0
            for _, keys_and_labels, ctxs, ctx_labels, scores in tqdm(testloader, desc="Processing Testset"):
                keys = keys_and_labels[0]
                labels = keys_and_labels[1]
                ctx_labels = torch.stack(ctx_labels).T
                encoding = self.tokenizer(
                    keys,
                    add_special_tokens=True,
                    padding="max_length",
                    return_tensors="pt",
                )
                inputs = encoding["input_ids"]
                mask = encoding["attention_mask"]
                inputs, mask, labels, ctxs, ctx_labels = (
                    inputs.to(self.device),
                    mask.to(self.device),
                    labels.to(self.device),
                    ctxs.to(self.device).to(self.dtype),
                    ctx_labels.to(self.device),
                )
                if self.use_memory:
                    outputs = self.model(inputs, mask, ctxs, ctx_labels)
                else:
                    outputs = self.model(inputs, mask)
                test_acc += self._get_accuracy(outputs, labels)
                test_steps += 1
            avg_test_acc = test_acc / test_steps
        self.model.train()
        return avg_test_acc

    def train_one_epoch(self, epoch=None, num_epochs=None) -> None:
        """
        Trains the model for one epoch.

        :param epoch: (Optional) The current epoch number. (default: None)
        :param num_epochs: (Optional) The total number of epochs. (default: None)
        """
        self.model.train()
        running_loss = 0.0
        running_acc = 0.0
        steps = 0
        for _, keys_and_labels, ctxs, ctx_labels, scores in tqdm(self.trainloader, desc="Processing Trainset"):
            keys = keys_and_labels[0]
            labels = keys_and_labels[1]
            ctx_labels = torch.stack(ctx_labels).T
            encoding = self.tokenizer(keys, add_special_tokens=True, padding="max_length", return_tensors="pt")
            inputs = encoding["input_ids"]
            mask = encoding["attention_mask"]
            if self.memory_dropout > 0.0:
                num_mems_max = 20  # TODO: factor out memory size as global a constant
                cutoff = int(num_mems_max * (1.0 - self.memory_dropout))
                filter = torch.randperm(num_mems_max)[:cutoff]
                ctxs = ctxs[:, filter, :]
                ctx_labels = ctx_labels[:, filter]
            inputs, mask, labels, ctxs, ctx_labels = (
                inputs.to(self.device),
                mask.to(self.device),
                labels.to(self.device),
                ctxs.to(self.device).to(self.dtype),
                ctx_labels.to(self.device),
            )
            self.optimizer.zero_grad()
            if self.use_memory:
                outputs = self.model(inputs, mask, ctxs, ctx_labels)
            else:
                outputs = self.model(inputs, mask)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item()
            running_acc += self._get_accuracy(outputs, labels)
            steps += 1
            if self.verbosity > 0 and steps % self.verbosity == 0:
                avg_loss = running_loss / steps
                avg_acc = running_acc / steps
                print(f"Epoch [{epoch}/{num_epochs}], Step [{steps}], Loss: {avg_loss:.4f}, Accuracy: {avg_acc:.4f}")

        avg_loss = running_loss / steps
        avg_acc = running_acc / steps
        print(
            f"Epoch [{epoch}/{num_epochs}], Loss: {avg_loss:.4f}, Accuracy: {avg_acc:.4f}, Test Accuracy: {self.get_test_accuracy():.4f}"
        )

    def train(self, num_epochs=10) -> None:
        """
        Trains the model for the given number of epochs.

        :param num_epochs: (Optional) The number of epochs to train for. (default: 10)
        """
        for epoch in range(num_epochs):
            self.train_one_epoch(epoch + 1, num_epochs)
