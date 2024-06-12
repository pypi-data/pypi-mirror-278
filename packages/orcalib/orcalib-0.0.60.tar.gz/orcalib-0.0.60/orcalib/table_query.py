from typing import Any, Generic, Optional, TypeVar

import pandas

from orcalib.client import OrcaClient, default_api_version_key
from orcalib.client_data_model import (
    ColumnName,
    Order,
    OrderByColumn,
    OrderByColumns,
    RowDict,
)
from orcalib.orca_expr import ColumnHandle, OrcaExpr

T = TypeVar("T", bound="TableQuery")


class TableQuery(Generic[T]):
    """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()"""

    # Which database to query
    db_name: str
    # The primary table for the query.
    # TODO: track the joined tables as well
    primary_table: "TableHandle"  # noqa: F821
    # The column names we've selected to return
    columns: list[ColumnName]
    # The filter to apply to the query
    filter: Optional[OrcaExpr]
    # The columns to order by (if any)
    order_by_columns: Optional[OrderByColumns]
    # The maximum number of rows to return
    limit: Optional[int]
    # The default order to use with "order_by" if no order is specified
    default_order: Order

    def __init__(
        self,
        db_name: str,
        primary_table: "TableHandle",  # noqa: F821
        # This is forward looking. Joins are not supported yet!
        columns: Optional[list[ColumnName]] = None,
        filter: Optional[OrcaExpr] = None,
        order_by_columns: Optional[OrderByColumns] = None,
        limit: Optional[int] = None,
        default_order: Order = Order.ASCENDING,
    ):
        """Create a new query on the given table

        :param db_name: The name of the database to query
        :param primary_table: The primary table to query
        :param columns: The columns we're selecting to return (if any) (default: None)
        :param filter: The filter to apply to the query (if any) (default: None)
        :param order_by_columns: The columns to order by (if any) (default: None)
        :param limit: The maximum number of rows to return (default: None)
        :param default_order: The default order to use with "order_by" if no order is specified (default: Order.ASCENDING)
        """
        from orcalib.table import TableHandle

        self.db_name = db_name
        assert isinstance(primary_table, TableHandle)
        self.primary_table = primary_table
        self.columns = columns
        self.filter = filter
        self.order_by_columns = order_by_columns
        self.default_order = default_order
        self.limit = limit

    def _clone(self, **kwargs) -> T:
        """Clone the query, optionally overriding some of the parameters

        NOTE: This is primarily intended for internal use, but may have limited external use (without parameters).

        :param kwargs: The parameters to override
        :return: A new TableQuery with the given parameters overridden
        """
        kwargs["db_name"] = kwargs.get("db_name", self.db_name)
        kwargs["primary_table"] = kwargs.get("primary_table", self.primary_table)
        kwargs["columns"] = kwargs.get("columns", self.columns.copy() if self.columns is not None else None)
        kwargs["filter"] = kwargs.get("filter", self.filter)
        kwargs["order_by_columns"] = kwargs.get(
            "order_by_columns",
            self.order_by_columns.copy() if self.order_by_columns is not None else None,
        )
        kwargs["default_order"] = kwargs.get("default_order", self.default_order)
        kwargs["limit"] = kwargs.get("limit", self.limit)

        return self.__class__(**kwargs)

    def _parse_column_name(self, column: ColumnName | ColumnHandle) -> ColumnName:
        """
        Convert a string or ColumnHandle to a column name, and verify the column exists

        :param column: The column to parse
        :return: The column name

        NOTE: This method should not be called directly. It is used internally.
        """
        if isinstance(column, ColumnHandle):
            col_name = column.column_name
        elif isinstance(column, str):
            col_name = column
        else:
            raise ValueError(f"Invalid type for column parameter: {column}, type: {type(column)}")
        if col_name not in self.primary_table.columns:
            raise ValueError(f"Column '{col_name}' not found in table {self.primary_table.table_name}")
        return col_name

    def _parse_params_columns(self, *columns: str | ColumnHandle) -> list[ColumnName]:
        """
        Parse the columns parameter into a dict mapping table names to column names

        :param columns: The columns to parse
        :return: The parsed columns

        NOTE: This method should not be called directly. It is used internally.
        """
        result = []

        for c in columns:
            if isinstance(c, str):
                result.append(c)
            elif isinstance(c, ColumnHandle):
                result.append(c.column_name)
            else:
                raise ValueError(f"Invalid column: {c}")
        invalid_columns = set(result) - set(self.primary_table.columns.keys())
        if invalid_columns:
            raise ValueError(f"Invalid columns: {invalid_columns} for table {self.primary_table.table_name}")
        return result

    def select(
        self,
        *columns: ColumnName | ColumnHandle | tuple[ColumnName | ColumnHandle, Order],
    ) -> T:
        """
        Selects the given columns from the table. If no columns are specified, all columns are selected.

        :param columns: The columns to select
        :return: A new TableQuery with the given columns selected

        .. code-block:: python

            select("col1", "col2", "col3") # string "ColumnName"
            select("table1.col1", "table2.col2") # string "TableName.ColumnName"
            select(table.column1, table.column2) # Using ColumnHandle

        """
        return self._clone(columns=self._parse_params_columns(*columns))

    def where(self, filter: OrcaExpr) -> T:
        """
        Filters the table by the given filter expression.

        :param filter: The filter expression
        :return: A new TableQuery with the given filter applied
        """
        return self._clone(filter=filter)

    def _parse_param_orderby(
        self,
        *params: ColumnHandle | ColumnName | tuple[ColumnName | ColumnHandle, Order],
    ) -> OrderByColumns:
        """
        Parse any column handles into column names to be compatible with the backend

        :param params: The parameters to parse
        :return: The parsed parameters

        NOTE: This method should not be called directly. It is used internally.
        """
        ret: OrderByColumns = []
        for p in params:
            if isinstance(p, tuple):
                column, order = p
                ret.append((self._parse_column_name(column), order))
            else:
                ret.append((self._parse_column_name(p), Order.DEFAULT))
        return ret

    def order_by(
        self,
        *columns: ColumnName | ColumnHandle | tuple[ColumnName | ColumnHandle, Order],
        default_order: Order = Order.ASCENDING,
    ) -> T:
        """
        Orders the table by the given columns. If no columns are specified, the table is ordered by the primary key.

        :param columns: The columns to order by
        :param default_order: The default order to use with "order_by" if no order is specified (default: Order.ASCENDING)
        :return: A new TableQuery with the given order applied
        """
        if default_order == Order.DEFAULT:
            default_order = Order.ASCENDING
        columns = self._parse_param_orderby(*columns) if columns else None
        return self._clone(order_by_columns=columns, default_order=default_order)

    def limit(self, limit: int) -> T:
        """
        Limits the number of rows returned by the query.

        :param limit: The maximum number of rows to return
        :return: A new TableQuery with the given limit applied
        """
        return self._clone(limit=limit)

    def _apply_default_order(self, t: OrderByColumn) -> tuple[ColumnName, Order]:
        """
        Apply the default order to the given column if no order is specified

        :param t: The column to apply the default order to
        :return: The column with the default order applied

        NOTE: This method should not be called directly. It is used internally.
        """
        if isinstance(t, tuple):
            if t[1] == Order.DEFAULT:
                return (t[0], self.default_order)
            else:
                return t
        if isinstance(t, str):
            return (t, self.default_order)
        raise ValueError(f"Invalid order by column: {t}")

    def _prepare_orderby_columns(self) -> OrderByColumns | None:
        """
        Prepare the order by columns for for the client call in fetch()

        :return: The prepared order by columns

        NOTE: This method should not be called directly. It is used internally.
        """
        orderby_columns = self.order_by_columns
        if orderby_columns is not None:
            if not isinstance(orderby_columns, list):
                orderby_columns = [orderby_columns]
            orderby_columns = list(map(self._apply_default_order, orderby_columns))
        return orderby_columns

    @default_api_version_key("table.fetch")
    def fetch(
        self,
        limit: int | None = None,
        include_ids: bool = False,
        api_version: Optional[str] = None,
        use_msgpack: bool = True,
    ) -> list[RowDict]:
        """Fetch rows from the table

        :param limit: The maximum number of rows to return (default: None)
        :param include_ids: Whether to include the row ids in the result (default: False)
        :param api_version: The API version to use for this request (default: None)
        :return: A list of row data
        """
        passed_filter = self.filter.as_serializable() if self.filter is not None else None
        columns = self.columns or list(self.primary_table.columns.keys())
        orderby_columns = self._prepare_orderby_columns()
        limit = self.limit or limit or None
        res = OrcaClient.select(
            self.primary_table,
            limit=limit,
            columns=columns,
            filter=passed_filter,
            order_by_columns=orderby_columns,
            default_order=self.default_order,
            api_version=api_version,
            use_msgpack=use_msgpack,
        )
        if res["status_code"] != 200:
            raise Exception(f"Error fetching data from {self.table_name}: {res}")

        if include_ids:
            return [(row["row_id"], row["column_values"]) for row in res["rows"]]
        return [row["column_values"] for row in res["rows"]]

    def df(self, limit: int | None) -> pandas.DataFrame:
        """
        Fetch rows from the table and return as a DataFrame

        :param limit: The maximum number of rows to return (default: None)
        :return: A DataFrame of row data
        """
        limit = limit or self.limit
        return pandas.DataFrame(self.fetch(limit=limit))
