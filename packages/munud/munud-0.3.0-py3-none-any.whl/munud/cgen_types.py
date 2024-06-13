import datetime

INDENT = " " * 4


BYTE_SIZE = 8
USE_ASSERTS = True

__version__ = "0.2.0"

HEADER = f"""
/*
* This file was automatically generated using munud {__version__}.
*
* This file should not be edited directly, any changes will be
* overwritten next time the script is run.
*
* Generated on {{}}.
*
* Source code for munud is available at:
* https://gitlab.com/hexa-h/munud
*/
"""


def get_header_with_date():
    return HEADER.format(datetime.datetime.now().strftime("%m/%d/%Y at %H:%M:%S"))


def get_includes(no_assert=False):
    if no_assert:
        return """
#include <stdint.h>
        """
    else:

        return """
#include <assert.h>
#include <stdint.h>
        """


PAYLOAD_TYPE = "uint8_t*"


class CFuncArg:
    def __init__(self, arg_name, arg_type):
        self.arg_name = arg_name
        self.arg_type = arg_type

    def __str__(self) -> str:
        return f"{self.arg_type} {self.arg_name}".replace("* ", " *")

    def __lt__(self, other):
        assert isinstance(
            other, CFuncArg
        ), "You cannot compare something else than a CFuncArg to a CFuncArg."

        order = (
            "uint64_t",
            "uint32_t",
            "uint16_t",
            "uint8_t",
        )

        if not all(
            (
                self.arg_type in order,
                other.arg_type in order,
            )
        ):
            return False

        return order.index(other.arg_type) > order.index(self.arg_type)


CStructArg = CFuncArg


class CCodeStatement:
    def __init__(self, code_statement: str):
        self.code_statement = code_statement

    def __str__(self) -> str:
        return f"{self.code_statement};"


class CCodeBlock:
    def __init__(self, code_statements=list[CCodeStatement], newline="\n"):
        self.code_statements = code_statements
        self.newline = newline

    def __str__(self) -> str:
        joined_code_statements = f"{self.newline}{INDENT}".join(
            str(cs) for cs in self.code_statements
        )
        return f"{self.newline}{INDENT}{joined_code_statements}{self.newline}"

    def __add__(self, other) -> "CCodeBlock":

        assert isinstance(
            other, CCodeBlock
        ), "You cannot add something else than a CCodeBlock to a CCodeBlock."

        return CCodeBlock(
            self.code_statements.extend(other.code_statements), newline=self.newline
        )


class CCommentBlock:
    def __init__(self, comment: str, indent: int = 0, newline="\n"):
        self.comment = comment
        self.indent = indent
        self.newline = newline

    def __str__(self):
        builder = f"{INDENT*self.indent}/*{self.newline}{INDENT*self.indent} * "
        builder += f"{self.newline}{INDENT*self.indent} * ".join(
            self.comment.splitlines()
        )
        builder += f"{self.newline}{INDENT*self.indent} */{self.newline}"

        return builder


class CFunc:
    def __init__(
        self,
        func_type: str,
        func_name: str,
        func_args: list[CFuncArg],
        body: CCodeBlock,
        docstring: str,
        inline_static: bool = True,
        newline: str = "\n",
    ):
        self.func_type = func_type
        self.func_name = func_name
        self.func_args = func_args
        self.body = body
        self.docstring = docstring
        self.inline_static = inline_static
        self.newline = newline

    def __str__(self) -> str:
        func_args = ", ".join(str(arg) for arg in self.func_args)
        comment_block = CCommentBlock(self.docstring, indent=1)

        prefix = "inline static" if self.inline_static else ""

        return f"{prefix} {self.func_type} {self.func_name}({func_args}){self.newline}{{{self.newline}{comment_block}{self.body}}}"


class CStruct:
    def __init__(
        self,
        struct_name: str,
        struct_components: list[CStructArg],
        docstring: str,
        packed: bool,
        newline: str = "\n",
    ):
        self.struct_name = struct_name
        self.struct_components = struct_components
        self.docstring = docstring
        self.packed = packed
        self.newline = newline

    def __str__(self) -> str:

        sorted_struct_components = sorted(self.struct_components)

        struct_body = str(
            CCodeBlock([CCodeStatement(str(arg)) for arg in sorted_struct_components])
        )

        packed_attribute = "__attribute__((packed))" if self.packed else ""

        return f"struct {packed_attribute}{self.struct_name}{self.newline}{{{self.newline}{struct_body}}};"
