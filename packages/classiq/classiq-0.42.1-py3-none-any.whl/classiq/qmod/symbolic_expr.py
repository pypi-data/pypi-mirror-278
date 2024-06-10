from __future__ import annotations

import ast
from typing import Any


class Symbolic:
    def __init__(self, expr: str) -> None:
        self._expr = expr

    def __str__(self) -> str:
        return self._expr

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        try:
            return bool(ast.literal_eval(self._expr))
        except ValueError:
            raise TypeError(
                f"Symbolic expression {self._expr!r} cannot be converted to bool"
            ) from None


class SymbolicExpr(Symbolic):
    def __init__(self, expr: str) -> None:
        super().__init__(expr)

    @staticmethod
    def _binary_op(lhs: Any, rhs: Any, op: str) -> SymbolicExpr:
        if not isinstance(lhs, (SymbolicExpr, int, float, bool)):
            raise TypeError(f"Invalid lhs argument {lhs!r} for binary operation {op!r}")

        if not isinstance(rhs, (SymbolicExpr, int, float, bool)):
            raise TypeError(f"Invalid lhs argument {rhs!r} for binary operation {op!r}")

        lhs_str = str(lhs) if isinstance(lhs, (int, float, bool)) else f"({lhs})"
        rhs_str = str(rhs) if isinstance(rhs, (int, float, bool)) else f"({rhs})"

        return SymbolicExpr(f"{lhs_str} {op} {rhs_str}")

    @staticmethod
    def _unary_op(arg: Any, op: str) -> SymbolicExpr:
        if not isinstance(arg, (SymbolicExpr, int, float, bool)):
            raise TypeError(f"Invalid argument {arg!r} for unary operation {op!r}")

        return SymbolicExpr(f"{op}({arg})")

    def __add__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "+")

    def __sub__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "-")

    def __mul__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "*")

    def __truediv__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "/")

    def __floordiv__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "//")

    def __mod__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "%")

    def __pow__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "**")

    def __lshift__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "<<")

    def __rshift__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, ">>")

    def __and__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "&")

    def __xor__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "^")

    def __or__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "|")

    def __radd__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "+")

    def __rsub__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "-")

    def __rmul__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "*")

    def __rtruediv__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "/")

    def __rfloordiv__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "//")

    def __rmod__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "%")

    def __rpow__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "**")

    def __rlshift__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "<<")

    def __rrshift__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, ">>")

    def __rand__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "&")

    def __rxor__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "^")

    def __ror__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(other, self, "|")

    def __lt__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "<")

    def __le__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, "<=")

    def __eq__(self, other: Any) -> SymbolicEquality:  # type: ignore[override]
        return SymbolicEquality(self, other)

    def __ne__(self, other: Any) -> SymbolicExpr:  # type: ignore[override]
        return SymbolicExpr._binary_op(self, other, "!=")

    def __gt__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, ">")

    def __ge__(self, other: Any) -> SymbolicExpr:
        return SymbolicExpr._binary_op(self, other, ">=")

    def __neg__(self) -> SymbolicExpr:
        return SymbolicExpr._unary_op(self, "-")

    def __pos__(self) -> SymbolicExpr:
        return SymbolicExpr._unary_op(self, "+")

    def __abs__(self) -> SymbolicExpr:
        return SymbolicExpr._unary_op(self, "abs")

    def __invert__(self) -> SymbolicExpr:
        return SymbolicExpr._unary_op(self, "~")


class SymbolicEquality(SymbolicExpr):
    def __init__(self, lhs: Any, rhs: Any) -> None:
        expr = SymbolicExpr._binary_op(lhs, rhs, "==")._expr
        super().__init__(expr)
        self.lhs = lhs
        self.rhs = rhs
