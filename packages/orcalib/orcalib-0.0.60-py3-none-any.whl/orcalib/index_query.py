from typing import Any, Optional

import pandas
from orca_common import ColumnName
from orcalib.batched_scan_result import BatchedScanResult
from orcalib.client import OrcaClient, default_api_version_key
from orcalib.client_data_model import RowDict
from orcalib.constants import EXACT_MATCH_THRESHOLD
from orcalib.orca_expr import ColumnHandle, OrcaExpr
from orcalib.table import TableHandle
from orcalib.table_query import TableQuery

IndexName = str


class DefaultIndexQuery(TableQuery["DefaultIndexQuery"]):
    """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()"""

    def __init__(
        self,
        db_name: str,
        primary_table: TableHandle,
        # The name of the index to query
        # NOTE: Must be an index on primary_table
        index: IndexName,
        # The value to query the index for
        index_query: Any,
        index_value: Optional[ColumnName] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        **kwargs,
    ):
        """
        Initialize a new index-based query on the given table.

        Args:
            db_name (str): The name of the database to query.
            primary_table (str): The primary table to query.
            columns (dict): The columns to select from each table.
            filter (str): The filter to apply to the query.
            order_by_columns (list of str): The columns to order by.
            limit (int): The maximum number of rows to return.
            default_order (str): The default order to use with "order_by" if no order is specified.
            index (IndexName): The name of the index to query.
            index_query (str): The value to query the index for.
            index_value (Optional[ColumnName]): The name of the column to store the index value in. If None, the index value is not stored. (default: None)
        """
        super().__init__(db_name, primary_table, **kwargs)
        self.index = index
        self.index_query = index_query
        self.index_value = index_value
        self.drop_exact_match = drop_exact_match
        self.exact_match_threshold = exact_match_threshold

    def _clone(self, **kwargs) -> "DefaultIndexQuery":
        """
        Clone this query, optionally overriding some parameters

        :param kwargs: The parameters to override
        :return: A new DefaultIndexQuery

        NOTE: This method should not be called directly. It is used internally.
        """
        kwargs["index"] = kwargs.get("index", self.index)
        kwargs["index_query"] = kwargs.get("index_query", self.index_query)
        kwargs["index_value"] = kwargs.get("index_value", self.index_value)
        kwargs["drop_exact_match"] = kwargs.get("drop_exact_match", self.drop_exact_match)
        kwargs["exact_match_threshold"] = kwargs.get("exact_match_threshold", self.exact_match_threshold)
        return super()._clone(**kwargs)

    def _parse_params_columns(self, *columns: str | ColumnHandle) -> list[ColumnName]:
        """Parse the columns parameter into a dict mapping table names to column names

        Unlike the base class, we allow you to request column names that aren't in the primary
        table, so that you can request things like $embedding and $score from the index.

        :param columns: The columns we're parsing. These can be strings or ColumnHandles.
        """
        result = []

        for c in columns:
            if isinstance(c, str):
                result.append(c)
            elif isinstance(c, ColumnHandle):
                result.append(c.column_name)
            else:
                raise ValueError(f"Invalid column: {c}")

        return result

    @default_api_version_key("index.scan")
    def fetch(self, limit: int, api_version: Optional[str]) -> list[RowDict]:
        """
        Fetch the results of this query

        :param limit: The maximum number of rows to return
        :param api_version: The API version to use
        :return: The results of this query
        """
        from orcalib.database import OrcaDatabase

        data = OrcaClient.scan_index(
            OrcaDatabase(self.db_name),
            self.index,
            self.index_query,
            limit=limit,
            columns=self.columns,
            api_version=api_version,
            drop_exact_match=self.drop_exact_match,
            exact_match_threshold=self.exact_match_threshold,
        )

        if self.index_value is not None:
            for row in data:
                row[self.index_value] = row["__index_value"]
                del row["__index_value"]
        return data

    def df(self, limit: Optional[int], explode: bool = False) -> pandas.DataFrame:
        """
        Fetch the results of this query as a pandas DataFrame

        :param limit: The maximum number of rows to return
        :param explode: Whether to explode the index_value column (if it exists) into multiple rows (default: False)
        :return: The results of this query as a pandas DataFrame
        """
        ret = super().df(limit=limit)
        if explode and self.index_value is not None:
            ret = ret.explode(self.index_value, ignore_index=True)
        return ret


class VectorIndexQuery(TableQuery["VectorIndexQuery"]):
    """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()"""

    def __init__(
        self,
        db_name: str,
        primary_table: TableHandle,
        index: IndexName,
        index_query: OrcaExpr,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
        **kwargs,
    ):
        """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()

        :param db_name: The name of the database to query.
        :param primary_table: The primary table to query.
        :param columns: The columns to select
        :param filter: The filter to apply to the query.
        :param order_by_columns: The columns to order by.
        :param limit: The maximum number of rows to return.
        :param default_order: The default order to use with "order_by" if no order is specified.
        :param index: The name of the index to query.
        :param index_query: The value to query the index for.
        :param drop_exact_match: Whether to drop the exact match from the results. (default: False)
        :param exact_match_threshold: The minimum threshold for dropping the exact match. (default: 0.99999)
        :param curate_run_ids: The run ids to use for curate. (default: None)
        :param curate_layer_name: The layer name to use for curate. (default: None)
        """

        super().__init__(db_name, primary_table, **kwargs)
        self.index_name = index
        self.index_query = index_query
        self.curate_run_ids = curate_run_ids
        self.curate_layer_name = curate_layer_name
        self.drop_exact_match = drop_exact_match
        self.exact_match_threshold = exact_match_threshold

    def _clone(self, **kwargs) -> "VectorIndexQuery":
        """
        Clone this query, optionally overriding some parameters

        :param kwargs: The parameters to override
        :return: A new VectorIndexQuery

        NOTE: This method should not be called directly. It is used internally.
        """
        kwargs["index"] = kwargs.get("index", self.index_name)
        kwargs["index_query"] = kwargs.get("index_query", self.index_query)
        kwargs["drop_exact_match"] = kwargs.get("drop_exact_match", self.drop_exact_match)
        kwargs["exact_match_threshold"] = kwargs.get("exact_match_threshold", self.exact_match_threshold)
        kwargs["curate_run_ids"] = kwargs.get("curate_run_ids", self.curate_run_ids)
        kwargs["curate_layer_name"] = kwargs.get("curate_layer_name", self.curate_layer_name)
        return super()._clone(**kwargs)

    # @override
    def _parse_params_columns(self, *columns: str | ColumnHandle) -> list[ColumnName]:
        """Parse the columns parameter into a dict mapping table names to column names"""
        result = []

        for c in columns:
            if isinstance(c, str):
                result.append(c)
            elif isinstance(c, ColumnHandle):
                result.append(c.column_name)
            else:
                raise ValueError(f"Invalid column: {c}")

        return result

    @default_api_version_key("index.vector_scan")
    def fetch(self, limit: int, api_version: Optional[str]) -> BatchedScanResult:
        """
        Fetch the results of this query

        :param limit: The maximum number of rows to return
        :param api_version: The API version to use
        :return: The results of this query
        """

        data = OrcaClient.vector_scan_index(
            self.primary_table,
            self.index_name,
            self.index_query,
            limit=limit,
            columns=self.columns,
            curate_run_ids=self.curate_run_ids,
            curate_layer_name=self.curate_layer_name,
            api_version=api_version,
            drop_exact_match=self.drop_exact_match,
            exact_match_threshold=self.exact_match_threshold,
        )
        return data

    def track_with_curate(self, run_ids: list[int], layer_name: str) -> "VectorIndexQuery":
        """
        Track this query with curate

        :param run_ids: The run ids to use for curate
        :param layer_name: The layer name to use for curate
        :return: A new VectorIndexQuery
        """
        return self._clone(curate_run_ids=run_ids, curate_layer_name=layer_name)
