from typing import Any, Optional, cast

import datasets
import gradio as gr
import numpy as np
import pandas
import torch
from orcalib.database import OrcaDatabase
from orcalib.file_ingestor import FileIngestorBase
from orcalib.orca_types import (
    BoolT,
    DocumentT,
    FloatT,
    IntT,
    OrcaTypeHandle,
    TextT,
    VectorT,
)
from orcalib.orca_utils import (
    bag_of_words_scores,
    extract_occurance_ranks,
    find_suffixes_in_sequence,
)
from orcalib.table import TableHandle
from transformers import LogitsProcessor


class OrcaGroundingProcessor(LogitsProcessor):
    """
    OrcaGroundingProcessor is a LogitsProcessor that adjusts the logits
    based on the memories in the database."""

    def __init__(
        self,
        memories: list[list[str]],
        tokenizer: Any,
        bag_weight: float = 0.05,
        sim_weight: float = 0.5,
        S_min: int = 3,
        S_max: int = 10,
    ):
        """
        :param memories: List of memories
        :param tokenizer: Tokenizer
        :param bag_weight: Bag of words weight (default: 0.05)
        :param sim_weight: Similarity weight (default: 0.5)
        :param S_min: Minimum suffix length (default: 3)
        :param S_max: Maximum suffix length (default: 10)
        """
        self.memories = memories
        self.bag_weight = bag_weight
        self.sim_weight = sim_weight

        self.tokenizer = tokenizer
        self.S_min = S_min
        self.S_max = S_max

    def _weighted_next_tokens_from_memory(
        self,
        q_tokens: list[int],
        candidates: list[list[int]],
        semantic_scores: list[float],
    ) -> tuple[
        dict[int, float], list[tuple[list[int], float]]
    ]:  # suffix max dict (token -> score), bag_of_words list (token list, score)
        """
        Get the weighted next tokens from memory

        :param q_tokens: Query tokens
        :param candidates: Candidates
        :param semantic_scores: Semantic scores
        :return: Weighted next tokens from memory

        NOTE: This method should not be called directly. It is used internally.
        """
        tokens_and_weights: dict[int, float] = {}
        for candidate, semantic_score in zip(candidates, semantic_scores):
            suffixes = find_suffixes_in_sequence(q_tokens, candidate, self.S_min, self.S_max)
            scores = extract_occurance_ranks(suffixes, len(candidate))
            for token, score in scores.items():
                if token not in tokens_and_weights or score > tokens_and_weights[token]:
                    tokens_and_weights[token] = score * semantic_score
        bag_of_words_tokens: list[list[int]] = candidates
        return {token: score for token, score in tokens_and_weights.items()}, list(
            zip(
                bag_of_words_tokens,
                [x / len(candidates) for x in semantic_scores],
                strict=True,
            )
        )

    def __call__(
        self,
        input_ids: torch.Tensor,
        scores: torch.Tensor,
    ) -> torch.Tensor:
        """
        Call the processor

        :param input_ids: Input ids
        :param scores: Scores
        :return: Adjusted scores
        """
        bs = input_ids.shape[0]
        vocab_size = scores.shape[1]

        bag_adjust = torch.zeros(size=(bs, vocab_size)).to(scores.device)
        sim_adjust = torch.zeros(size=(bs, vocab_size)).to(scores.device)
        for i in range(bs):
            candidates: list[list[int]] = [
                self.tokenizer(self.memories[i][j], add_special_tokens=False).input_ids
                for j in range(len(self.memories[i]))
            ]

            # for now, just exponential decaying weights as memory is lower in position
            # TODO eventually should use the score from ANN
            semantic_scores: list[float] = np.exp(-1 * np.arange(len(self.memories[i]))).tolist()

            input_toks = input_ids[i].tolist()

            sub_candidates, bag_of_words = self._weighted_next_tokens_from_memory(
                q_tokens=input_toks,
                candidates=candidates,
                semantic_scores=semantic_scores,
            )

            bag_adjust_i = bag_of_words_scores(bag_of_words, vocab_size)
            bag_adjust[i] = bag_adjust_i

            for token, score in sub_candidates.items():
                sim_adjust[i, token] = score

        probs = torch.softmax(scores, dim=-1)

        # broadcast/unsqueeze along sequence dimension
        probs = probs + self.sim_weight * sim_adjust + self.bag_weight * bag_adjust

        # renormalize probabilities to sum to 1
        probs = probs / probs.sum(dim=-1, keepdim=True)

        return torch.log(probs)


class HFDatasetIngestor(FileIngestorBase):
    """
    HuggingFace Dataset Ingestor
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset: datasets.arrow_dataset.Dataset | str,
        auto_table: bool = False,
        replace: bool = False,
        split: Optional[str] = None,
        cache_dir: Optional[str] = None,
    ):
        """
        :param db: Database
        :param table_name: Table name
        :param dataset: Dataset
        :param auto_table: Auto table (default: False)
        :param replace: Replace (default: False)
        :param split: Split (default: None)
        :param cache_dir: Cache directory (default: None)
        """
        if auto_table and not replace:
            assert table_name not in db.tables, "Table already exists - can't use auto_table"
        self._db = db
        self._table_name = table_name
        if isinstance(dataset, str):
            temp = datasets.load.load_dataset(dataset, cache_dir=cache_dir)
            if isinstance(temp, datasets.dataset_dict.DatasetDict):
                split = split or "train"
                temp = temp[split]
            assert isinstance(temp, datasets.arrow_dataset.Dataset)
            self._dataset = temp
        else:
            self._dataset = dataset
        self._auto_table = auto_table
        self._replace = replace

    def _create_table(self) -> TableHandle:
        """
        Create table

        :return: Table

        NOTE: This method should not be called directly. It is used internally.
        """
        if self._replace and self._auto_table and self._table_name in self._db.tables:
            self._db.drop_table(self._table_name)
        return self._db.create_table(self._table_name, **self._schema_from_dataset(self._dataset.select([0])[0]))  # type: ignore

    def run(self) -> TableHandle:
        """
        Run

        :return: Table
        """
        if self._auto_table:
            table = self._create_table()
        else:
            table = self._db[self._table_name]
        temp = cast(
            list[dict[str, Any]],
            list(self._dataset),
        )
        table.insert(*temp)
        return table


def getHFModelAndTokenizer(
    model_name: str, cache_dir: Optional[str] = None, hf_access_token: Optional[str] = None
) -> tuple[Any, Any]:
    """
    HuggingFace AutoModel does not currently support Llama-2, hence this function.

    :param model_name: Model name
    :param cache_dir: Cache directory (default: None)
    :param hf_access_token: HuggingFace access token (default: None)
    :return: Model and tokenizer
    """
    try:
        from transformers import AutoModelForPreTraining

        model = AutoModelForPreTraining.from_pretrained(
            model_name,
            device_map="auto",
            cache_dir=cache_dir,
            torch_dtype=torch.float16,
        )
    except Exception as e:
        if model_name.startswith("meta-llama/Llama-2"):
            from transformers import LlamaForCausalLM

            model = LlamaForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                cache_dir=cache_dir,
                torch_dtype=torch.float16,
                token=hf_access_token,
            )
        else:
            print(e)
            raise NotImplementedError

    # Currently AutoTokenizer works for all models
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, token=hf_access_token)

    return model, tokenizer


@DeprecationWarning
class HFAutoModelWrapper:
    """
    HuggingFace AutoModel Wrapper
    """

    def __init__(
        self,
        db: OrcaDatabase,
        index_name: str,
        model_name: str,
        hf_access_token: Optional[str] = None,
    ):
        """
        :param db: Database
        :param index_name: Index name
        :param model_name: Model name
        :param hf_access_token: HuggingFace access token (default: None)
        """
        self.model_name = model_name
        self._db = db
        self._index_name = index_name
        self.override_memories: Optional[pandas.DataFrame] = None
        self.model, self.tokenizer = getHFModelAndTokenizer(model_name=model_name, hf_access_token=hf_access_token)

    def _search_index(self, query: str) -> tuple[str, pandas.DataFrame]:
        """
        Search index

        :param query: Query
        :return: Search index

        NOTE: This method should not be called directly. It is used internally.
        """
        if self.override_memories is None:
            self.latest_memories = (
                self._db.scan_index(index_name=self._index_name, query=query)
                .select("*", index_value="__segment")  # type: ignore
                .df(10, explode=True)
            )
            res = self.latest_memories.to_dict(orient="records")
            return "\n".join([r["__segment"] for r in res]) + "\n", self.latest_memories
        else:
            return (
                "\n".join([r["__segment"] for r in self.override_memories.to_dict(orient="records")]) + "\n",
                self.override_memories,
            )

    def __call__(self, query: str) -> str:
        """
        Call

        :param query: Query
        :return: Response
        """
        context, _ = self._search_index(query)

        input_text = context + "\n\n =================== \n" + query
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.model.device)  # type: ignore

        outputs = self.model.generate(input_ids, max_new_tokens=50)  # type: ignore
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _memory_update(self, df: pandas.DataFrame) -> None:
        """
        Memory update

        :param df: Dataframe

        NOTE: This method should not be called directly. It is used internally.
        """
        self.override_memories = df

    def inspect_latest_memories(self, *columns: str) -> None:
        """
        Inspect latest memories

        :param columns: Columns
        """
        with gr.Blocks() as demo:
            with gr.Row():
                gr.Markdown("# Accessed Memories")
                gr.Markdown("![](file/demo/logo-small.jpg)")
            selected_df = self.latest_memories[list(columns) + ["__segment"]]
            df = gr.Dataframe(wrap=True, headers=["Source Article", "Memory Segment"], interactive=True, value=selected_df)  # type: ignore
            df.change(self._memory_update, inputs=df)
        demo.launch(quiet=True)
