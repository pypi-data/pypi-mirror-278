import copy
from enum import Enum
from typing import Optional

from munud.utils import C_HEX_TOKEN

BYTE_SIZE = 8


class Operators(Enum):
    LSHIFT = "<<"
    RSHIFT = ">>"
    AND = "&"
    OR = "|"


class Var:
    def __init__(
        self,
        name,
        slice: Optional[int] = None,
        history: list[tuple[Operators, int]] = [],
    ):
        self.name = name
        self.history = history
        self.slice = slice

    def __lshift__(self, n) -> "Var":

        assert isinstance(n, int)

        new_history = copy.copy(self.history)

        new_history.append((Operators.LSHIFT, n))
        return Var(self.name, slice=self.slice, history=new_history)

    def __rshift__(self, n) -> "Var":
        assert isinstance(n, int)

        new_history = copy.copy(self.history)

        new_history.append((Operators.RSHIFT, n))
        return Var(self.name, slice=self.slice, history=new_history)

    def __getitem__(self, key) -> "Var":
        self.slice = key
        return self

    def __and__(self, n) -> "Var":
        assert isinstance(n, int)
        new_history = copy.copy(self.history)

        new_history.append((Operators.AND, n))
        return Var(self.name, slice=self.slice, history=new_history)

    def __or__(self, n) -> "Var":
        assert isinstance(n, int)
        new_history = copy.copy(self.history)

        new_history.append((Operators.OR, n))
        return Var(self.name, slice=self.slice, history=new_history)

    def __str__(self):
        return f"{self.history}"


class WriteOperation:
    def __init__(self, var_out: Var, var_in: Var, or_write: bool = False):
        self.var_out = var_out
        self.var_in = var_in
        self.or_write = or_write

    def run_expr(self, value) -> int:

        for op, v in self.var_in.history:
            if op == Operators.AND:
                value &= v
            elif op == Operators.OR:
                value |= v
            elif op == Operators.LSHIFT:
                value <<= v
            elif op == Operators.RSHIFT:
                value >>= v

        return value

    def to_c_expr(self):
        str_repr = f"{self.var_in.name}"

        for op, v in self.var_in.history:
            if op == Operators.AND:
                str_repr = f"({str_repr} {op.value} {C_HEX_TOKEN(v)})"
            else:
                str_repr = f"({str_repr} {op.value} {v})"

        if self.var_in.history:
            str_repr = str_repr[1:-1]

        write_op = "|=" if self.or_write else "="

        if self.var_out.slice is None:
            return f"{self.var_out.name} {write_op} {str_repr}"
        else:
            return f"{self.var_out.name}[{self.var_out.slice}] {write_op} {str_repr}"

    def __str__(self):
        return f"WRITE : \t{self.to_c_expr()}"


class ReadOperation:
    def __init__(self, var_in: Var):
        self.var_in = var_in

    def run_expr(self, _bytes: bytes) -> int:

        assert self.var_in.slice is not None, f"{self.var_in} slice is None"

        result = _bytes[self.var_in.slice]

        for op, v in self.var_in.history:
            if op == Operators.AND:
                result &= v
            elif op == Operators.OR:
                result |= v
            elif op == Operators.LSHIFT:
                result <<= v
            elif op == Operators.RSHIFT:
                result >>= v

        return result

    def to_c_expr(self):
        str_repr = f"{self.var_in.name}[{self.var_in.slice}]"

        for op, v in self.var_in.history:
            if op == Operators.AND:
                str_repr = f"({str_repr} {op.value} {C_HEX_TOKEN(v)})"
            else:
                str_repr = f"({str_repr} {op.value} {v})"

        if self.var_in.history:
            str_repr = str_repr[1:-1]

        return f"return {str_repr}"

    def __str__(self):
        return f"READ  : \tout = {self.to_c_expr()}"


class BundeledReadOperation(ReadOperation):
    def __init__(self, read_ops: list[ReadOperation]):
        self.read_ops = read_ops

    def run_expr(self, _bytes: bytes):

        result = 0

        for r_op in self.read_ops:

            assert r_op.var_in.slice is not None, f"{self.var_in} slice is None"

            part_result = _bytes[r_op.var_in.slice]

            for op, v in r_op.var_in.history:
                if op == Operators.AND:
                    part_result &= v
                elif op == Operators.OR:
                    part_result |= v
                elif op == Operators.LSHIFT:
                    part_result <<= v
                elif op == Operators.RSHIFT:
                    part_result >>= v

            result |= r_op.run_expr(_bytes)

        return result

    def to_c_expr(self):
        bundeled_str_repr = ""

        for r_op in self.read_ops:
            str_repr = f"{r_op.var_in.name}[{r_op.var_in.slice}]"

            for op, v in r_op.var_in.history:
                if op == Operators.AND:
                    str_repr = f"({str_repr} {op.value} {C_HEX_TOKEN(v)})"
                else:
                    str_repr = f"({str_repr} {op.value} {v})"

            if r_op.var_in.history:
                str_repr = str_repr[1:-1]

            bundeled_str_repr += " | " + str_repr

        return f"return {bundeled_str_repr[3:]}"

    def __str__(self):
        return f"BREAD : \tout = {self.to_c_expr()}"
