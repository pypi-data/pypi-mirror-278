import csv
import json
import pickle
from abc import ABC
from collections import Counter
from typing import Any, cast
from urllib.request import urlopen

import numpy as np
import pandas
import pyarrow
from tqdm.auto import trange
from orca_common import ColumnName, RowDict

from orcalib.database import OrcaDatabase
from orcalib.orca_types import (
    BoolT,
    DocumentT,
    DocumentTypeHandle,
    FloatT,
    IntT,
    OrcaTypeHandle,
    TextT,
    VectorT,
)


class FileIngestorBase(ABC):
    """
    Base class for file ingestors
    """

    def __init__(
        self,
        db: OrcaDatabase,
        table_name: str,
        dataset: list[dict[str, Any]],
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset: Dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        if auto_table and not replace:
            assert table_name not in db.tables, "Table already exists - can't use auto_table"
        self._db = db
        self._table_name = table_name
        self._dataset = dataset
        self._auto_table = auto_table
        self._replace = replace

    def _schema_from_dataset(self, sample: RowDict) -> dict[ColumnName, OrcaTypeHandle]:
        """
        Infer schema from the dataset

        :param sample: Sample row
        :return: Schema
        """
        schema = {}

        for col in sample.keys():
            if isinstance(sample[col], str):
                if len(sample[col]) > 100:
                    schema[col] = DocumentT
                else:
                    schema[col] = TextT
            elif isinstance(sample[col], int):
                schema[col] = IntT
            elif isinstance(sample[col], float):
                schema[col] = FloatT
            elif isinstance(sample[col], bool):
                schema[col] = BoolT
            elif isinstance(sample[col], list):
                schema[col] = VectorT[len(sample[col])]
            else:
                raise ValueError(f"Can't infer type for column {col}")
        return schema

    def _create_table(self) -> Any:
        """
        Create table

        :return: Table

        NOTE: This method should not be called directly. It is used internally.
        """
        if self._replace and self._auto_table and self._table_name in self._db.tables:
            self._db.drop_table(self._table_name)
        schema = self._schema_from_dataset(self._dataset[0])
        print(f"Creating table {self._table_name} with schema {schema}")
        return self._db.create_table(self._table_name, **schema)

    def dataframe_to_list(self, df: pandas.DataFrame) -> list[dict]:
        """
        Convert dataframe to list of dictionaries

        :param df: Dataframe
        :return: List of dictionaries
        """
        dataset = []
        columns = df.columns.values.tolist()
        for i in trange(len(df)):
            curr_row = df.iloc[i].tolist()
            for j in range(len(curr_row)):
                # Process vectors and numpy integers
                if isinstance(curr_row[j], str) and curr_row[j][0] == "[":
                    if curr_row[j][-1] != "]":
                        raise Exception("Incorrectly formatted list in CSV file")
                    curr_row[j] = [float(x.strip()) for x in curr_row[j][1 : len(curr_row[j]) - 1].split(",")]
                elif isinstance(curr_row[j], np.integer):
                    curr_row[j] = int(curr_row[j])
                elif isinstance(curr_row[j], np.ndarray):
                    curr_row[j] = list(curr_row[j])
            dataset.append(dict(zip(columns, curr_row)))
        return dataset

    def run(self, only_create_table: bool = False, skip_create_table: bool = False) -> Any:
        """
        Run ingestor

        :param only_create_table: Only create table and don't insert data (default: False)
        :param skip_create_table: Skip creating table if it doesn't exist (default: False)
        :return: Table
        """
        if self._auto_table and not skip_create_table:
            table = self._create_table()
        else:
            table = self._db[self._table_name]
            # Convert file schema to hashable format with strings so we can use Counter
            file_col_types = []
            for file_col in self._schema_from_dataset(self._dataset[0]).values():
                if isinstance(file_col, DocumentTypeHandle):
                    file_col_types.append("text")
                else:
                    file_col_types.append(file_col.full_name)
            # Do the same for the schema of the existing table
            curr_col_types = []
            for table_col in table.columns:
                col_type = table.columns[table_col].dtype
                # Just like above, we treat text and document as the same type
                if col_type == "document":
                    curr_col_types.append("text")
                else:
                    curr_col_types.append(col_type)
            # If the file schema doesn't match the existing table schema,
            # We want to throw an exception.
            if self._auto_table and Counter(file_col_types) != Counter(curr_col_types):
                raise Exception("File schema does not match table schema")
        temp = cast(
            list[dict[str, Any]],
            list(self._dataset),
        )
        if not only_create_table:
            table.insert(*temp)
        return table


class PickleIngestor(FileIngestorBase):
    """
    Ingestor for pickle files
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset_path: Path to the dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                dataset = pickle.load(f)
        else:
            with open(dataset_path, "rb") as f:
                dataset = pickle.load(f)
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class JSONIngestor(FileIngestorBase):
    """
    Ingestor for JSON files
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset_path: Path to the dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                json_dataset = json.load(f)
        else:
            with open(dataset_path, "r") as f:
                json_dataset = json.load(f)
        if isinstance(json_dataset, list):
            dataset = json_dataset
        elif "data" in json_dataset:
            dataset = json_dataset["data"]
        else:
            raise Exception("Incorrectly formatted JSON file")
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class JSONLIngestor(FileIngestorBase):
    """
    Ingestor for JSONL files
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset_path: Path to the dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        dataset = []
        if dataset_path[0:4] == "http":
            with urlopen(dataset_path) as f:
                for line in f:
                    dataset.append(json.loads(line))
        else:
            with open(dataset_path, "r") as f:
                for line in f:
                    dataset.append(json.loads(line))
        FileIngestorBase.__init__(self, db, table_name, dataset, auto_table, replace)


class CSVIngestor(FileIngestorBase):
    """
    Ingestor for CSV files
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset_path: Path to the dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        df = pandas.read_csv(dataset_path)
        FileIngestorBase.__init__(self, db, table_name, self.dataframe_to_list(df), auto_table, replace)


class ParquetIngestor(FileIngestorBase):
    """
    Ingestor for Parquet files
    """

    def __init__(
        self,
        db: OrcaDatabase,
        *,
        table_name: str,
        dataset_path: str,
        auto_table: bool = False,
        replace: bool = False,
    ):
        """
        :param db: Database
        :param table_name: Name of the table
        :param dataset_path: Path to the dataset
        :param auto_table: automatically create table if it doesn't exist (default: False)
        :param replace: replace table if it already exists (default: False)
        """
        df = pyarrow.parquet.read_table(dataset_path).to_pandas()
        FileIngestorBase.__init__(self, db, table_name, self.dataframe_to_list(df), auto_table, replace)
