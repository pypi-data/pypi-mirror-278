from typing import Any, Optional

from orca_common import ColumnName
from orca_common.embedding_models import EmbeddingModel
from orcalib.constants import EXACT_MATCH_THRESHOLD
from orcalib.orca_types import NumericTypeHandle, OrcaTypeHandle


class IndexHandle:
    """A handle to an index in an Orca database."""

    def __init__(
        self,
        name: str,
        db_name: str,
        table_name: str,
        column_name: ColumnName,
        column_type: OrcaTypeHandle,
        embedding_type: OrcaTypeHandle,
        index_type: str,
        artifact_columns: dict[ColumnName, str | OrcaTypeHandle],
        embedding_model: EmbeddingModel | None = None,
    ):
        """
        :param name: Name of this index
        :param db_name: Database that this index belongs to
        :param table_name: Table that this index belongs to
        :param column_name: Name of the column that this index is built on
        :param column_type: Type of the column that this index is built on
        :param embedding_type: Type of the vector embedding used by this index (if any)
        :param index_type: Type of this index
        :param artifact_columns: Artifact columns that are available from the index
        """
        self.name = name
        self.db_name = db_name
        self.table_name = table_name
        self.column_name = column_name
        self.column_type = column_type
        self.embedding_type = embedding_type
        self.index_type = index_type
        self.artifact_columns: dict[ColumnName, OrcaTypeHandle] = {
            column: (OrcaTypeHandle.from_string(column_type) if isinstance(column_type, str) else column_type)
            for column, column_type in artifact_columns.items()
        }
        self.embedding_model = embedding_model

    @property
    def embedding_dim(self) -> Optional[int]:
        """Return the embedding dimension of this index (if any).

        :return: embedding dimension
        :rtype: Optional[int]
        """
        if self.embedding_type is None or not isinstance(self.embedding_type, NumericTypeHandle):
            return None

        return self.embedding_type.length

    def scan(
        self,
        query: Any,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> "DefaultIndexQuery":  # noqa: F821
        """
        Scan the index for a given query. This is the default index query method.

        :param query: Query to scan the index with
        :return: DefaultIndexQuery
        """
        from orcalib.database import OrcaDatabase
        from orcalib.index_query import DefaultIndexQuery

        return DefaultIndexQuery(
            db_name=self.db_name,
            primary_table=OrcaDatabase(self.db_name).get_table(self.table_name),
            index=self.name,
            index_query=query,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
        )

    def vector_scan(
        self,
        query: Any,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> "VectorIndexQuery":  # noqa: F821
        """
        Scan the index for a given query. This is the vector index query method.

        :param query: Query to scan the index with
        :return: VectorIndexQuery
        """
        from orcalib.database import OrcaDatabase
        from orcalib.index_query import VectorIndexQuery

        return VectorIndexQuery(
            db_name=self.db_name,
            primary_table=OrcaDatabase(self.db_name).get_table(self.table_name),
            index=self.name,
            index_query=query,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
        )

    def get_status(self) -> dict[str, Any]:
        """
        Get the status of this index.

        :return: Index status
        """
        from orcalib.client import OrcaClient

        return OrcaClient.get_index_status(self.db_name, self.name)

    def __str__(self) -> str:
        """
        Return a string representation of this index.

        :return: String representation
        """
        return f"{self.index_type} index: {self.name} on {self.db_name}.{self.table_name}.{self.column_name} ({self.column_type})"

    def __repr__(self) -> str:
        """
        Return a string representation of this index.

        :return: String representation
        """
        return str(self)
