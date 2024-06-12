import json
import os
import time
from functools import wraps
from typing import IO, Any, Optional, TypedDict
from uuid import UUID

import msgpack
import numpy as np
import requests
from orca_common import ColumnName, Order, OrderByColumns, RowDict, TableCreateMode
from orca_common.embedding_models import EmbeddingModel
from orcalib.client_data_model import (
    ApiFilter,
    SimpleTableQueryRequest,
    TableSelectResponse,
    decode_ndarray,
)
from orcalib.constants import EXACT_MATCH_THRESHOLD
from orcalib.exceptions import (
    OrcaBadRequestException,
    OrcaException,
    OrcaNotFoundException,
    OrcaUnauthenticatedException,
    OrcaUnauthorizedException,
)
from orcalib.index_handle import IndexHandle
from orcalib.orca_types import CustomSerializable, OrcaTypeHandle
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

OrcaMetadataDict = dict[str, str | int | float | bool | list[str] | list[int] | list[float] | list[bool] | None]


class ApiColumnSpec(TypedDict):
    name: str
    notnull: bool
    unique: bool
    dtype: str


def _prepare_file_list(files: list[tuple[str, IO[bytes]]]) -> list[tuple[str, tuple[str, IO[bytes]]]]:
    """
    Prepare the file list for a multipart request

    :param files: The list of files to prepare
    :return: The prepared file list

    NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
    """
    return [("files", (file_name, file_bytes)) for file_name, file_bytes in files]


def default_api_version_key(api_version_key: str) -> Any:
    """
    Automatically sets the `api_version` kwarg to the current api version using the specific api version key
    Essentially, it replaces a None `api_version` parameter with `OrcaClient.current_api_version[api_version_key]`

    :param api_version_key: The key to use to get the current api version
    :return: The decorator
    """

    def decorator(func: Any) -> Any:
        """
        The decorator

        :param func: The function to decorate
        :return: The decorated function
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            The wrapper

            :param args: The arguments
            :param kwargs: The keyword arguments
            :return: The result of the function
            """
            api_version = kwargs.get("api_version") or OrcaClient.current_api_version[api_version_key]
            kwargs["api_version"] = api_version
            return func(*args, **kwargs)

        return wrapper

    return decorator


class OrcaClient:
    """
    The OrcaClient class is used to make requests to the Orca web service
    """

    # The api key to use for the session locally (should not store in code, use environment variables or similar instead)
    API_KEY = "my_api_key"
    # The secret key to use for the session locally (should not store in code, use environment variables or similar instead)
    SECRET_KEY = "my_secret_key"
    # The base url for the local web service
    BASE_URL = "http://localhost:1583/"

    # Holds the current api version for each endpoint
    current_api_version = {
        "table.fetch": "v2",
        "table.insert": "v2",
        "table.update": "v2",
        "table.upsert": "v2",
        "index.scan": "v2",
        "index.vector_scan": "v3",
        "index.get": "v3",
        "index.create": "v3",
    }

    @staticmethod
    def version_string_to_int(api_version: str) -> int:
        """Returns the integer version number from the api version string

        :param api_version: The api version string
        :return: The integer version number

        Example: "v1" -> 1
        """
        if api_version is None or not api_version.startswith("v") or len(api_version) < 2:
            raise ValueError(f"Invalid api version: {api_version}. Version should be a string like 'v1'")
        version = int(api_version[1:])
        if version < 1:
            raise ValueError(f"Invalid api version: {api_version}. Version must be >= 1")
        return version

    @staticmethod
    def set_credentials(*, api_key: str, secret_key: str, endpoint: Optional[str] = None) -> None:
        """
        Set the api and secret key for the session

        :param api_key: The api key
        :param secret_key: The secret key
        :param endpoint: The endpoint to use (optional)
        """
        OrcaClient.API_KEY = api_key
        OrcaClient.SECRET_KEY = secret_key
        if endpoint is not None and endpoint[-1] != "/" and os.name == "nt":  # windows compatibility
            endpoint += "/"
        if endpoint:
            OrcaClient.BASE_URL = endpoint

    @staticmethod
    def _format_num_bytes(num: int, suffix: str = "B") -> str:
        """
        Format a number of bytes into a human readable string

        :param num: The number of bytes
        :param suffix: The suffix to use (default: "B")
        :return: The formatted string of bytes

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    @staticmethod
    def _orca_request(
        method: str,
        url: str,
        request_params: Optional[dict[str, Any]] = None,
        retries: int = 3,
        verbose: bool = False,
        file_path: str = None,
    ) -> requests.Response:
        """
        Perform the http request to the web service with auth details

        :param method: The http method to use
        :param url: The url to request
        :param request_params: The parameters to send with the request (optional)
        :param retries: The number of times to retry the request if it fails (default: 3)
        :param verbose: If True, print verbose output about the request (default: False)
        :param file_path: The path to a file to upload (optional)
        :return: The response from the web service

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """

        if request_params is None:
            request_params = {}

        if method == "GET":
            assert "json" not in request_params, "GET requests cannot have a body"

        if verbose:
            print(f"Orca request start: {method} {url}")

        start_time = time.time()

        request_params["headers"] = {
            **{
                "api-key": OrcaClient.API_KEY,
                "secret-key": OrcaClient.SECRET_KEY,
            },
            **request_params.get("headers", {}),
        }

        status_force_retry = [500, 502, 504]

        retry_config = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=0.3,
            status_forcelist=status_force_retry,
        )

        adapter = HTTPAdapter(max_retries=retry_config)
        with requests.Session() as session:
            session.mount(url, adapter)
            if verbose:
                print(f"Orca request params: {request_params}")
            # Needed because requests.request has issues with large file upload: ChunkedEncodingError
            if file_path:
                file = {"file": open(file_path, "rb")}
                resp = requests.post(url=url, files=file, **request_params)
            else:
                resp = requests.request(method=method, url=url, **request_params)

        end_time = time.time()

        elapsed_time_ms = int((end_time - start_time) * 1000)

        if verbose:
            content_length = OrcaClient._format_num_bytes(len(resp.content))
            print(f"Orca request end: {method} {url} {resp.status_code} {content_length} {elapsed_time_ms}ms")

        if not resp.ok:
            if resp.status_code == 404:
                raise OrcaNotFoundException(resp.content)
            elif resp.status_code == 401:
                raise OrcaUnauthenticatedException(resp.content)
            elif resp.status_code == 403:
                raise OrcaUnauthorizedException(resp.content)
            elif resp.status_code == 400:
                raise OrcaBadRequestException(resp.content)
            raise OrcaException(resp.content)

        return resp

    @staticmethod
    def create_database(db_name: str) -> requests.Response:
        """
        Create a new database

        :param db_name: The name of the database
        :return: Creat database response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/create_database")
        request_params = {"params": {"db_name": db_name}}
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def drop_database(db_name: str, ignore_db_not_found: bool = False) -> bool:
        """
        Drop the database

        :param db_name: The name of the database
        :param ignore_db_not_found: If True, ignore the error if the database is not found (default: False)
        :return: True if the database was dropped, False if it was not found
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/drop/db/{db_name}")
        request_params = {"params": {"ignore_db_not_found": ignore_db_not_found}}
        res = OrcaClient._orca_request("DELETE", url, request_params)
        return res.json()["value"]

    @staticmethod
    def database_exists(db_name: str) -> bool:
        """
        Check if the database exists

        :param db_name: The name of the database
        :return: True if the database exists, False if it does not
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/exists/db/{db_name}")
        request_params = {"params": {}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()["value"]

    @staticmethod
    def restore_backup(target_db_name: str, backup_name: str, checksum: str | None = None) -> requests.Response:
        """
        Restore a database from a backup

        :param target_db_name: The name of the target database
        :param backup_name: The name of the backup
        :param checksum: The checksum of the backup file (optional)
        :return: Restore database response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/restore_database")
        request_params = {
            "params": {
                "target_db_name": target_db_name,
                "backup_name": backup_name,
                "checksum": checksum,
            }
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def create_backup(db_name: str) -> requests.Response:
        """
        Create a backup of the database

        :param db_name: The name of the database
        :return: Create backup response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/backup_database")
        request_params = {"params": {"db_name": db_name}}
        res = OrcaClient._orca_request("POST", url, request_params)
        return res.json()

    @staticmethod
    def download_backup(backup_file: str, download_path: str = "./data", overwrite: bool = False) -> requests.Response:
        """
        Download a backup from the server

        :param backup_file: The name of the backup file
        :param download_path: The path to download the backup file to (default: "./data")
        :param overwrite: If True, overwrite the file if it already exists (default: False)
        :return: Download backup response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/download_backup")
        request_params = {"params": {"backup_file": backup_file}}
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        download_file_location = f"{download_path}/{backup_file}"
        if not overwrite and os.path.exists(download_file_location):
            raise ValueError(f"{download_file_location} already exists")
        res = OrcaClient._orca_request("GET", url, request_params)
        with open(download_file_location, "wb") as f:
            f.write(res.content)
        return res

    @staticmethod
    def upload_backup(file_path: str) -> requests.Response:
        """
        Upload a backup to the server

        :param file_path: The path to the backup file
        :return: Upload backup response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/upload_backup")
        res = OrcaClient._orca_request("POST", url, file_path=file_path)
        return res

    @staticmethod
    def delete_backup(backup_file_name: str) -> requests.Response:
        """
        Delete a backup from the server

        :param backup_file_name: The name of the backup file
        :return: Delete backup response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/delete_backup")
        request_params = {"params": {"backup_file_name": backup_file_name}}
        res = OrcaClient._orca_request("DELETE", url, request_params)
        return res

    @staticmethod
    def list_databases() -> list[str]:
        """
        List all the databases on the server

        :return: List of database names
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/list_databases")
        res = OrcaClient._orca_request("GET", url)
        return res.json()["databases"]

    @staticmethod
    def list_tables(db_name: str) -> list[str]:
        """
        List all the tables in the database

        :param db_name: The name of the database
        :return: List of table names
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/get_tables")
        request_params = {"params": {"db_name": db_name}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()["tables"]

    @staticmethod
    def table_info(db_name: str, table_name: str) -> list[ApiColumnSpec]:
        """
        Get the information about a table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :return: Table information
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/table_info")
        request_params = {"params": {"db_name": db_name, "table_name": table_name}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()

    @staticmethod
    def healthcheck() -> dict[str, Any]:
        """
        Perform a healthcheck on the server

        :return: Healthcheck response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/healthcheck")
        res = OrcaClient._orca_request("GET", url)
        return res.json()

    @staticmethod
    def create_table(
        db_name: str,
        table_name: str,
        table_schema: list[dict[str, Any]],
        if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
    ) -> requests.Response:
        """
        Create a new table in the database

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param table_schema: The schema of the table
        :param if_table_exists: What to do if the table already exists (default: TableCreateMode.ERROR_IF_TABLE_EXISTS)
        :return: Create table response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/create_table")
        request_params = {
            "params": {
                "db_name": db_name,
                "table_name": table_name,
                "if_table_exists": if_table_exists.name,
            },
            "json": table_schema,
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    @default_api_version_key("table.insert")
    def insert(
        db_name: str,
        table_name: str,
        rows: list[RowDict],
        files: list[tuple[str, IO[bytes]]],
        api_version: str | None = None,
    ) -> requests.Response:
        """
        Insert rows into the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param rows: The rows to insert
        :param files: The files to upload
        :param api_version: The api version to use (optional)
        :return: Insert response
        """
        if api_version == "v1":
            url = os.path.join(OrcaClient.BASE_URL, "v1/insert")
            request_params = {
                "params": {"db_name": db_name, "table_name": table_name},
                "json": rows,
            }
        elif api_version == "v2":
            url = os.path.join(OrcaClient.BASE_URL, f"{api_version}/db/insert/{db_name}/{table_name}")
            request_params = {
                "data": {"data": json.dumps({"rows": rows})},
                "files": _prepare_file_list(files),
            }
        else:
            raise ValueError(f"Unsupported api version: {api_version}")
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    @default_api_version_key("table.update")
    def update(
        db_name: str,
        table_name: str,
        row: RowDict,
        filter: Any,
        files: list[tuple[str, IO[bytes]]],
        api_version: str | None = None,
    ) -> requests.Response:
        """
        Update a row in the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param row: The row to update
        :param filter: The filter to apply
        :param files: The files to upload
        :param api_version: The api version to use (optional)
        :return: Update response
        """
        if api_version == "v1":
            url = os.path.join(OrcaClient.BASE_URL, "v1/update")
            request_params = {
                "params": {"db_name": db_name, "table_name": table_name},
                "json": {"item": row, "filter": filter},
            }
        elif api_version == "v2":
            url = os.path.join(OrcaClient.BASE_URL, f"v2/db/update/{db_name}/{table_name}")
            request_params = {
                "data": {"data": json.dumps({"row": row, "filter": filter})},
                "files": _prepare_file_list(files),
            }
        else:
            raise ValueError(f"Unsupported api version: {api_version}")
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    @default_api_version_key("table.upsert")
    def upsert(
        db_name: str,
        table_name: str,
        rows: list[RowDict],
        key_columns: list[str],
        files: list[tuple[str, IO[bytes]]],
        api_version: str | None = None,
    ) -> requests.Response:
        """
        Upsert rows into the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param rows: The rows to upsert
        :param key_columns: The key columns to use for the upsert
        :param files: The files to upload
        :param api_version: The api version to use (optional)
        :return: Upsert response
        """
        if api_version == "v1":
            url = os.path.join(OrcaClient.BASE_URL, "v1/upsert")
            request_params = {
                "params": {"db_name": db_name, "table_name": table_name},
                "json": {"items": rows, "key_columns": key_columns},
            }
        elif api_version == "v2":
            url = os.path.join(OrcaClient.BASE_URL, f"v2/db/upsert/{db_name}/{table_name}")
            request_params = {
                "data": {"data": json.dumps({"rows": rows, "key_columns": key_columns})},
                "files": _prepare_file_list(files),
            }
        else:
            raise ValueError(f"Unsupported api version: {api_version}")
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def delete(db_name: str, table_name: str, filter: Any) -> requests.Response:
        """
        Delete rows from the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param filter: The filter to apply
        :return: Delete response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/delete")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": filter,
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def add_column(
        db_name: str,
        table_name: str,
        new_col: list[str],
        dtype: list[str],
        notnull: list[bool],
        unique: list[bool],
    ) -> requests.Response:
        """
        Add a new column to the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param new_col: The name of the new column
        :param dtype: The data type of the new column
        :param notnull: If the new column is not null
        :param unique: If the new column is unique
        :return: Add column response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/add_column")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": {
                "new_col": new_col,
                "dtype": dtype,
                "notnull": notnull,
                "unique": unique,
            },
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def drop_column(
        db_name: str,
        table_name: str,
        col_names: list[str],
    ) -> requests.Response:
        """
        Drop a column from the table

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param col_names: The name of the column to drop
        :return: Drop column response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_column")
        request_params = {
            "params": {"db_name": db_name, "table_name": table_name},
            "json": col_names,
        }
        res = OrcaClient._orca_request("POST", url, request_params)
        return res

    @staticmethod
    def drop_table(db_name: str, table_name: str, error_if_not_exists: bool = True) -> requests.Response:
        """
        Drop a table from the database

        :param db_name: The name of the database
        :param table_name: The name of the table
        :param error_if_not_exists: If True, raise an error if the table does not exist (default: True)
        :return: Drop table response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_table")
        request_params = {
            "params": {
                "db_name": db_name,
                "table_name": table_name,
                "error_if_not_exists": error_if_not_exists,
            },
            "json": [],
        }
        res = OrcaClient._orca_request("DELETE", url, request_params)
        return res

    @staticmethod
    def drop_index(db_name: str, index_name: str) -> requests.Response:
        """
        Drop an index from the database

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: Drop index response
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/drop_index")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
            "json": [],
        }
        res = OrcaClient._orca_request("DELETE", url, request_params)
        return res

    @staticmethod
    @default_api_version_key("table.fetch")
    def select(
        table: "TableHandle",  # noqa: F821
        columns: Optional[list[ColumnName]] = None,
        limit: Optional[int] = None,
        filter: Optional[ApiFilter] = None,
        order_by_columns: Optional[OrderByColumns] = None,
        default_order: Order = Order.ASCENDING,
        api_version: str | None = None,
        use_msgpack: bool = True,
    ) -> TableSelectResponse:
        """
        Perform a select query on the table

        :param table: The TableHandle for the table we're querying
        :param columns: The columns to select. If None, all columns are selected (default: None)
        :param limit: The maximum number of rows to return (default: None)
        :param filter: The filter to apply to the query (default: None)
        :param order_by_columns: The columns to order by. If None, no order is applied. (default: None)
        :param default_order: The default order to use if no order is specified. Defaults to ascending. (default: Order.ASCENDING)
        :param api_version: The api version to use (default: None)
        :return: The response from the select query

        Example:

        .. code-block:: python

            >>> OrcaClient.select(OrcaTableHandle("my_db", "my_table"),
                                    columns=["col1", "col2"],
                                    limit=100,
                                    filter={"col1": {"$gt": 10}},
                                    order_by_columns=["col1", ("col2", Order.DESCENDING)])

        """
        url = os.path.join(
            OrcaClient.BASE_URL,
            f"{api_version}/select/db/{table.db_name}/{table.table_name}",
        )
        params = SimpleTableQueryRequest(
            columns=columns,
            limit=limit,
            filter=filter,
            order_by_columns=order_by_columns,
            default_order=default_order,
        )
        request = {
            "params": {},
            "json": params.dict(by_alias=True, exclude_unset=True),
        }

        if not use_msgpack:
            request["headers"] = {"Accept": "application/json"}

        response = OrcaClient._orca_request("POST", url, request)

        if response.headers["Content-Type"] == "application/json":
            content = response.json()
        elif response.headers["Content-Type"] == "application/msgpack":
            content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        else:
            raise ValueError(f"Unsupported content type: {response.headers['Content-Type']}")

        col_name_to_type = {
            col_name: OrcaTypeHandle.from_string(table.columns[col_name].dtype) for col_name in table.columns
        }

        for row in content["rows"]:
            OrcaClient._deserialize_column_value_dict(col_name_to_type, row["column_values"])

        return content

    @staticmethod
    def _deserialize_column_value(col_type: OrcaTypeHandle, value: Any) -> Any:
        """
        Deserialize a single column value using the column's data type

        :param col_type: The column's data type
        :param value: The value to deserialize
        :return: The deserialized value

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        if not isinstance(col_type, CustomSerializable):
            return value
        assert isinstance(value, dict)
        return col_type.msgpack_deserialize(value)

    @staticmethod
    def _deserialize_column_value_dict(col_name_to_type: dict[ColumnName, OrcaTypeHandle], row_values: RowDict) -> None:
        """
        Deserialize a dictionary of column values using the given type dictionary

        NOTE: This updates the dictionary in place!!

        This is used to deserialize the results of select

        :param col_name_to_type: A dictionary of column names to their data types
        :param row_values: The dictionary of column values to deserialize

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        for col_name, col_type in col_name_to_type.items():
            if col_name in row_values:
                row_values[col_name] = OrcaClient._deserialize_column_value(col_type, row_values[col_name])

    @staticmethod
    def _deserialize_column_value_list(ordered_type_list: list[OrcaTypeHandle], value_list: list[Any]) -> list[Any]:
        """
        Deserialize a list of column values using the given type list

        This is used to deserialize the results of scan_index and vector_scan_index

        :param ordered_type_list: A list of column data types
        :param value_list: The list of column values to deserialize
        :return: The deserialized list of column values

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        assert len(ordered_type_list) == len(value_list)
        return [OrcaClient._deserialize_column_value(t, v) for t, v in zip(ordered_type_list, value_list)]

    @staticmethod
    def _create_index_v1(
        db_name: str, index_name: str, table_name: str, column: str, index_type: str
    ) -> requests.Response:
        """
        Create a new index (v1)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param table_name: The name of the table
        :param column: The name of the column to index
        :param index_type: The type of the index
        :return: Create index response (requests.Response)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.

        embedding_model only applies to text or document indexes and will default to sentence_transformer if None is provided.
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/create_index")
        request_params = {
            "params": {
                "index_type": index_type,
                "index_name": index_name,
                "db_name": db_name,
            },
            "json": [{"database": db_name, "table": table_name, "column": column}],
        }

        return OrcaClient._orca_request("POST", url, request_params, verbose=False)

    @staticmethod
    def _create_index_v2(db_name: str, index_name: str, table_name: str, column: str, index_type: str) -> IndexHandle:
        """
        Create a new index (v2)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param table_name: The name of the table
        :param column: The name of the column to index
        :param index_type: The type of the index
        :return: Create index response (IndexHandle)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.

        embedding_model only applies to text or document indexes and will default to sentence_transformer if None is provided.
        """
        url = os.path.join(OrcaClient.BASE_URL, "v2/create_index")
        request_params = {
            "params": {
                "index_type": index_type,
                "index_name": index_name,
                "db_name": db_name,
            },
            "json": [{"database": db_name, "table": table_name, "column": column}],
        }

        json = OrcaClient._orca_request("POST", url, request_params, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    @staticmethod
    def _create_index_v3(
        db_name: str,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        ann_index_type: str,
        embedding_model: EmbeddingModel | None = None,
    ) -> IndexHandle:
        """
        Create a new index (v3)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param table_name: The name of the table
        :param column: The name of the column to index
        :param index_type: The type of the index
        :param embedding_model: The name of the embedding model (optional) (roberta, sentence_transformer)
        :return: Create index response (IndexHandle)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.

        embedding_model only applies to text or document indexes and will default to sentence_transformer if None is provided.
        """
        url = os.path.join(OrcaClient.BASE_URL, "v3/create_index")
        request_params = {
            "params": {
                "index_type": index_type,
                "index_name": index_name,
                "ann_index_type": ann_index_type,
                "db_name": db_name,
                "embedding_model": embedding_model,
            },
            "json": [{"database": db_name, "table": table_name, "column": column}],
        }

        json = OrcaClient._orca_request("POST", url, request_params, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    create_index_strategy = {
        "v1": _create_index_v1,
        "v2": _create_index_v2,
        "v3": _create_index_v3,
    }

    @staticmethod
    @default_api_version_key("index.create")
    def create_index(
        db_name: str,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        ann_index_type: str = "hnswlib",
        api_version: str | None = None,
        embedding_model: EmbeddingModel | None = None,
    ) -> IndexHandle:
        """
        Create a new index

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param table_name: The name of the table
        :param column: The name of the column to index
        :param index_type: The type of the index
        :param api_version: The api version to use (optional)
        :param embedding_model: The name of the embedding model (optional) (roberta, sentence_transformer)
        :return: Create index response (requests.Response (v1) or IndexHandle (v2))

        NOTE: embedding_model only applies to text or document indexes and will default to sentence_transformer if None is provided.
        """
        call_correct_version = OrcaClient.create_index_strategy.get(api_version, None)
        if call_correct_version is None:
            raise ValueError(f"Unsupported get_index api version: {api_version}")
        if api_version == "v3":
            return call_correct_version(
                db_name, index_name, table_name, column, index_type, ann_index_type, embedding_model
            )
        return call_correct_version(db_name, index_name, table_name, column, index_type)

    @staticmethod
    def get_index_status(db_name: str, index_name: str) -> dict[str, Any]:
        """
        Get the status of an index

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: Get index status response
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/get_index_status/{db_name}/{index_name}")
        request_params = {"params": {}}
        res = OrcaClient._orca_request("GET", url, request_params)
        return res.json()

    @staticmethod
    def _get_index_v1(db_name: str, index_name: str):
        """
        Get the details of an index (v1)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The index details (v1) (IndexHandle)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v1/db/index_info/{db_name}/{index_name}")
        json = OrcaClient._orca_request("GET", url, None, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json, artifact_columns={})

    @staticmethod
    def _get_index_v2(db_name: str, index_name: str):
        """
        Get the details of an index (v2)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The index details (v2) (IndexHandle)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/index_info/{db_name}/{index_name}")
        json = OrcaClient._orca_request("GET", url, None, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    @staticmethod
    def _get_index_v3(db_name: str, index_name: str):
        """
        Get the details of an index (v3)

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The index details (v3) (IndexHandle)

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/index_info/{db_name}/{index_name}")
        json = OrcaClient._orca_request("GET", url, None, verbose=False).json()
        json["column_type"] = OrcaTypeHandle.from_string(json["column_type"])
        embed_type = json.get("embedding_type", None)
        json["embedding_type"] = OrcaTypeHandle.from_string(embed_type) if embed_type else None
        return IndexHandle(**json)

    get_index_strategy = {
        "v1": _get_index_v1,
        "v2": _get_index_v2,
        "v3": _get_index_v3,
    }

    @staticmethod
    @default_api_version_key("index.get")
    def get_index(db_name: str, index_name: str, api_version: str | None = None) -> IndexHandle:
        """
        Get the details of an index

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The index details

        """
        call_correct_version = OrcaClient.get_index_strategy.get(api_version, None)
        if call_correct_version is None:
            raise ValueError(f"Unsupported get_index api version: {api_version}")
        return call_correct_version(db_name, index_name)

    @staticmethod
    def _scan_index_v1(
        db: "OrcaDatabase",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> dict[str, Any]:
        """
        Scan an index

        :param db: The OrcaDatabase object
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: UNUSED in this version
        :param exact_match_threshold: UNUSED in this version
        :return: The response from the scan index query

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/scan_index")
        request_params = {
            "params": {"db_name": db.name, "index_name": index_name},
            "json": {
                "query": query,
                "columns": columns,
                "limit": limit,
                "filter": filter,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} fetching data from {index_name}: {response.text}")

        return response.json()

    @staticmethod
    def _scan_index_v2(
        db: "OrcaDatabase",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> list[RowDict]:
        """
        Scan an index

        :param db: The OrcaDatabase object
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: Drops the exact match from the results, if it's found
        :param exact_match_threshold: The minimum distance threshold for the exact match
        :return: The response from the scan index query

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/scan_index/{db.name}/{index_name}")
        table = db._get_index_table(index_name)
        request_params = {
            "json": {
                "columns": columns,
                "filter": filter,
                "primary_table": table.table_name,
                "max_neighbor_count": limit,
                "index_query": query,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        col_name_to_type = {
            col_name: OrcaTypeHandle.from_string(table.columns[col_name].dtype) for col_name in table.columns
        }
        for row_values in content:
            OrcaClient._deserialize_column_value_dict(col_name_to_type, row_values)

        return content

    scan_index_strategy = {
        "v1": _scan_index_v1,
        "v2": _scan_index_v2,
    }

    @staticmethod
    @default_api_version_key("index.scan")
    def scan_index(
        db: "OrcaDatabase",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        api_version: str | None = None,
    ) -> Any:
        """
        Scan an index

        :param db: The OrcaDatabase object
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: Drops the exact match from the results, if it's found
        :param exact_match_threshold: The minimum distance threshold for the exact match
        :param api_version: The api version to use (optional)
        :return: The response from the scan index query
        """
        call_correct_version = OrcaClient.scan_index_strategy.get(api_version, None)
        if call_correct_version is None:
            raise ValueError(f"Unsupported scan_index api version: {api_version}")
        return call_correct_version(
            db,
            index_name,
            query,
            limit,
            columns,
            filter,
            drop_exact_match,
            exact_match_threshold,
        )

    @staticmethod
    def _vector_scan_index_v1(
        table: "TableHandle",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Scan a vector index

        :param table: The TableHandle for the table we're querying
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: UNUSED in this version
        :param exact_match_threshold: UNUSED in this version
        :param curate_run_ids: The curate run ids to apply (optional)
        :param curate_layer_name: The curate layer name to apply (optional)
        :return: The response from the scan index query

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/vector_scan_index")
        request_params = {
            "params": {"db_name": table.db_name, "index_name": index_name},
            "json": {
                "query": query,
                "columns": columns,
                "limit": limit,
                "filter": filter,
                "curate_run_ids": curate_run_ids,
                "curate_layer_name": curate_layer_name,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} fetching data from {index_name}: {response.text}")
        return response.json()

    @staticmethod
    def _vector_scan_index_v2(
        table: "TableHandle",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
    ) -> "BatchedVectorScanResult_V2":  # noqa: F821
        """
        Scan a vector index

        :param table: The TableHandle for the table we're querying
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: UNUSED in this version
        :param exact_match_threshold: UNUSED in this version
        :param curate_run_ids: The curate run ids to apply (optional)
        :param curate_layer_name: The curate layer name to apply (optional)
        :return: The response from the scan index query

        NOTE: This function should not be called directly. It is used internally by the OrcaClient class.
        """
        # TODO: When we remove this, also remove BatchedVectorScanResult_V2
        from orcalib.index_query import BatchedVectorScanResult_V2

        url = os.path.join(OrcaClient.BASE_URL, f"v2/db/vector_scan_index/{table.db_name}/{index_name}")
        request_params = {
            "json": {
                "columns": columns,
                "filter": filter,
                "primary_table": table.table_name,
                "max_neighbor_count": limit,
                "index_query": query,
                "curate_run_ids": curate_run_ids,
                "curate_layer_name": curate_layer_name,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        ordered_type_list = [OrcaTypeHandle.from_string(table.columns[col].dtype) for col in columns]
        content = [
            [
                (
                    np.array(row[0]),
                    *OrcaClient._deserialize_column_value_list(ordered_type_list, row[1]),
                )
                for row in batch
            ]
            for batch in content
        ]
        # NOTE: This is a temporary adapter as we migrate to the new return type
        # TODO: Remove this once the new return type is fully supported by the server
        return BatchedVectorScanResult_V2(
            extra_col_names=columns,
            data=content,
        )

    def _vector_scan_index_v3(
        table: "TableHandle",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
    ) -> "BatchedScanResult":  # noqa: F821
        """Performs a vector scan index query using the v3 api version.

        NOTE: This version-specific method is used to handle the differences in the response format between api versions,
        and is not called directly by FastAPI.

        :param table: The TableHandle for the table we're querying
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: The flag to drop exact matches
        :param exact_match_threshold: The threshold for exact matches
        :param curate_run_ids: The curate run ids to apply (optional)
        :param curate_layer_name: The curate layer name to apply (optional)
        :return: The response from the scan index query
        """
        from orcalib.batched_scan_result import BatchedScanResult

        url = os.path.join(OrcaClient.BASE_URL, f"v3/db/vector_scan_index/{table.db_name}/{index_name}")
        request_params = {
            "json": {
                "columns": columns,
                "filter": filter,
                "primary_table": table.table_name,
                "max_neighbor_count": limit,
                "index_query": query,
                "curate_run_ids": curate_run_ids,
                "curate_layer_name": curate_layer_name,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
            },
        }
        response = OrcaClient._orca_request("POST", url, request_params)
        content = msgpack.unpackb(response.content, object_hook=decode_ndarray, raw=False)
        print(content.keys(), content["columns"], len(content["data"]))
        column_dict = {
            col_name: OrcaTypeHandle.from_string(col_type) for col_name, col_type in content["columns"].items()
        }
        ordered_type_list = [col_type for col_type in column_dict.values()]
        data = content["data"]
        data = [
            [(*OrcaClient._deserialize_column_value_list(ordered_type_list, row),) for row in batch] for batch in data
        ]

        return BatchedScanResult(column_dict, data)

    vector_index_strategy = {
        "v1": _vector_scan_index_v1,
        "v2": _vector_scan_index_v2,
        "v3": _vector_scan_index_v3,
    }

    @staticmethod
    @default_api_version_key("index.vector_scan")
    def vector_scan_index(
        table: "TableHandle",  # noqa: F821
        index_name: str,
        query: Any,
        limit: int,
        columns: Optional[list[str]] = None,
        filter: Optional[str] = None,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
        api_version: str | None = None,
    ) -> "BatchedScanResult":  # noqa: F821
        """
        Scan a vector index

        :param table: The TableHandle for the table we're querying
        :param index_name: The name of the index
        :param query: The query to apply
        :param limit: The maximum number of rows to return
        :param columns: The columns to return (optional)
        :param filter: The filter to apply (optional)
        :param drop_exact_match: The flag to drop exact matches
        :param exact_match_threshold: The threshold for exact matches
        :param curate_run_ids: The curate run ids to apply (optional)
        :param curate_layer_name: The curate layer name to apply (optional)
        :param api_version: The api version to use (optional)
        :return: The response from the scan index query
        """
        call_correct_version = OrcaClient.vector_index_strategy.get(api_version, None)
        if call_correct_version is None:
            raise ValueError(f"Unsupported vector_scan_index api version: {api_version}")

        return call_correct_version(
            table,
            index_name,
            query,
            limit,
            columns,
            filter,
            drop_exact_match,
            exact_match_threshold,
            curate_run_ids,
            curate_layer_name,
        )

    @staticmethod
    def full_vector_memory_join(
        *,
        db_name: str,
        index_name: str,
        memory_index_name: str,
        num_memories: int,
        query_columns: list[str] | str,
        page_size: int = 100,
        page_index: int = 0,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        shuffle_memories: bool = False,
    ) -> requests.Response:
        """
        Perform a full vector memory join

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param memory_index_name: The name of the memory index
        :param num_memories: The number of memory indexes
        :param query_columns: The columns to query (or a single column)
        :param page_size: The size of the page to return (default: 100)
        :param page_index: The index of the page to return (default: 0)
        :return: The response from the full vector memory join query
        """
        if not isinstance(query_columns, list):
            query_columns = [query_columns]

        url = os.path.join(OrcaClient.BASE_URL, "v1/full_vector_memory_join")
        request_params = {
            "json": {
                "db_name": db_name,
                "index_name": index_name,
                "memory_index_name": memory_index_name,
                "num_memories": num_memories,
                "page_size": page_size,
                "page_index": page_index,
                "query_columns": query_columns,
                "drop_exact_match": drop_exact_match,
                "exact_match_threshold": exact_match_threshold,
                "shuffle_memories": shuffle_memories,
            },
        }

        return OrcaClient._orca_request("POST", url, request_params)

    @staticmethod
    def get_index_values(db_name: str, index_name: str) -> requests.Response:
        """
        Get the values of an index

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The response from the get index values query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/dump_index")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
        }

        return OrcaClient._orca_request("GET", url, request_params)

    @staticmethod
    def get_index_values_paginated(
        db_name: str,
        index_name: str,
        page_index: int = 0,
        page_size: int = 100,
    ) -> requests.Response:
        """
        Get the values of an index paginated

        :param db_name: The name of the database
        :param index_name: The name of the index
        :param page_index: The index of the page to return (default: 0)
        :param page_size: The size of the page to return (default: 100)
        :return: The response from the get index values paginated query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/dump_index_paginated")
        request_params = {
            "params": {
                "db_name": db_name,
                "index_name": index_name,
                "page_index": page_index,
                "page_size": page_size,
            },
        }

        return OrcaClient._orca_request("GET", url, request_params)

    @staticmethod
    def get_index_table(db_name: str, index_name: str) -> str:
        """
        Get the table of an index

        :param db_name: The name of the database
        :param index_name: The name of the index
        :return: The response from the get index table query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/get_index_table")
        request_params = {
            "params": {"db_name": db_name, "index_name": index_name},
        }

        return OrcaClient._orca_request("GET", url, request_params).json()

    @staticmethod
    def run_sql(db_name: str, query: str, params: list[None | int | float | bytes | str] = []) -> list[dict[str, Any]]:
        """
        Run a SQL query

        :param db_name: The name of the database
        :param query: The SQL query
        :param params: The parameters for the query
        :return: The response from the SQL query
        """
        url = os.path.join(OrcaClient.BASE_URL, "experimental/sql")
        request_params = {
            "params": {"db_name": db_name},
            "json": {"query": query, "params": params},
        }

        return OrcaClient._orca_request("POST", url, request_params).json()["rows"]

    @staticmethod
    def encode_roberta(strings: list[str]) -> list[dict[str, Any]]:
        """
        Encode a list of strings using the Roberta model

        :param strings: The list of strings to encode
        :return: The response from the encode query
        """
        url = os.path.join(OrcaClient.BASE_URL, "experimental/encode/roberta")
        request_params = {
            "json": {"strings": strings},
        }

        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def encode_sentence_transformer(strings: list[str]) -> list[dict[str, Any]]:
        """
        Encode a list of strings using the Sentence Transformer model

        :param strings: The list of strings to encode
        :return: The response from the encode query
        """
        url = os.path.join(OrcaClient.BASE_URL, "experimental/encode/sentence_transformer")
        request_params = {
            "json": {"strings": strings},
        }

        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def init_forward_pass(
        db_name: str,
        model_id: str,
        batch_size: int,
        model_version: Optional[str] = None,
        seq_id: Optional[UUID] = None,
        tags: Optional[set[str]] = None,
        metadata: Optional[OrcaMetadataDict] = None,
    ) -> list[int]:
        """
        Initialize a forward pass

        :param db_name: The name of the database
        :param model_id: The id of the model
        :param batch_size: The batch size
        :param model_version: The version of the model (optional)
        :param seq_id: The sequence id for the forward pass (optional)
        :param tags: The tags for the forward pass (optional)
        :param metadata: The metadata for the forward pass (optional)
        :return: The response from the init forward pass query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/init_forward_pass")
        request_params = {
            "json": {
                "db_name": db_name,
                "orca_model_id": model_id,
                "orca_model_version": model_version,
                "batch_size": batch_size,
                "seq_id": seq_id,
                "tags": list(tags),
                "metadata": metadata,
            },
        }
        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def prune_data(db_name: str, model_id: str, filters: list[Any]) -> list[int]:
        """
        Prune data

        :param db_name: The name of the database
        :param model_id: The id of the model
        :param filters: The filters
        :return: The response from the prune data query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/init_forward_pass")
        request_params = {
            "params": {"db_name": db_name, "model_id": model_id},
            "json": {"filters": filters},
        }
        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def record_model_scores(
        db_name: str,
        run_ids: list[int],
        scores: list[float],
    ) -> dict[str, Any]:
        """
        Record model scores

        :param db_name: The name of the database
        :param run_ids: The run ids
        :param scores: The scores
        :return: The response from the record model scores query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/record_scores")
        request_params = {
            "json": {
                "db_name": db_name,
                "run_ids": run_ids,
                "scores": scores,
            },
        }
        return OrcaClient._orca_request("POST", url, request_params).json()

    @staticmethod
    def record_model_input_output(
        db_name: str,
        run_ids: list[int],
        inputs: list[Any],
        outputs: list[Any],
    ) -> dict[str, Any]:
        """
        Record model input output

        :param db_name: The name of the database
        :param run_ids: The run ids
        :param inputs: The inputs
        :param outputs: The outputs
        :return: The response from the record model input output query
        """
        url = os.path.join(OrcaClient.BASE_URL, "v1/curate/record_model_in_out")
        request_params = {
            "json": {
                "db_name": db_name,
                "run_ids": run_ids,
                "inputs": inputs,
                "outputs": outputs,
            },
        }
        return OrcaClient._orca_request("POST", url, request_params).json()
