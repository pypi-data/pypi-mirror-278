from itertools import chain
from typing import IO, Any, Optional, cast

import pandas
from orca_common import ColumnName, RowDict, TableName
from orcalib.client import OrcaClient, default_api_version_key
from orcalib.client_data_model import RowData
from orcalib.data_classes import ColumnSpec
from orcalib.orca_expr import ColumnHandle, OrcaExpr
from orcalib.orca_types import CustomSerializable, OrcaTypeHandle
from orcalib.table_query import TableQuery
from tqdm.auto import tqdm


class TableHandle:
    """A handle to a table in the Orca database"""

    db_name: str
    table_name: TableName
    columns: dict[ColumnName, ColumnSpec]

    def __init__(
        self,
        db_name: str,
        table_name: str,
        # This parameter is used when cloning a table handle to prevent unnecessary calls to the server
        _columns: Optional[dict[ColumnName, ColumnSpec]] = None,
    ):
        """Create a handle to a table in the database.

        :param db_name: The database name
        :param table_name: The table name
        """

        #
        if _columns is None:
            table_info = OrcaClient.table_info(db_name, table_name)
            self.columns = {col["name"]: ColumnSpec(**col) for col in table_info}
        else:
            self.columns = _columns

        self.db_name = db_name
        self.table_name = table_name

    def get_column_type_dict(self) -> dict[ColumnName, OrcaTypeHandle]:
        """
        Get a dictionary of column names and orca types for this table

        :return: A dictionary of column names and orca types
        """
        return {name: OrcaTypeHandle.from_string(spec.dtype) for name, spec in self.columns.items()}

    def copy(self) -> "TableHandle":
        """
        Create a copy of this table handle

        :return: A copy of this table handle
        """
        return TableHandle(
            self.db_name,
            self.table_name,
            _columns=self.columns.copy(),
        )

    def copy_with_overrides(self, **kwargs) -> "TableHandle":
        """
        Create a copy of this table handle with the specified attributes changed

        :param kwargs: the attributes to change
        :return: A copy of this table handle with the specified attributes changed
        """
        result = self.copy()

        for key, value in kwargs.items():
            setattr(result, key, value)

        return result

    def __getattr__(self, column_name: str | ColumnHandle) -> ColumnHandle:
        """
        Get a column handle by name

        :param column_name: The name of the column
        :return: A column handle
        """
        if isinstance(column_name, ColumnHandle):
            if column_name.table_name != self.table_name:
                raise ValueError(f"Column {column_name.column_name} not found in table {self.table_name}")
            return column_name
        if column_name not in self.columns:
            raise Exception(f"Column {column_name} not found in table {self.table_name}")
        return ColumnHandle(self.db_name, self.table_name, column_name)

    def __getitem__(self, column_name: str | ColumnHandle) -> ColumnHandle:
        """
        Get a column handle by name

        :param column_name: The name of the column
        :return: A column handle
        """
        return self.__getattr__(column_name)

    def __contains__(self, column_name: str) -> bool:
        return column_name in self.columns

    def get_column(self, column_name: str | ColumnHandle) -> ColumnHandle:
        """
        Get a column handle by name

        :param column_name: The name of the column
        :return: A column handle
        """
        return self.__getattr__(column_name)

    def select(self, *args) -> TableQuery:
        """
        Start a new query on this table

        :param args: The columns to select
        :return: A new table query
        """
        return TableQuery(self.db_name, self).select(*args)

    def where(self, *args) -> TableQuery:
        """
        Start a new query on this table

        :param args: The columns to select
        :return: A new table query
        """
        return TableQuery(self.db_name, self).where(*args)

    def order_by(self, *args, **kwargs) -> TableQuery:
        """
        Start a new query on this table

        :param args: The columns to select
        :return: A new table query
        """
        return TableQuery(self.db_name, self).order_by(*args, **kwargs)

    def fetch(self, *args, **kwargs) -> list[RowDict] | list[tuple[int, RowDict]]:
        """
        Fetch rows from the table

        :param args: The columns to fetch
        :return: A list of rows
        """
        return TableQuery(self.db_name, self).fetch(*args, **kwargs)

    def df(self, limit: Optional[int] = None) -> pandas.DataFrame:
        """
        Fetch rows from the table and return as a pandas DataFrame

        :param limit: The maximum number of rows to fetch (default: None)
        :return: A pandas DataFrame
        """
        return pandas.DataFrame(self.fetch(limit))

    def _extract_rowdicts(self, row_data: RowData) -> list[RowDict]:
        """
        Builds a list of RowDict objects from various sources of row data.

        TODO: Add constraint validation based on column type parameters

        TODO: Collect file-like object dict for binary uploads

        :param row_data: The row data to insert. This can be a RowDict, a pandas DataFrame, or a list of RowDicts.
        :return: A list of RowDict objects

        NOTE: This method should not be called directly. It is used internally.
        """

        if isinstance(row_data, pandas.DataFrame):
            rows = row_data.to_dict(orient="records")
            return cast(list[RowDict], rows)

        match row_data:
            case dict():
                return [row_data]
            case list() as rows:
                unexpected_elements = [(x, type(x)) for x in rows if not isinstance(x, dict)]
                if unexpected_elements:
                    raise TypeError(f"List elements expected to be dict[ColumnName, Any] but got {unexpected_elements}")
                return row_data
            case _:
                raise TypeError(f"Invalid argument for insert: {row_data} type {type(row_data)}")

    def _parse_row_data(self, positional_data: tuple[RowData, ...], kw_data: Any = None) -> list[RowDict]:
        """
        Converts the positional and keyword arguments to a list of RowDict objects

        TODO: Add collecting constraint violations based on column type parameters

        TODO: Add collecting file-like objects for binary uploads

        :param positional_data: The positional row data to insert. This can be a RowDict, a pandas DataFrame, or a list of RowDicts.
        :param kw_data: The keyword row data to insert. This should be a dict[str, Any] where the keys are column names. (default: None)
        :return: A list of RowDict objects

        NOTE: This method should not be called directly. It is used internally.
        """
        # ensure either col or cols is specified, but not both
        if not positional_data and not kw_data:
            raise TypeError("No columns specified for insert")
        if positional_data and kw_data:
            raise TypeError("Cannot specify both positional and keyword arguments")

        if positional_data:
            return list(chain.from_iterable(self._extract_rowdicts(data) for data in positional_data))
        return [kw_data]

    def _extract_binary_values(self, row_dicts: list[RowDict]) -> list[tuple[str, IO[bytes]]]:
        """
        Extracts binary values from row dicts and adds them to the file dict

        NOTE: DO NOT read/log/inspect the file contents before sending them with the request!
        Otherwise, the file pointer will be at the end of the file and the server will receive an empty file.

        :param row_dicts: The row data to insert. This can be a RowDict, a pandas DataFrame, or a list of RowDicts.
        :return: A list of tuples of (filename, file-like object) that is required for the multipart upload

        NOTE: This method should not be called directly. It is used internally.
        """
        # This is a list of tuples of (filename, file-like object) that is required for the multipart upload
        named_file_list: list[tuple[str, IO[bytes]]] = []
        for row_dict in row_dicts:
            for column_name, value in row_dict.items():
                col_type = OrcaTypeHandle.from_string(self.columns[column_name].dtype)
                if not isinstance(col_type, CustomSerializable):
                    continue

                filename = f"upload_{len(named_file_list)}_{column_name}"
                named_file_list.append((filename, col_type.binary_serialize(value)))
                row_dict[column_name] = filename
        return named_file_list

    @default_api_version_key("table.insert")
    def insert(
        self,
        *positions_args: RowData,
        api_version: str | None = None,
        **column_values: Any,
    ) -> None:
        """
        Insert rows into the table

        NOTE: You may not specify both positional and keyword arguments

        :param positions_args: The row data to insert. This can be a RowDict, a pandas DataFrame, or a list of RowDicts.
        :param column_values: Specifies the keys and values to insert. This can be used to insert a single row.
        :param api_version: The version of the API to use (default: None)
        """
        api_version_num = OrcaClient.version_string_to_int(api_version)
        MAX_BATCH_SIZE = 100

        rows = self._parse_row_data(positions_args, column_values)
        if len(rows) <= MAX_BATCH_SIZE:
            file_list = self._extract_binary_values(rows) if api_version_num >= 2 else []
            OrcaClient.insert(self.db_name, self.table_name, rows, file_list, api_version=api_version)
        else:
            # large batch mode
            batches = (rows[i : i + MAX_BATCH_SIZE] for i in range(0, len(rows), MAX_BATCH_SIZE))
            with tqdm(total=len(rows)) as progress_bar:
                for batch in batches:
                    file_list = self._extract_binary_values(batch) if api_version_num >= 2 else []
                    OrcaClient.insert(
                        self.db_name,
                        self.table_name,
                        batch,
                        file_list,
                        api_version=api_version,
                    )
                    progress_bar.update(len(batch))

    @default_api_version_key("table.update")
    def update(self, data: RowDict, filter: OrcaExpr, api_version: str | None = None) -> None:
        """
        Update rows in the table

        :param data: The row data to update. This should be a dict[str, Any] where the keys are column names.
        :param filter: The filter to apply to the rows to update
        :param api_version: The version of the API to use (default: None)
        """
        api_version_num = OrcaClient.version_string_to_int(api_version)

        file_list = self._extract_binary_values([data]) if api_version_num >= 2 else []
        OrcaClient.update(
            self.db_name,
            self.table_name,
            data,
            filter.as_serializable(),
            file_list,
            api_version=api_version,
        )

    @default_api_version_key("table.upsert")
    def upsert(
        self,
        data: RowData,
        key_columns: list[ColumnName],
        api_version: str | None = None,
    ) -> None:
        """
        Upsert rows into the table

        :param data: The row data to insert. This can be a RowDict, a pandas DataFrame, or a list of RowDicts.
        :param key_columns: The columns to use as the primary key
        :param api_version: The version of the API to use (default: None)
        """
        api_version_num = OrcaClient.version_string_to_int(api_version)

        rows = self._parse_row_data((data,))
        file_list = self._extract_binary_values(rows) if api_version_num >= 2 else []
        OrcaClient.upsert(
            self.db_name,
            self.table_name,
            rows,
            key_columns,
            file_list,
            api_version=api_version,
        )

    def delete(self, filter: OrcaExpr) -> None:
        """
        Delete rows from the table

        :param filter: The filter to apply to the rows to delete
        """
        OrcaClient.delete(self.db_name, self.table_name, filter.as_serializable())

    def add_column(self, **columns: OrcaTypeHandle) -> None:
        """
        Add columns to the table

        :param columns: The columns to add
        """
        names, dtypes, notnulls, uniques = [], [], [], []
        for column_name, column_type in columns.items():
            names.append(column_name)
            dtypes.append(column_type.full_name)
            notnulls.append(column_type._notnull)
            uniques.append(column_type._unique)
        OrcaClient.add_column(self.db_name, self.table_name, names, dtypes, notnulls, uniques)
        self.columns.update(
            {
                name: ColumnSpec(name=name, dtype=dtype, notnull=notnull, unique=unique)
                for name, dtype, notnull, unique in zip(names, dtypes, notnulls, uniques)
            }
        )

    def drop_column(self, column_names: list[str] | str) -> None:
        """
        Drop columns from the table

        :param column_names: The column or columns to drop
        """
        column_names = [column_names] if isinstance(column_names, str) else column_names
        OrcaClient.drop_column(self.db_name, self.table_name, column_names)
        for column_name in column_names:
            del self.columns[column_name]

    def __str__(self) -> str:
        """
        Get a string representation of this table handle

        :return: A string representation of this table handle
        """
        ret = f"{self.db_name}.{self.table_name}(\n"
        for column in self.columns.values():
            ret += f"\t{column.name} {column.dtype}{' NOT NULL' if column.notnull else ''}{' UNIQUE' if column.unique else ''},\n"
        ret += ")"
        return ret

    def __repr__(self) -> str:
        """
        Get a string representation of this table handle

        :return: A string representation of this table handle
        """
        return self.__str__()
