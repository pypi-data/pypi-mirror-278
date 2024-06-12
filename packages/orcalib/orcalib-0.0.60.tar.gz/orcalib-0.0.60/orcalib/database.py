from typing import Any, Optional

import orjson
import pandas
import requests
import torch
from orca_common import EmbeddingModel, TableCreateMode
from tqdm.auto import trange
from transformers import AutoModel, AutoTokenizer

from orcalib.client import OrcaClient
from orcalib.constants import EXACT_MATCH_THRESHOLD
from orcalib.exceptions import OrcaException
from orcalib.index_handle import IndexHandle
from orcalib.index_query import DefaultIndexQuery, VectorIndexQuery
from orcalib.orca_types import OrcaTypeHandle
from orcalib.table import TableHandle


class OrcaDatabase:
    name: str
    _default_instance = None

    def __init__(self, name: str):
        """
        Create a new OrcaDatabase object

        :param name: name of the database
        """
        self.name = name
        OrcaClient.create_database(name)
        self.tables = OrcaClient.list_tables(name)
        self.tokenizer = None
        self.model = None

    def _load_model_and_tokenizer(self) -> tuple[AutoTokenizer, AutoModel]:
        """
        Load the default model and tokenizer

        :return: tokenizer, model

        NOTE: This method should not be called directly. It is used internally by the library to load the default model and tokenizer.
        """
        if self.tokenizer is None or self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
            self.model = AutoModel.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")  # .to("cuda")
        return self.tokenizer, self.model

    def __contains__(self, table_name: str) -> bool:
        """
        Check if a table exists in the database

        :param table_name: name of the table
        """
        return table_name in self.tables

    def __getitem__(self, table_name: str) -> TableHandle:
        """
        Get a handle to a table by name

        :param table_name: name of the table
        :return: TableHandle object
        """
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} not found in database {self.name}")
        return TableHandle(self.name, table_name)

    def get_table(self, table_name: str) -> TableHandle:
        """
        Get a handle to a table by name

        :param table_name: name of the table
        :return: TableHandle object
        """
        return self.__getitem__(table_name)

    @classmethod
    def get_default_instance(cls) -> "OrcaDatabase":
        """
        Get the default instance of OrcaDatabase

        :return: OrcaDatabase object
        """
        if cls._default_instance is None:
            cls._default_instance = cls("default")
        return cls._default_instance

    @staticmethod
    def list_databases() -> list[str]:
        """
        List all databases on the server

        :return: list of database names
        """
        return OrcaClient.list_databases()

    @classmethod
    def is_server_up(cls) -> bool:
        """
        Check if the server is up and running

        :return: True if server is up, False otherwise
        """
        try:
            cls.list_databases()
            return True
        except Exception:
            return False

    @classmethod
    def drop_database(cls, db: "str | OrcaDatabase", ignore_db_not_found: bool = False) -> None:
        """
        Drops a database by name or using the OrcaDatabase object

        :param db: name of the database or OrcaDatabase object to drop
        :param ignore_db_not_found: if True, ignore error if database doesn't exist and continue with the operation anyway (default: False)
        """
        db_name = db.name if isinstance(db, OrcaDatabase) else db
        OrcaClient.drop_database(db_name, ignore_db_not_found)

    @classmethod
    def exists(cls, db: "str | OrcaDatabase") -> bool:
        """
        Checks if a database exists by name or using the OrcaDatabase object

        :param db: name of the database or OrcaDatabase object
        :return: True if database exists, False otherwise
        """
        db_name = db.name if isinstance(db, OrcaDatabase) else db
        return OrcaClient.database_exists(db_name)

    @staticmethod
    def restore(target_db_name: str, backup_name: str, checksum: str | None = None) -> "OrcaDatabase":
        """Restore a backup into a target database

        CAREFUL: this will overwrite the target database if it already exists

        :param target_db_name: name of database that backup will be restored into (will be created if it doesn't exist)
        :param backup_name: name of the backup to restore
        :param checksum: optionally the checksum for the backup
        :return: restored database
        """
        OrcaClient.restore_backup(target_db_name, backup_name, checksum=checksum)
        return OrcaDatabase(target_db_name)

    def list_tables(self) -> list[str]:
        """
        List all tables in the database

        :return: list of table names
        """
        return OrcaClient.list_tables(self.name)

    def backup(self) -> tuple[str, str]:
        """Create a backup of the database

        :return: tuple containing name of the backup and checksum
        """
        res = OrcaClient.create_backup(self.name)
        return res["backup_name"], res["checksum"]

    @staticmethod
    def download_backup(backup_file_name: str) -> requests.Response:
        """Downloads the backup of the database

        :param backup_file_name: name of the backup file
        :return: backed up file
        """
        return OrcaClient.download_backup(backup_file_name)

    @staticmethod
    def upload_backup(file_path: str) -> requests.Response:
        """Uploads tar file of the database

        :param file_path: path to the tar file
        :return: Upload response
        """
        return OrcaClient.upload_backup(file_path)

    @staticmethod
    def delete_backup(backup_file_name: str) -> requests.Response:
        """
        Delete backup file

        :param backup_file_name: name of the backup file
        :return: delete response
        """
        return OrcaClient.delete_backup(backup_file_name)

    def default_vectorize(self, text: str) -> list[float]:
        """
        Vectorize text using the default model

        :param text: text to vectorize
        :return: list of floats
        """
        tokenizer, model = self._load_model_and_tokenizer()
        encoded_input = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True)  # .to("cuda")
        output = model(**encoded_input)
        return output.pooler_output.tolist()[0]

    def create_table(
        self,
        table_name: str,
        if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
        **columns: OrcaTypeHandle,
    ) -> TableHandle:
        """
        Create a table in the database

        :param table_name: name of the table
        :param if_table_exists: what to do if the table already exists
        :param columns: column names and types
        :return: TableHandle object
        """
        # We will deal with the case where the table already exists in server.
        self._create_table(table_name, if_table_exists, **columns)
        return self.get_table(table_name)

    def _create_table(
        self,
        table_name: str,
        if_table_exists: TableCreateMode,
        **columns: OrcaTypeHandle,
    ) -> TableHandle:
        """
        Create a table in the database

        :param table_name: name of the table
        :param if_table_exists: what to do if the table already exists
        :param columns: column names and types
        :return: TableHandle object

        NOTE: This method should not be called directly. It is used internally by the library to create a table in the database.
        """
        table_schema = []
        for column_name, column_type in columns.items():
            table_schema.append(
                {
                    "name": column_name,
                    "dtype": column_type.full_name,
                    "notnull": column_type._notnull,
                    "unique": column_type._unique,
                }
            )
        OrcaClient.create_table(self.name, table_name, table_schema, if_table_exists)
        self.tables.append(table_name)
        return TableHandle(self.name, table_name)

    def _create_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        ann_index_type: str = "hnswlib",
        error_if_exists: bool = True,
        api_version: str | None = None,
        embedding_model: EmbeddingModel | None = None,
    ) -> IndexHandle:
        """
        Create an index on a table

        :param index_name: name of the index
        :param table_name: name of the table
        :param column: name of the column
        :param index_type: type of the index
        :param error_if_exists: if True, raise an error if the index already exists (default: True)
        :param api_version: API version to use (default: None)
        :param embedding_model: embedding model to use (default: None) (roberta, sentence_transformer) (only for text and document indexes)

        NOTE: This method should not be called directly. It is used internally by the library to create an index on a table.

        embedding_model defaults to sentence_transformer model if None is provided and it can only be used on text and document indexes.
        """
        try:
            print(f"Creating index {index_name} of type {index_type} on table {table_name} with column {column}")
            return OrcaClient.create_index(
                self.name,
                index_name,
                table_name,
                column,
                index_type,
                ann_index_type,
                api_version=api_version,
                embedding_model=embedding_model,
            )
        except OrcaException as e:
            if error_if_exists:
                raise e

    def get_index_status(self, index_name: str) -> dict[str, Any]:
        """
        Get the status of an index

        :param index_name: name of the index
        :return: status of the index
        """
        try:
            return OrcaClient.get_index_status(db_name=self.name, index_name=index_name)
        except OrcaException as e:
            raise e

    def get_index(self, index_name: str) -> IndexHandle:
        """
        Get a handle to an index by name

        :param index_name: name of the index
        :return: IndexHandle object
        """
        response = OrcaClient.get_index(self.name, index_name)
        return response

    def create_vector_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        ann_index_type: str = "hnswlib",
        error_if_exists: bool = True,
        api_version: str | None = None,
    ) -> IndexHandle:
        """
        Create a vector index on a table

        :param index_name: name of the index
        :param table_name: name of the table
        :param column: name of the column
        :param error_if_exists: if True, raise an error if the index already exists (default: True)
        :param api_version: API version to use (default: None)
        """
        return self._create_index(
            index_name, table_name, column, "vector", ann_index_type, error_if_exists, api_version=api_version
        )

    def create_document_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        ann_index_type: str = "hnswlib",
        error_if_exists: bool = True,
        embedding_model: EmbeddingModel | None = None,
        api_version: str | None = None,
    ) -> IndexHandle:
        """
        Create a document index on a table

        :param index_name: name of the index
        :param table_name: name of the table
        :param column: name of the column
        :param error_if_exists: if True, raise an error if the index already exists (default: True)
        :param embedding_model: embedding model to use (default: None) (roberta, sentence_transformer)
        :param api_version: API version to use (default: None)

        NOTE: embedding_model defaults to sentence_transformer model if None is provided.
        """
        return self._create_index(
            index_name,
            table_name,
            column,
            "document",
            ann_index_type,
            error_if_exists,
            embedding_model=embedding_model,
            api_version=api_version,
        )

    def create_text_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        ann_index_type: str = "hnswlib",
        error_if_exists: bool = True,
        embedding_model: EmbeddingModel | None = None,
        api_version: str | None = None,
    ) -> IndexHandle:
        """
        Create a text index on a table

        :param index_name: name of the index
        :param table_name: name of the table
        :param column: name of the column
        :param error_if_exists: if True, raise an error if the index already exists (default: True)
        :param embedding_model: embedding model to use (default: None) (roberta, sentence_transformer)
        :param api_version: API version to use (default: None)

        NOTE: embedding_model defaults to sentence_transformer model if None is provided.
        """
        return self._create_index(
            index_name,
            table_name,
            column,
            "text",
            ann_index_type,
            error_if_exists,
            embedding_model=embedding_model,
            api_version=api_version,
        )

    def create_btree_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        ann_index_type: str = "hnswlib",
        error_if_exists: bool = True,
        api_version: str | None = None,
    ) -> IndexHandle:
        """
        Create a btree index on a table

        :param index_name: name of the index
        :param table_name: name of the table
        :param column: name of the column
        :param error_if_exists: if True, raise an error if the index already exists (default: True)
        :param api_version: API version to use (default: None)
        """
        return self._create_index(
            index_name, table_name, column, "btree", ann_index_type, error_if_exists, api_version=api_version
        )

    def drop_index(self, index_name: str, error_if_not_exists: bool = True) -> None:
        """
        Drop an index from the database

        :param index_name: name of the index
        :param error_if_not_exists: if True, raise an error if the index doesn't exist (default: True)
        """
        try:
            OrcaClient.drop_index(self.name, index_name)
        except OrcaException as e:
            if error_if_not_exists:
                raise e

    def drop_table(self, table_name: str, error_if_not_exists: bool = True) -> None:
        """
        Drop a table from the database

        :param table_name: name of the table
        :param error_if_not_exists: if True, raise an error if the table doesn't exist (default: True)
        """
        OrcaClient.drop_table(self.name, table_name, error_if_not_exists)
        if table_name in self.tables:
            self.tables.remove(table_name)

    def search_memory(
        self,
        index_name: str,
        query: list[float],
        limit: int,
        columns: Optional[list[str]] = None,
    ) -> list[tuple[list[float], Any]]:
        """
        Search the memory for a given query

        :param index_name: name of the index
        :param query: query vector
        :param limit: maximum number of results to return
        :param columns: optional list of columns to return in the result (default: None)
        :return: list of tuples containing (vector, extra)
        """
        res = OrcaClient.scan_index(
            self,
            index_name,
            query,
            limit,
            columns,
        )
        return res

    def scan_index(
        self,
        index_name: str,
        query: Any,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> DefaultIndexQuery:
        """
        Scan an index for a given query

        :param index_name: name of the index
        :param query: query
        :return: DefaultIndexQuery object
        """
        return DefaultIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(index_name),
            index=index_name,
            index_query=query,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
        )

    def vector_scan_index(
        self,
        index_name: str,
        query: Any,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
    ) -> VectorIndexQuery:
        """
        Scan an index for a given query

        :param index_name: name of the index
        :param query: query
        :return: VectorIndexQuery object
        """
        return VectorIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(index_name),
            index=index_name,
            index_query=query,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
        )

    def full_vector_memory_join(
        self,
        *,
        index_name: str,
        memory_index_name: str,
        num_memories: int,
        query_columns: list[str],
        page_index: int,
        page_size: int,
        drop_exact_match: bool = False,
        exact_match_threshold: float = EXACT_MATCH_THRESHOLD,
        shuffle_memories: bool = False,
    ) -> dict[str, list[tuple[list[float], Any]]]:
        """
        Join a vector index with a memory index

        :param index_name: name of the index
        :param memory_index_name: name of the memory index
        :param num_memories: number of memories to join
        :param query_columns: list of columns to return
        :param page_index: page index
        :param page_size: page size
        :return: dictionary containing the joined vectors and extra columns
        """
        res = OrcaClient.full_vector_memory_join(
            db_name=self.name,
            index_name=index_name,
            memory_index_name=memory_index_name,
            num_memories=num_memories,
            query_columns=query_columns,
            page_index=page_index,
            page_size=page_size,
            drop_exact_match=drop_exact_match,
            exact_match_threshold=exact_match_threshold,
            shuffle_memories=shuffle_memories,
        )

        return orjson.loads(res.text)

    def _get_index_values(self, index_name: str) -> dict[int, list[float]]:
        """
        Get all values for an index

        :param index_name: name of the index
        :return: dictionary containing the index values

        NOTE: This method should not be called directly. It is used internally by the library to get all values for an index.
        """
        res = OrcaClient.get_index_values(self.name, index_name).json()
        return {int(k): v for k, v in res.items()}

    def _get_index_values_paginated(
        self,
        index_name: str,
        page_size: int = 1000,
    ) -> dict[int, list[float]]:
        """
        Get all values for an index, paginated

        :param index_name: name of the index
        :param page_size: page size (default: 1000)
        :return: dictionary containing the index values

        NOTE: This method should not be called directly. It is used internally by the library to get all values for an index.
        """
        page_index = 0

        result = {}

        res = OrcaClient.get_index_values_paginated(
            self.name, index_name, page_index=page_index, page_size=page_size
        ).json()

        num_pages = res["num_pages"]

        for v in res["items"]:
            result[int(v[0])] = v[1]

        if num_pages > 1:
            print(f"Fetching vectors for index {index_name} ({num_pages} pages)")

            for page_index in trange(1, num_pages):
                res = OrcaClient.get_index_values_paginated(
                    self.name, index_name, page_index=page_index, page_size=page_size
                ).json()

                for v in res["items"]:
                    result[int(v[0])] = v[1]

        print(f"Finished fetching vectors for index {index_name} ({num_pages} pages)")

        return result

    def _get_index_table(self, index_name: str) -> TableHandle:
        """
        Get the table associated with an index

        :param index_name: name of the index
        :return: TableHandle object

        NOTE: This method should not be called directly. It is used internally by the library to get the table associated with an index.
        """
        return TableHandle(self.name, OrcaClient.get_index_table(self.name, index_name))

    def memory_layer(self, index_name: str) -> torch.nn.Module:
        """
        Create a memory layer for the index

        :param index_name: name of the index
        :return: torch.nn.Module object
        """
        return torch.nn.Sequential(
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
        )

    def wrap_hf_model(self, index_name: str, model_name: str):
        pass

    def query(self, query: str, params: list[None | int | float | bytes | str] = []) -> pandas.DataFrame:
        """Send a read query to the database

        This cannot be used for inserting, updating, or deleting data.

        :param query: SQL query to run
        :param params: optional values to pass to a parametrized query (default: [])
        :return: pandas DataFrame containing the results
        """
        df = pandas.DataFrame(OrcaClient.run_sql(self.name, query, params))
        return df

    def record_model_scores(self, run_ids: list[int] | int, scores: list[float] | float) -> None:
        """
        Record model scores in the database

        :param run_ids: list of run IDs
        :param scores: list of scores
        """
        if isinstance(run_ids, int):
            run_ids = [run_ids]
            assert isinstance(scores, float), "Only a single score is allowed if a single run_id is provided"
            scores = [scores]
        assert isinstance(scores, list)
        OrcaClient.record_model_scores(self.name, run_ids, scores)

    def record_model_input_output(
        self, run_ids: list[int] | int, inputs: list[Any] | Any, outputs: list[Any] | Any
    ) -> None:
        """
        Record model input/output in the database

        :param run_ids: list of run IDs
        :param inputs: list of inputs
        :param outputs: list of outputs
        """
        if isinstance(run_ids, int):
            run_ids = [run_ids]
            assert not isinstance(inputs, list) and not isinstance(
                outputs, list
            ), "Only a single input/output is allowed if a single run_id is provided"
            inputs = [inputs]
            outputs = [outputs]
        OrcaClient.record_model_input_output(self.name, run_ids, inputs, outputs)

    def __str__(self) -> str:
        """
        String representation of the database

        :return: String representation
        """
        return f"OrcaDatabase({self.name}) - Tables: {', '.join(self.tables)}"

    def __repr__(self) -> str:
        """
        String representation of the database

        :return: String representation
        """
        return self.__str__()


def with_default_database_method(method: Any) -> Any:
    """
    Decorator to add the default database as the first argument to a method.

    :param method: method to decorate
    :return: decorated method
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper function

        :param args: arguments
        :param kwargs: keyword arguments
        """
        default_database = OrcaDatabase.get_default_instance()
        return method(default_database, *args, **kwargs)

    return wrapper
