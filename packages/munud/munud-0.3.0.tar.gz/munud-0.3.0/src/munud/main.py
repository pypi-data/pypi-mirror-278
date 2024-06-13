
import click
import yaml
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from .cgen import build_code_from_payload_format
from .munud_types import UnalignedUInt

__version__ = "0.2.0"

BYTE_SIZE = 8


class MunudDecoder:

    def __init__(self, structure: dict[str, UnalignedUInt] = {}, byte_size=0) -> None:
        """Creates a new MunudDecoder instance

        Args:
            structure (dict[str, UnalignedBytes], optional): The structure of the MunudDecoder. Defaults to {}.
            byte_size (int, optional): The size in bytes of the resulting payload. Defaults to 0.
        """
        self.structure = structure
        self.byte_count = byte_size

    def decode(self, payload: bytes) -> dict[str, int]:
        """Decodes a payload according to the given structure.

        Args:
            payload (bytes): The payload to decode.

        Returns:
            dict[str, int]: The decoded payload as a dictionary.
        """

        pattern: dict[str, int] = {}

        for var in self.structure.keys():
            pattern[var] = self.structure[var].extract(payload)

        return pattern

    def encode(self, values: dict[str, int]) -> bytes:
        """Encodes the given values into a munud-formatted bytes payload

        Args:
            values (dict[str, int]): The values as a dictionary [name => value]

        Returns:
            bytes: The munud-formatted bytes payload.
        """

        payload: list[int] = [0] * self.byte_count

        for var in self.structure.keys():
            assert (
                values.get(var) is not None
            ), f"The dict of values sould contain the {var} key."
            self.structure[var].shove(payload, values[var])

        return bytes(payload)

    @classmethod
    def from_yaml_file(cls, filename: str) -> "MunudDecoder":
        """Builds a MunudDecoder instance with the structure described in a yaml file.

        Args:
            filename (str): The filename of the yaml file to use.

        Raises:
            ValueError: If a description of a variable misses the size or the name.

        Returns:
            MunudDecoder: The instance built.
        """

        mDecoder = cls()

        with open(filename, "r") as f:
            offset = 0
            for var in yaml.safe_load(f):
                var_size = var.get("size")
                var_name = var.get("name")

                if var_size is None:
                    raise ValueError(
                        "Ill-formed payload structure: unable to find variable size"
                    )

                if var_name is None:
                    raise ValueError(
                        "Ill-formed payload structure: unable to find variable name"
                    )

                mDecoder.structure[var_name] = UnalignedUInt(
                    offset,
                    var_size,
                )

                offset += var_size

        mDecoder.byte_count = offset // BYTE_SIZE + int(offset % BYTE_SIZE != 0)

        return mDecoder

    @classmethod
    def from_yaml(cls, fmt: str):
        """Builds a MunudDecoder instance with the structure described in a yaml string.

        Args:
            filename (str): The yaml string to use.

        Raises:
            ValueError: If a description of a variable misses the size or the name.

        Returns:
            MunudDecoder: The instance built.
        """
        mDecoder = cls()

        offset = 0
        for var in yaml.safe_load(fmt):
            var_size = var.get("size")
            var_name = var.get("name")

            if var_size is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable size"
                )

            if var_name is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable name"
                )

            mDecoder.structure[var_name] = UnalignedUInt(
                offset,
                var_size,
            )

            offset += var_size

        mDecoder.byte_count = offset // 8 + int(offset % 8 != 0)

        return mDecoder


@click.group()
@click.version_option(__version__)
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.pass_context
def main(ctx, fmt):
    ctx.ensure_object(dict)
    if not fmt:
        return

    ctx.obj["fmt"] = fmt


@main.command()
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.option("-o", "--output", help="The output .h file.")
@click.option(
    "--crlf",
    is_flag=True,
    show_default=True,
    default=False,
    help="Use \\r\\n (crlf) as newline instead of \\n (crlf).",
)
@click.option(
    "--use-assert",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate assert check before writing to payload.",
)
@click.option(
    "--get-only",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate only getters.",
)
@click.option(
    "--set-only",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate only setters.",
)
@click.option(
    "--without-struct",
    is_flag=True,
    show_default=True,
    default=False,
    help="Do not generate a struct containing the payload.",
)
@click.option(
    "--packed-struct",
    is_flag=True,
    show_default=True,
    default=False,
    help="Add the gcc __attribute__((packed)) attribute to the struct.",
)
@click.option("-n", "--struct-name", default="Payload", help="Payload struct name.")
@click.option(
    "--without-safety-mask",
    is_flag=True,
    show_default=True,
    default=False,
    help="Removes the 0xff mask when writing ints on bytes.",
)
@click.option(
    "--payload-type",
    default="uint8_t*",
    help="The type of the payload, usually uint8_t*.",
)
@click.option(
    "--cpp",
    is_flag=True,
    show_default=True,
    default=False,
    help="Generate cpp-style namespace.",
)
@click.option(
    "--namespace",
    default="",
    help="The name of an optional namespace. If cpp is not enabled, add it as a prefix.",
)
@click.pass_context
def cgen(
    ctx,
    fmt,
    output,
    crlf,
    use_assert,
    get_only,
    set_only,
    without_struct,
    packed_struct,
    struct_name,
    without_safety_mask,
    payload_type,
    cpp,
    namespace,
):

    if not fmt:
        if not hasattr(ctx, "obj"):
            print("Please specify a format (--fmt).")
            return

        fmt = ctx.obj.get("fmt")
    if not fmt:
        print("Please specify a format (--fmt).")
        return

    if get_only and set_only:
        print("get-only and set-only are, obviously, mutually exclusive.")
        return

    with open(fmt, "r") as f:
        c_file_result = build_code_from_payload_format(
            yaml.safe_load(f),
            newline="\r\n" if crlf else "\n",
            use_assert=use_assert,
            generate_getters=not set_only,
            generate_setters=not get_only,
            generate_struct=not without_struct,
            packed_struct=packed_struct,
            safety_mask=not without_safety_mask,
            payload_type=payload_type,
            struct_name=struct_name,
            cpp=cpp,
            namespace=namespace,
        )

    if output:
        with open(output, "w") as outfile:
            outfile.write(c_file_result)
    else:
        console = Console()
        syntax = Syntax(c_file_result, "cpp" if cpp else "c")
        console.print(syntax)


@main.command()
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.pass_context
def show(ctx, fmt):

    if not fmt:
        if not hasattr(ctx, "obj"):
            print("Please specify a format (--fmt).")
            return

        fmt = ctx.obj.get("fmt")
    if not fmt:
        print("Please specify a format (--fmt).")
        return

    table = Table(title="Payload")

    table.add_column("Type", justify="right", style="red", no_wrap=True)
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Size (bits)", style="magenta")
    table.add_column("Byte Span", justify="right", style="green")

    with open(fmt, "r") as f:

        offset = 0
        for var in yaml.safe_load(f):
            var_size = var.get("size")
            var_name = var.get("name")
            var_type = var.get("type")

            if var_size is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable size"
                )

            if var_name is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable name"
                )

            if var_type is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable type"
                )

            start_bit = offset
            end_bit = offset + var_size

            bytes_start = start_bit // BYTE_SIZE
            bytes_end = end_bit // BYTE_SIZE + 1

            bit_start = start_bit % BYTE_SIZE
            bit_end = BYTE_SIZE - (end_bit % BYTE_SIZE)

            if bit_end == BYTE_SIZE:
                bit_end = 0
                bytes_end -= 1

            table.add_row(
                var_type,
                var_name,
                f"{var_size}",
                f"[{bytes_start} (+{bit_start}) - {bytes_end}]",
            )

            offset += var_size

        console = Console()
        console.print(table)

        print(f"Total payload size: {offset} bits")


@main.command()
@click.option("-f", "--fmt", help="A file describing the wanted format.")
@click.option("-p", "--payload", help="A hex string describing binary format.")
@click.pass_context
def decode(ctx, fmt, payload):

    if not fmt:
        if not hasattr(ctx, "obj"):
            print("Please specify a format (--fmt).")
            return

        fmt = ctx.obj.get("fmt")
    if not fmt:
        print("Please specify a format (--fmt).")
        return

    if not payload:
        print("Please specify a format (--payload).")
        return

    table = Table(title="Payload")

    table.add_column("Type", justify="right", style="red", no_wrap=True)
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="white")

    with open(fmt, "r") as f:

        offset = 0
        for var in yaml.safe_load(f):
            var_size = var.get("size")
            var_name = var.get("name")
            var_type = var.get("type")

            if var_size is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable size"
                )

            if var_name is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable name"
                )

            if var_type is None:
                raise ValueError(
                    "Ill-formed payload structure: unable to find variable type"
                )

            start_bit = offset
            end_bit = offset + var_size

            bytes_end = end_bit // BYTE_SIZE + 1

            bit_end = BYTE_SIZE - (end_bit % BYTE_SIZE)

            if bit_end == BYTE_SIZE:
                bit_end = 0
                bytes_end -= 1

            val = UnalignedUInt(offset=start_bit, bit_size=var_size).extract(
                bytes.fromhex(payload)
            )

            table.add_row(
                var_type,
                var_name,
                str(val),
            )

            offset += var_size

        console = Console()
        console.print(table)

        print(f"Total payload size: {offset} bits")
