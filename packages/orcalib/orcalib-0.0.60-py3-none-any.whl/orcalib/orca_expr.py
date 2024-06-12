from typing import Any, Union

from orca_common import Order

LiteralType = Union[int, str, float, bool]


OperableType = Union[LiteralType, "Operable"]


class Operable:
    def __eq__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$EQ", (self, value))

    def __ne__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$NEQ", (self, value))

    def __lt__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$LT", (self, value))

    def __le__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$LTE", (self, value))

    def __gt__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$GT", (self, value))

    def __ge__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$GTE", (self, value))

    def __add__(self, value: OperableType) -> Any:
        """
        :param value: Value to add
        """
        return OrcaExpr("$ADD", (self, value))

    def __radd__(self, value: OperableType) -> Any:
        """
        :param value: Value to add
        """
        return OrcaExpr("$ADD", (value, self))

    def __sub__(self, value: OperableType) -> Any:
        """
        :param value: Value to subtract
        """
        return OrcaExpr("$SUB", (self, value))

    def __rsub__(self, value: OperableType) -> Any:
        """
        :param value: Value to subtract
        """
        return OrcaExpr("$SUB", (value, self))

    def __mul__(self, value: OperableType) -> Any:
        """
        :param value: Value to multiply
        """
        return OrcaExpr("$MUL", (self, value))

    def __rmul__(self, value: OperableType) -> Any:
        """
        :param value: Value to multiply
        """
        return OrcaExpr("$MUL", (value, self))

    def __truediv__(self, value: OperableType) -> Any:
        """
        :param value: Value to divide
        """
        return OrcaExpr("$DIV", (self, value))

    def __rtruediv__(self, value: OperableType) -> Any:
        """
        :param value: Value to divide
        """
        return OrcaExpr("$DIV", (value, self))

    def __and__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$&", (self, value))

    def __or__(self, value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        return OrcaExpr("$|", (self, value))

    def _in(self, *value: OperableType) -> Any:
        """
        :param value: Value to compare with
        """
        if len(value) == 1 and isinstance(value[0], OrcaExpr) and value[0].op == "$ARRAY":
            val = value[0]
        else:
            val = OrcaExpr("$ARRAY", value)
        return OrcaExpr("$CONTAINS", (val, self))


class OrcaExpr(Operable):
    """Orca expression class. This class is used to represent expressions in Orca."""

    op: str
    args: tuple[OperableType, ...]

    def __init__(self, op: str, args: tuple[OperableType, ...]):
        """
        :param op: The operation to perform
        :param args: The arguments to the operation
        """
        self.op = op
        self.args = args

    def _serialize_arg(self, arg: OperableType) -> Union[str, dict[str, Union[str, list]]]:
        """
        Serialize the argument to a format that can be sent to the server

        :param arg: The argument to serialize

        NOTE: This method should not be called directly. It is used internally.
        """
        if isinstance(arg, OrcaExpr):
            return arg.as_serializable()
        elif isinstance(arg, ColumnHandle):
            return arg.as_serializable()
        elif isinstance(arg, str) or isinstance(arg, float) or isinstance(arg, int) or isinstance(arg, bool):
            return f"{arg}"
        else:
            raise ValueError(f"{arg} is not a valid value for arg")

    def as_serializable(self) -> dict[str, Union[str, list]]:
        """
        Serialize the expression to a format that can be sent to the server
        """
        return {
            "op": self.op,
            "args": [self._serialize_arg(arg) for arg in self.args],
        }

    def __repr__(self) -> str:
        """
        Return a string representation of this expression
        """
        return f"OrcaExpr<{self.op}({', '.join(repr(arg) for arg in self.args)})>"


class ColumnHandle(Operable):
    """Handle for a column in a table."""

    def __init__(self, db_name: str, table_name: str, column_name: str):
        """
        :param db_name: Name of the database
        :param table_name: Name of the table
        :param column_name: Name of the column
        """
        self.db_name = db_name
        self.table_name = table_name
        self.column_name = column_name

    def __repr__(self) -> str:
        """
        Return a string representation of this column handle
        """
        return f"ColumnHandle<{self.table_name}.{self.column_name}>"

    def as_serializable(self) -> str:
        """
        Serialize the column handle to a format that can be sent to the server
        """
        return f"{self.table_name}.{self.column_name}"

    @property
    def ASC(self) -> tuple[str, Order]:
        """Return a tuple of the column name and the ascending order.
        This can be used with TableHandle.order_by() to sort this column in ascending order
        """
        return (self.column_name, Order.ASCENDING)

    @property
    def DESC(self) -> tuple[str, Order]:
        """Return a tuple of the column name and the descending order.
        This can be used with TableHandle.order_by() to sort this column in descending order
        """
        return (self.column_name, Order.DESCENDING)
