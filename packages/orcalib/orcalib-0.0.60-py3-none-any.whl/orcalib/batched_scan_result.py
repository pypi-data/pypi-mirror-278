import random
from itertools import islice
from typing import Any, Callable, Iterator, Optional

import numpy as np
import pandas
import torch
from orca_common import ColumnName
from orcalib.orca_types import OrcaTypeHandle


def is_single_element_slice(slice_obj: int | slice | str | None, target_length: int) -> bool:
    """Return True if the given slice object selects a single element from a sequence of the given length

    :param slice_obj: The slice object (or an index) to check
    :param target_length: The length of the sequence that's being sliced/indexed
    :return: True if the slice object selects a single element, False otherwise
    """

    if slice_obj is None:
        return target_length == 1
    elif isinstance(slice_obj, (str, int)):
        return True
    elif isinstance(slice_obj, list) and len(slice_obj) == 1:
        return True
    elif isinstance(slice_obj, slice):
        indices = slice_obj.indices(target_length)
        return abs(indices[0] - indices[1]) == 1
    else:
        return False


def try_collapse_slice(slice_obj: slice, target_length: int) -> int | slice:
    """Try to collapse the given slice object into a single index, if possible

    :param slice_obj: The slice object we're trying to collapse
    :param target_length: The length of the sequence that's being sliced/indexed
    :return: The collapsed slice object, or the original slice object if it can't be collapsed
    """
    indices = slice_obj.indices(target_length)
    if indices[0] == indices[1] - 1:
        return indices[0]
    else:
        return slice_obj


def index_to_slice(index: int) -> slice:
    """Convert an index to a slice

    :param index: The index we want the slice to select
    :return: A slice that selects the given index
    """
    if index == -1:
        return slice(index, None)
    return slice(index, index + 1)


class BatchedScanResult:
    """A batched scan result, containing batches of memory results. Each
    batch contains a list of memories. Each memory contains a list of values
    that were selected in the query.

    This class acts as a view on the underlying data, allowing you to slice it
    by batch, memory, and column. The slicing is lazy, so it doesn't copy any
    of the underlying data.
    """

    # A slice into a column. Can be a single column name, a list of column names
    # or indices, or a slice of column indices.
    ColumnSlice = slice | int | list[int] | ColumnName | list[ColumnName]

    def __init__(
        self,
        column_dict: dict[ColumnName, OrcaTypeHandle],
        data: list[list[tuple[Any, ...]]],
        batch_slice: slice | int | None = None,
        memory_slice: slice | int | None = None,
        column_slice: Optional[ColumnSlice] = None,
    ):
        """
        :param column_dict: A dictionary of column name to column type. These are the columns that were requested in the query.
        :param data: The underlying data. This is a list of batches, where each batch is a list of memories, where each memory is a tuple of values.
        :param batch_slice: Used internally to maintain a "view" of the data based on a subset of the batches. You shouldn't need to set this manually.
        :param memory_slice: Used internally to maintain a "view" of the data based on a subset of the memories. You shouldn't need to set this manually.
        :param column_slice: Used internally to maintain a "view" of the data based on a subset of the columns. You shouldn't need to set this manually.
        """
        self.data = data

        self.batch_size = len(data)
        self.memories_per_batch = len(data[0]) if self.batch_size > 0 else 0

        if batch_slice is not None:
            assert isinstance(
                batch_slice, (slice, int)
            ), f"batch_slice must be a slice or int. You passed: {batch_slice}"
        if memory_slice is not None:
            assert isinstance(
                memory_slice, (slice, int)
            ), f"memory_slice must be a slice or int. You passed: {memory_slice}"
        if column_slice is not None:
            assert isinstance(
                column_slice, (slice, int, list, ColumnName)
            ), f"column_slice must be a slice, int, list, or ColumnName. You passed: {column_slice}"

        self.batch_slice = batch_slice
        self.memory_slice = memory_slice
        self.column_slice = column_slice

        self.column_dict = column_dict
        self.column_to_index = {name: i for i, name in enumerate(self.column_dict.keys())}

    def shuffle(self):
        """Shuffles the memories within each batch. This can be helpful for training machine learning models."""
        for sublist in self.data:
            random.shuffle(sublist)

    def _clone(self, **overrides) -> "BatchedScanResult":
        """Clone this BatchedScanResult, optionally overriding some parameters"""

        overrides["column_dict"] = overrides.get("column_dict", self.column_dict)
        overrides["data"] = overrides.get("data", self.data)
        overrides["batch_slice"] = overrides.get("batch_slice", self.batch_slice)
        overrides["memory_slice"] = overrides.get("memory_slice", self.memory_slice)
        overrides["column_slice"] = overrides.get("column_slice", self.column_slice)

        return BatchedScanResult(**overrides)

    def _get_column_slice(self, batch_slice, memory_slice, column_slice) -> "BatchedScanResult":
        """Helper function that slices the data based on the given batch, memory, and column slices.

        NOTE: When batch_slice and memory_slice are ints, this function doesn't return a BatchedScanResult.

        Instead, if one column is selected, it returns a single value. If multiple columns are selected, it returns
        a list of values.
        """
        assert self.column_slice is None, f"BatchedScanResult already fully sliced: {repr(self)}"

        return self._clone(batch_slice=batch_slice, memory_slice=memory_slice, column_slice=column_slice)

    def _get_memory_slice(self, batch_slice, key: tuple | int) -> "BatchedScanResult":
        """Helper function that slices the data based on the given batch and memory slices."""
        if self.memory_slice is not None:
            return self._get_column_slice(self.batch_slice, self.memory_slice, key)

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"

        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=batch_slice, memory_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=batch_slice, memory_slice=key[0])
        elif key_length == 2:
            return self._get_column_slice(batch_slice, *key)
        else:
            raise ValueError(
                f"key must be a tuple with (memory_slice) or (memory_slice, column_slice). You passed: {key}"
            )

    def item(self) -> Any:
        """Return a single value from the result. This is only valid when the result is a single value (i.e., not a list)."""

        batch_slice, memory_slice, column_slice = self._get_slices(collapse_slices=True)

        if not is_single_element_slice(batch_slice, len(self.data)):
            raise ValueError(f"item() batch_slice must select a single batch. You passed: {batch_slice}")
        batch = self.data[batch_slice]

        if not is_single_element_slice(memory_slice, len(batch)):
            raise ValueError(f"item() memory_slice must select a single memory. You passed: {memory_slice}")
        memory = batch[memory_slice]

        if not is_single_element_slice(column_slice, len(memory)):
            raise ValueError(f"item() column_slice must select a single value. You passed: {column_slice}")
        values = self._extract_memory_values(memory, column_slice, force_list=True)

        return values[0]

    def __getitem__(self, key) -> "BatchedScanResult":
        """Slice the data based on the given batch, memory, and column slices.

        :param key: Key for indexing into the current BatchedScanResult.
        :return: A new BatchedScanResult that is a view on the underlying data.

        NOTE:

        - If we haven't sliced the data at all, then the key must be one of batch_slice, (batch_slice), (batch_slice, memory_slice), or (batch_slice, memory_slice, column_slice)

        - If batch_slice is already set, then the key must be one of memory_slice, (memory_slice), or (memory_slice, column_slice)

        - If batch_slice and memory_slice are already set, then the key must be a column_slice.

        - A batch_slice can be a single batch index or a slice of batch indices.

        - A memory_slice can be a single memory index or a slice of memory indices.

        - A column_slice can be a single column name, a list of column names or indices, or a slice of column indices.

        When batch_slice and memory_slice are ints, this function doesn't return a BatchedScanResult.
        Instead, if one column is selected, it returns a single value. If multiple columns are selected,
        it returns a list of values.

        Examples:

        .. code-block:: python

            >>> # Slice the data by batch, memory, and column
            >>> first_batch = result[0] # Get the first batch
            >>> first_batch_last_memory = first_batch[-1:] # Get the last memory of the first batch
            >>> first_batch_last_memory_vector = first_batch_last_memory["$embedding"] # Get the vector of the last memory of the first batch
            >>> first_batch[-1:, "$embedding"] # Equivalent to the above
            >>> result[0, -1:, "$embedding"] # Equivalent to the above

            >>> result[0, -1:, ["$embedding", "col1"]] # Get the vector and col1 of the last memory of the first batch
        """
        if self.batch_slice is not None:
            return self._get_memory_slice(self.batch_slice, key)

        assert (
            self.memory_slice is None
        ), "Cannot slice a BatchedScanResult with a memory_slice unless batch_slice is slready specified"
        assert (
            self.column_slice is None
        ), "Cannot slice a BatchedScanResult with a column_slice unless batch_slice, memory_slice are already specified"

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"
        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=key[0])
        elif key_length == 2:
            return self._get_memory_slice(*key)
        elif key_length == 3:
            return self._get_column_slice(*key)
        else:
            raise ValueError(
                f"key must be a tuple with (batch_slice) or (batch_slice, memory_slice) or (batch_slice, memory_slice, column_slice). You passed: {key}"
            )

    def __repr__(self) -> str:
        """Return a string representation of this BatchedScanResult"""
        if self.column_slice is not None:
            return f"BatchedScanResult[{self.batch_slice},{self.memory_slice},{self.column_slice}]"
        elif self.memory_slice is not None:
            return f"BatchedScanResult[{self.batch_slice},{self.memory_slice}]"
        elif self.batch_slice is not None:
            return f"BatchedScanResult[{self.batch_slice}]"

        return f"BatchedScanResult(batch_size={self.batch_size}, mem_count={self.memories_per_batch}, col_names={list(self.column_dict.keys())})"

    # Need a function to convert the values of a vector column to a tensor with shape (batch_size, mem_count, vector_len)
    def to_tensor(
        self,
        column: Optional[ColumnName | int] = None,
        dtype: Optional[torch.dtype] = None,
        device: Optional[torch.device] = None,
    ) -> torch.Tensor:
        """
        Convert the selected values from a vector column of the batched scan results into a PyTorch tensor. This method is useful
        for preparing the scan results for machine learning models and other tensor-based computations.

        This method assumes that the selected data can be appropriately converted into a tensor. It works best when the data is numeric
        and consistently shaped across batches and memories. Non-numeric data or inconsistent shapes may lead to errors or unexpected results.

        :param column: (Optional[ColumnName | int]): Specifies the column from which to extract the values. If None, the method uses the
                current column slice. If a column has been singularly selected by previous slicing, this parameter is optional.
        :param dtype: (Optional[torch.dtype]): The desired data type of the resulting tensor. If not provided, the default is inferred based
                on the data types of the input values.
        :param device: (Optional[torch.device]): The device on which the resulting tensor will be allocated. Use this to specify if the tensor
                should be on CPU, GPU, or another device. If not provided, the default is the current device setting in PyTorch.

        :return: torch.Tensor: A tensor representation of the selected data. The shape of the tensor is typically (batch_size, mem_count, vector_len),
                but can vary based on the current slicing of the BatchedScanResult object.

        Examples:

        .. code-block:: python

            >>> result = my_index.vector_scan(...)
            >>> # Convert the '$embedding' column into a tensor
            >>> embedding_tensor = result.to_tensor(column='$embedding')
            >>> # Convert and specify data type and device
            >>> embedding_tensor = result[0:2, :, 'features'].to_tensor(dtype=torch.float32, device=torch.device('cuda:0'))
        """
        batch_slice, memory_slice, column_slice = self._get_slices()
        column = column if column is not None else column_slice

        if isinstance(batch_slice, int):
            batch_slice = index_to_slice(batch_slice)
        if isinstance(memory_slice, int):
            memory_slice = index_to_slice(memory_slice)

        # NOTE: We don't check for "None" here because None was converted to slice(None) in _get_slices()
        assert isinstance(batch_slice, slice), f"batch_slice must be a slice. You passed: {self.batch_slice}"
        assert isinstance(memory_slice, slice), f"memory_slice must be a slice. You passed: {self.memory_slice}"

        if isinstance(column, list) and len(column) == 1:
            # If column is a list with a single element, convert it to a single element
            column = column[0]

        if isinstance(column, int):
            col_index = column
            assert col_index < len(self.column_dict)
        elif isinstance(column, ColumnName):
            col_index = self.column_to_index.get(column, None)
            assert col_index is not None, f"column {column} not found in extra columns: {list[self.column_dict.keys()]}"
        else:
            raise ValueError(f"column must be a single column name or integer. You passed: {column}")
        return torch.tensor(
            np.array([[row[col_index] for row in memories[memory_slice]] for memories in self.data[batch_slice]]),
            dtype=dtype,
            device=device,
        )

    def _extract_memory_values(self, memory, column_slice: Optional[ColumnSlice], force_list: bool = False):
        """Helper function that extracts the values of the given column slice from the given memory"""
        if column_slice is None:
            return memory[:]
        elif isinstance(column_slice, int):
            return [memory[column_slice]] if force_list else memory[column_slice]
        elif isinstance(column_slice, slice):
            return memory[column_slice]
        elif isinstance(column_slice, ColumnName):
            idx = self.column_to_index[column_slice]
            return [memory[idx]] if force_list else memory[idx]
        elif isinstance(column_slice, list):
            if all(isinstance(col, int) for col in column_slice):
                return [memory[col] for col in column_slice]
            elif all(isinstance(col, ColumnName) for col in column_slice):
                return [memory[self.column_to_index[col]] for col in column_slice]
            else:
                raise ValueError(
                    f"If column_slice is a list, all elements must be either ints or strings (but not a mix). You passed: {column_slice}"
                )
        else:
            raise ValueError(
                f"column_slice must be a slice, int, or list of ints or column names. You passed: {column_slice}"
            )

    def _get_slices(self, collapse_slices: bool = False) -> tuple[Any, Any, Any]:
        """Helper function that returns the effective batch, memory, and column slices"""
        batch_slice = self.batch_slice if self.batch_slice is not None else slice(None)
        memory_slice = self.memory_slice if self.memory_slice is not None else slice(None)
        column_slice = self.column_slice if self.column_slice is not None else slice(None)

        if collapse_slices:
            if isinstance(batch_slice, slice):
                batch_slice = try_collapse_slice(batch_slice, self.batch_size)
            if isinstance(memory_slice, slice):
                memory_slice = try_collapse_slice(memory_slice, self.memories_per_batch)

        return batch_slice, memory_slice, column_slice

    def __len__(self) -> int:
        """Based on the current slices, return the number of batches, memories, or values in a vector column."""
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(self.batch_slice, int):
            if self.memory_slice is int:
                return len(self._extract_memory_values(self.data[self.batch_slice][memory_slice], column_slice))
            else:
                return len(self.data[batch_slice][memory_slice])
        else:
            return len(self.data[batch_slice])

    def __iter__(self) -> Iterator:
        """Iterate over the batches of memories

        :return: The return type depends on the current slices:

        - When batch_slice is an int (but memory_slice and column_slice are None), this yields each memory from that batch.

        - When batch_slice and memory_slice are both ints (but column_slice is None), this yields each value from that memory.

        - Otherwise, this yields each batch with the specified subset of selected memories/columns
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(batch_slice, int):
            if isinstance(memory_slice, int):
                yield from self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
            else:
                yield from (
                    self._extract_memory_values(memory, column_slice) for memory in self.data[batch_slice][memory_slice]
                )
        else:
            yield from (
                [self._extract_memory_values(memory, column_slice) for memory in batch[memory_slice]]
                for batch in self.data[batch_slice]
            )

    def to_list(
        self,
    ) -> list[list[list[Any] | Any]]:
        """Convert the values of a vector column to a list of lists

        Example:

        .. code-block:: python

            >>> bsr[0].to_list() # returns the list of memories in the first batch
            >>> bsr[0, 0].to_list() # returns a list of the column values in the first memory of the first batch.
            >>> bsr[0, 0, "col1"].to_list() # returns the value of "col1" for the first memory of the first batch
            >>> bsr[0, 0, ["col1", "col2"]].to_list() # returns [value of col1, value of col2] for the first memory of the first batch
            >>> bsr[1:3, -2:, ["col1", "col2"]].to_list() # returns a list of lists of [value of col1, value of col2] for
            the last two memories of the second and third batches
        """
        return list(self)

    def df(
        self,
        limit: Optional[int] = None,
        explode: bool = False,
    ) -> pandas.DataFrame:
        """
        Convert the current view of your results into a pandas DataFrame, enabling easy manipulation and analysis of the data.

        This method restructures the nested data into a tabular format, while respecting the current slicing of the BatchedScanResult
        object. If the object has been sliced to select certain batches, memories, or columns, only the selected data will be included
        in the DataFrame.

        Special columns '_batch' and '_memory' are added to the DataFrame if the batch or memory, respectively, has not been singularly
        selected. These columns track the batch and memory indices of each row in the DataFrame.

        :param limit: (Optional[int]) If provided, limits the number of rows in the resulting DataFrame to the specified value.
            This can be useful for large datasets where you only need a sample of the data for quick analysis or visualization.

        :param explode: (bool) If True, any list-like columns in the DataFrame will be 'exploded' into separate rows, each containing
            one element from the list. This parameter is currently not implemented but can be used in future for handling
            nested data structures. Currently, its value does not change the behavior of the method.

        :return: A DataFrame representing the selected portions of the batched scan data. The exact shape and content
            of the DataFrame depend on the current state of the BatchedScanResult object, including any applied batch, memory,
            and column slices.

        Examples

        .. code-block:: python

            >>> result = BatchedScanResult(...)
            >>> # Convert entire data to DataFrame
            >>> df = result.df()
            >>> # Convert first 10 rows to DataFrame
            >>> df_limited = result.df(limit=10)
            >>> # Convert and 'explode' list-like columns (if implemented)
            >>> df_exploded = result.df(explode=True)
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        # First decide which columns to include in the DataFrame
        columns = list(self.column_dict.keys())
        match self.column_slice:
            case None:
                pass
            case slice() as s:  # Match any slice
                columns = columns[s]
            case int() as idx:  # Match any integer, store it in 'idx'
                columns = [columns[idx]]
            case list() as idxs if all(isinstance(i, int) for i in idxs):  # Match list of integers
                columns = [columns[i] for i in idxs]
            case str() as col_name:  # Match any string, assuming it's a column name
                columns = [col_name]
            case list() as col_names if all(
                isinstance(name, str) for name in col_names
            ):  # Match list of strings (column names)
                columns = col_names
            case _:  # Match anything else
                raise ValueError(
                    f"Invalid column_slice: {self.column_slice}. Slice must be None, int, str, list[int], or list[str]."
                )

        # Then decide whether we need the batch and memory columns
        include_batch_column = not is_single_element_slice(batch_slice, self.batch_size)
        include_memory_column = not is_single_element_slice(memory_slice, self.memories_per_batch)

        # Add the batch and memory columns if needed
        if include_memory_column:
            columns = ["_memory"] + columns
        if include_batch_column:
            columns = ["_batch"] + columns

        # Decide how to generate the rows of the DataFrame
        # Keys are (include_batch_column, include_memory_column)
        row_generator_dict: dict[tuple[bool, bool], Callable[[int, int, list]]] = {
            (False, False): lambda batch_index, memory_index, values: values,
            (False, True): lambda batch_index, memory_index, values: [memory_index, *values],
            (True, False): lambda batch_index, memory_index, values: [batch_index, *values],
            (True, True): lambda batch_index, memory_index, values: [batch_index, memory_index, *values],
        }

        # Generate the rows of the DataFrame
        row_generator = row_generator_dict[(include_batch_column, include_memory_column)]

        # Make sure that batch_slice and memory_slice are slices, so we can enumerate over them
        if isinstance(batch_slice, int):
            batch_slice = slice(batch_slice, None if batch_slice == -1 else batch_slice + 1)
        if isinstance(memory_slice, int):
            memory_slice = slice(memory_slice, None if memory_slice == -1 else memory_slice + 1)

        data_generator = (
            row_generator(batch_index, memory_index, self._extract_memory_values(memory, column_slice, force_list=True))
            for batch_index, batch in enumerate(self.data[batch_slice])
            for memory_index, memory in enumerate(batch[memory_slice])
        )

        # Limit the number of rows (if needed)
        if limit is not None:
            data_generator = islice(data_generator, limit)

        # Create the DataFrame
        return pandas.DataFrame(data_generator, columns=columns)


class BatchedVectorScanResult_V2:
    """A batched vector scan result, containing batches of memory results. Each
    memory result contains its embedding vector and any additional columns that
    were requested in the query.

    NOTE: This is compatible with `OrcaClient._vector_scan_index_v2(...)`

    TODO: Remove this class once the `OrcaClient._vector_scan_index_v2(...)` is removed

    This class acts as a view on the underlying data, allowing you to slice it
    by batch, memory, and column. The slicing is lazy, so it doesn't copy any
    of the underlying data.
    """

    # The name of the special column that contains the embedding vector
    VECTOR_KEY = "__vector__"
    _special_key_count = 1
    # TODO: Add additional special columns, e.g., "similarity to query vector"

    # A slice into a column. Can be a single column name, a list of column names
    # or indices, or a slice of column indices.
    ColumnSlice = slice | int | list[int] | ColumnName | list[ColumnName]

    def __init__(
        self,
        extra_col_names: list[ColumnName],
        data: list[list[tuple[Any, ...]]],
        batch_slice: slice | int | None = None,
        memory_slice: slice | int | None = None,
        column_slice: Optional[ColumnSlice] = None,
    ):
        """
        :param extra_col_names: The names of the extra columns that were requested in the query.
        :param data: The underlying data. This is a list of batches, where each batch is a list of memories, where each memory is a tuple of values.
        :param batch_slice: Used internally to maintain a "view" of the data based on a subset of the batches. You shouldn't need to set this manually.
        :param memory_slice: Used internally to maintain a "view" of the data based on a subset of the memories. You shouldn't need to set this manually.
        :param column_slice: Used internally to maintain a "view" of the data based on a subset of the columns. You shouldn't need to set this manually.
        """
        self.data = data

        self.batch_size = len(data)
        self.memories_per_batch = len(data[0]) if self.batch_size > 0 else 0

        if batch_slice is not None:
            assert isinstance(
                batch_slice, (slice, int)
            ), f"batch_slice must be a slice or int. You passed: {batch_slice}"
        if memory_slice is not None:
            assert isinstance(
                memory_slice, (slice, int)
            ), f"memory_slice must be a slice or int. You passed: {memory_slice}"
        if column_slice is not None:
            assert isinstance(
                column_slice, (slice, int, list, ColumnName)
            ), f"column_slice must be a slice, int, list, or ColumnName. You passed: {column_slice}"

        self.batch_slice = batch_slice
        self.memory_slice = memory_slice
        self.column_slice = column_slice

        self.extra_col_names = extra_col_names
        self.column_names = [self.VECTOR_KEY, *extra_col_names]
        self.column_to_index = {name: i for i, name in enumerate(self.column_names)}

    def _clone(self, **overrides) -> "BatchedVectorScanResult_V2":
        """Clone this BatchedVectorScanResult_V2, optionally overriding some parameters

        :param overrides: The parameters to override
        :return: A new BatchedVectorScanResult_V2

        NOTE: This method should not be called directly. It is used internally."""

        overrides["extra_col_names"] = overrides.get("extra_col_names", self.extra_col_names)
        overrides["data"] = overrides.get("data", self.data)
        overrides["batch_slice"] = overrides.get("batch_slice", self.batch_slice)
        overrides["memory_slice"] = overrides.get("memory_slice", self.memory_slice)
        overrides["column_slice"] = overrides.get("column_slice", self.column_slice)

        return BatchedVectorScanResult_V2(**overrides)

    def _get_column_slice(self, batch_slice, memory_slice, column_slice) -> "BatchedVectorScanResult_V2":
        """
        Helper function that slices the data based on the given batch, memory, and column slices.

        NOTE: When batch_slice and memory_slice are ints, this function doesn't return a BatchedVectorScanResult_V2.
        Instead, if one column is selected, it returns a single value. If multiple columns are selected, it returns
        a list of values.

        :param batch_slice: The slice of batches to select
        :param memory_slice: The slice of memories to select
        :param column_slice: The slice of columns to select
        :return: A new BatchedVectorScanResult_V2 that is a view on the underlying data.

        NOTE: This function is used internally to slice the data based on the given batch, memory, and column slices.
        """
        assert self.column_slice is None, f"BatchedVectorScanResult_V2 already fully sliced: {repr(self)}"

        if (
            isinstance(batch_slice, int)
            and isinstance(memory_slice, int)
            and isinstance(column_slice, (int, ColumnName))
        ):
            return self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
        else:
            return self._clone(batch_slice=batch_slice, memory_slice=memory_slice, column_slice=column_slice)

    def _get_memory_slice(self, batch_slice, key: tuple | int) -> "BatchedVectorScanResult_V2":
        """Helper function that slices the data based on the given batch and memory slices.

        :param batch_slice: The slice of batches to select
        :param key: The memory slice to select
        :return: A new BatchedVectorScanResult_V2 that is a view on the underlying data.

        NOTE: This function is used internally to slice the data based on the given batch and memory slices.
        """

        if self.memory_slice is not None:
            return self._get_column_slice(self.batch_slice, self.memory_slice, key)

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"

        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=batch_slice, memory_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=batch_slice, memory_slice=key[0])
        elif key_length == 2:
            return self._get_column_slice(batch_slice, *key)
        else:
            raise ValueError(
                f"key must be a tuple with (memory_slice) or (memory_slice, column_slice). You passed: {key}"
            )

    def __getitem__(self, key) -> "BatchedVectorScanResult_V2":
        """Slice the data based on the given batch, memory, and column slices.

        :param key: Key for indexing into the current BatchedVectorScanResult_V2.
        :return: A new BatchedVectorScanResult_V2 that is a view on the underlying data.

        NOTE:

        - If we haven't sliced the data at all, then the key must be one of batch_slice, (batch_slice), (batch_slice, memory_slice), or (batch_slice, memory_slice, column_slice)

        - If batch_slice is already set, then the key must be one of memory_slice, (memory_slice), or (memory_slice, column_slice)

        - If batch_slice and memory_slice are already set, then the key must be a column_slice.

        - A batch_slice can be a single batch index or a slice of batch indices.

        - A memory_slice can be a single memory index or a slice of memory indices.

        - A column_slice can be a single column name, a list of column names or indices, or a slice of column indices.


        When batch_slice and memory_slice are ints, this function doesn't return a BatchedVectorScanResult_V2.
        Instead, if one column is selected, it returns a single value. If multiple columns are selected,
        it returns a list of values.

        Examples:

        .. code-block:: python

            >>> # Slice the data by batch, memory, and column
            >>> first_batch = result[0] # Get the first batch
            >>> first_batch_last_memory = first_batch[-1:] # Get the last memory of the first batch
            >>> first_batch_last_memory_vector = first_batch_last_memory["__vector__"] # Get the vector of the last memory of the first batch
            >>> first_batch[-1:, "__vector__"] # Equivalent to the above
            >>> result[0, -1:, "__vector__"] # Equivalent to the above
            >>> result[0, -1:, ["__vector__", "col1"]] # Get the vector and col1 of the last memory of the first batch
        """
        if self.batch_slice is not None:
            return self._get_memory_slice(self.batch_slice, key)

        assert (
            self.memory_slice is None
        ), "Cannot slice a BatchedVectorScanResult_V2 with a memory_slice unless batch_slice is slready specified"
        assert (
            self.column_slice is None
        ), "Cannot slice a BatchedVectorScanResult_V2 with a column_slice unless batch_slice, memory_slice are already specified"

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"
        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=key[0])
        elif key_length == 2:
            return self._get_memory_slice(*key)
        elif key_length == 3:
            return self._get_column_slice(*key)
        else:
            raise ValueError(
                f"key must be a tuple with (batch_slice) or (batch_slice, memory_slice) or (batch_slice, memory_slice, column_slice). You passed: {key}"
            )

    def __repr__(self) -> str:
        """Return a string representation of this BatchedVectorScanResult_V2"""
        if self.column_slice is not None:
            return f"BatchedVectorScanResult_V2[{self.batch_slice},{self.memory_slice},{self.column_slice}]"
        elif self.memory_slice is not None:
            return f"BatchedVectorScanResult_V2[{self.batch_slice},{self.memory_slice}]"
        elif self.batch_slice is not None:
            return f"BatchedVectorScanResult_V2[{self.batch_slice}]"

        return f"BatchedVectorScanResult_V2(batch_size={self.batch_size}, mem_count={self.memories_per_batch}, extra_col_names={self.extra_col_names})"

    # Need a function to convert the values of a vector column to a tensor with shape (batch_size, mem_count, vector_len)
    def to_tensor(
        self,
    ) -> torch.Tensor:
        """
        Convert the values of a vector column to a tensor with shape (batch_size, mem_count, vector_len)

        NOTE: This function only works when all of the following are true:

        * The batch slice is a slice or None (i.e., not an int)
        * The memory slice is a slice or None (i.e., not an int)
        * The column_slice is None or a single column name or integer.

        NOTE: When column_slice is None, the tensor is built from the embedding vectors (i.e., the __vector__ column)

        :return: A tensor with shape (batch_size, mem_count, vector_len)
        """
        batch_slice, memory_slice, column = self._get_slices()

        # NOTE: We don't check for "None" here because None was converted to slice(None) in _get_slices()
        assert isinstance(batch_slice, slice), f"batch_slice must be a slice. You passed: {self.batch_slice}"
        assert isinstance(memory_slice, slice), f"memory_slice must be a slice. You passed: {self.memory_slice}"

        # The default column is the embedding vector
        if self.column_slice is None:
            column = self.VECTOR_KEY

        if isinstance(column, int):
            col_index = column
            assert col_index < len(self.column_names)
        elif isinstance(column, ColumnName):
            col_index = self.column_to_index.get(column, None)
            assert col_index is not None, f"column {column} not found in extra columns: {self.extra_col_names}"
        else:
            raise ValueError(f"column must be a single column name or integer. You passed: {column}")
        return torch.tensor(
            np.array([[row[col_index] for row in memories[memory_slice]] for memories in self.data[batch_slice]])
        )

    def _extract_memory_values(self, memory, column_slice: Optional[ColumnSlice]):
        """Helper function that extracts the values of the given column slice from the given memory

        NOTE: When column_slice is a single column, this function doesn't return a list. Instead, it returns
        a single value - might happen to be a list (e.g., if the column was a vector column).

        :param memory: The memory to extract values from
        :param column_slice: The slice of columns to extract
        :param force_list: If True, force the return value to be a list
        :return: The values of the given column slice from the given memory

        NOTE: This function is used internally to extract the values of a column slice from a memory.
        """
        if column_slice is None:
            return memory[:]
        elif isinstance(column_slice, (int, slice)):
            return memory[column_slice]
        elif isinstance(column_slice, ColumnName):
            return memory[self.column_to_index[column_slice]]
        elif isinstance(column_slice, list):
            if all(isinstance(col, int) for col in column_slice):
                return [memory[col] for col in column_slice]
            elif all(isinstance(col, ColumnName) for col in column_slice):
                return [memory[self.column_to_index[col]] for col in column_slice]
            else:
                raise ValueError(
                    f"If column_slice is a list, all elements must be either ints or strings (but not a mix). You passed: {column_slice}"
                )
        else:
            raise ValueError(
                f"column_slice must be a slice, int, or list of ints or column names. You passed: {column_slice}"
            )

    def _get_slices(self) -> tuple[Any, Any, Any]:
        """
        Helper function that returns the effective batch, memory, and column slices

        :return: A tuple of the effective batch, memory, and column slices

        NOTE: This function is used internally to get the effective slices for the current BatchedVectorScanResult.
        """
        batch_slice = self.batch_slice if self.batch_slice is not None else slice(None)
        memory_slice = self.memory_slice if self.memory_slice is not None else slice(None)
        column_slice = self.column_slice if self.column_slice is not None else slice(None)

        return batch_slice, memory_slice, column_slice

    def __len__(self) -> int:
        """
        Based on the current slices, return the number of batches, memories, or values in a vector column.

        :return: The return type depends on the current slices:
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(self.batch_slice, int):
            if self.memory_slice is int:
                return len(self._extract_memory_values(self.data[self.batch_slice][memory_slice], column_slice))
            else:
                return len(self.data[batch_slice][memory_slice])
        else:
            return len(self.data[batch_slice])

    def __iter__(self) -> Iterator:
        """
        Iterate over the batches of memories

        :return: The return type depends on the current slices:
        :rtype: Iterator

        - When batch_slice is an int (but memory_slice and column_slice are None), this yields each memory from that batch.

        - When batch_slice and memory_slice are both ints (but column_slice is None), this yields each value from that memory.

        - Otherwise, this yields each batch with the specified subset of selected memories/columns

        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(batch_slice, int):
            if isinstance(memory_slice, int):
                yield from self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
            else:
                yield from (
                    self._extract_memory_values(memory, column_slice) for memory in self.data[batch_slice][memory_slice]
                )
        else:
            yield from (
                [self._extract_memory_values(memory, column_slice) for memory in batch[memory_slice]]
                for batch in self.data[batch_slice]
            )

    def to_list(
        self,
    ) -> list[list[list[Any] | Any]]:
        """
        Convert the values of a vector column to a list of lists

        :return: A list of lists of values

        Example:

        .. code-block:: python

            >>> bsr[0].to_list() # returns the list of memories in the first batch
            >>> bsr[0, 0].to_list() # returns the list of "extra" column values in the first memory of the first batch.
            NOTE:The "special" keys like __vector__ are not included unless they're specifically requested.
            >>> bsr[0, 0, "col1"].to_list() # returns [value of col1] for the first memory of the first batch
            >>> bsr[0, 0, ["col1", "col2"]].to_list() # returns [value of col1, value of col2] for the first memory of the first batch
            >>> bsr[1:3, -2:, ["col1", "col2"]].to_list() # returns a list of lists of [value of col1, value of col2] for
            the last two memories of the second and third batches
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(batch_slice, int):
            if isinstance(memory_slice, int):
                value = self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
                return value if isinstance(value, list) else [value]
            else:
                return [
                    self._extract_memory_values(memory, column_slice) for memory in self.data[batch_slice][memory_slice]
                ]
        else:
            return [
                [self._extract_memory_values(row, column_slice) for row in memories[memory_slice]]
                for memories in self.data[batch_slice]
            ]
