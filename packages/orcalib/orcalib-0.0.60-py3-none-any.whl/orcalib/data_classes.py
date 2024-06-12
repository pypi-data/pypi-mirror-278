from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class ColumnSpec:
    """Specification for a column in a table."""

    name: str
    notnull: bool
    unique: bool
    dtype: str


@dataclass
class VectorScanResult:
    """Result of a vector scan."""

    vec: np.ndarray
    extra: list[Any]

    def __str__(self) -> str:
        """
        Return a string representation of this vector scan result.

        :return: String representation
        """
        return f"VectorScanResult({','.join([str(item) for item in self.extra])})"

    def __repr__(self) -> str:
        """
        Return a string representation of this vector scan result.

        :return: String representation
        """
        return self.__str__()
