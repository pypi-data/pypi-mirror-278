from dataclasses import dataclass
from typing import Union

from .munud import BundeledReadOperation, ReadOperation, Var, WriteOperation


@dataclass
class UnalignedUInt:
    """A representation of an unsigned integer of arbitrary length,
    in an array of bytes, which is not aligned on the bytes.

    """

    offset: int = 0
    bit_size: int = 4
    use_safety_mask: bool = True
    byte_size: int = 8

    def integrity_check(self, byte_buffer: Union[bytes, list[int]]) -> None:
        """_summary_

        Args:
            byte_buffer (_type_): _description_


        Raises:
            ValueError: When the starting bit falls outside the array
            ValueError: When the byte buffer is too small to contain this integer
        """
        if self.bit_start >= self.byte_size:
            raise ValueError(
                f"Starting bit ({self.bit_start}) is greater than byte size ({self.byte_size})"
            )

        if self.byte_offset + self.bytes_span > len(byte_buffer):
            raise ValueError(
                f"{self.byte_offset + self.bytes_span = } > {len(byte_buffer) = } : The byte buffer is too small"
            )

    def extract(self, byte_buffer: bytes) -> int:
        self.integrity_check(byte_buffer)

        value = self.op_read().run_expr(byte_buffer)

        assert (
            value < 2**self.bit_size
        ), f"{value} is too big to fit into {self.bit_size} bits. Something went horribly wrong."

        return value

    def shove(self, byte_buffer: list[int], value: int) -> None:
        self.integrity_check(byte_buffer)

        assert (
            value < 2**self.bit_size
        ), f"{value} is too big to fit into {self.bit_size} bits."

        for w_op in self.op_write():
            assert (
                w_op.var_out.slice is not None
            ), "`var_out` should have a slice. This is munud's developper fault, please report this bug."

            if w_op.or_write:
                byte_buffer[w_op.var_out.slice] |= w_op.run_expr(value)
            else:
                byte_buffer[w_op.var_out.slice] = w_op.run_expr(value)

    def setter_c_docstring(self, var_name: str, newline: str) -> str:
        end = self.offset + self.bit_size
        bytes_end = end // self.byte_size + 1

        bit_start = self.offset % self.byte_size
        bit_end = self.byte_size - (end % self.byte_size)

        if bit_end == self.byte_size:
            bit_end = 0
            bytes_end -= 1

        docstring = f"This function writes the value {var_name} ({self.bit_size} bits).{newline}"
        if bytes_end - self.byte_offset > 1:
            docstring += f"The value will spread between bytes {self.byte_offset} and {bytes_end -1 }.{newline}"
        else:
            docstring += f"The value will be written in byte {self.offset}.{newline}"

        docstring += f"The value starts at bit {bit_start}.{newline}"

        return docstring

    def getter_c_docstring(self, var_name: str, newline: str) -> str:
        end = self.offset + self.bit_size
        bytes_end = end // self.byte_size + 1

        bit_start = self.offset % self.byte_size
        bit_end = self.byte_size - (end % self.byte_size)

        if bit_end == self.byte_size:
            bit_end = 0
            bytes_end -= 1

        docstring = f"This function retrives the value {var_name} ({self.bit_size} bits).{newline}"

        if bytes_end - self.byte_offset > 1:
            docstring += f"The value spreads between bytes {self.byte_offset} and {bytes_end -1 }.{newline}"
        else:
            docstring += f"The value is found in byte {self.byte_offset}.{newline}"

        docstring += f"The value starts at bit {bit_start}.{newline}"

        return docstring

    @property
    def bit_start(self) -> int:
        return self.offset % self.byte_size

    @property
    def byte_offset(self) -> int:
        return self.offset // self.byte_size

    @property
    def first_byte_mask(self) -> int:
        if self.is_aligned_left:
            raise ValueError("First byte mask is 0xFF, as we are left aligned.")

        return (1 << (self.byte_size - self.bit_start)) - 1

    @property
    def bytes_span(self) -> int:
        return (self.bit_size + self.bit_start) // 8 + (not self.is_aligned_right)

    @property
    def is_aligned(self) -> bool:
        return self.bit_start == 0 and self.bit_size % self.byte_size == 0

    @property
    def is_aligned_left(self) -> bool:
        return self.bit_start == 0

    @property
    def is_aligned_right(self) -> bool:
        return (self.bit_start + self.bit_size) % self.byte_size == 0

    def op_read(self) -> ReadOperation:

        if self.bytes_span == 1:
            if self.is_aligned:
                return self.aligned_single_byte_op_read()
            if self.is_aligned_left:
                return self.left_aligned_single_byte_op_read()
            if self.is_aligned_right:
                return self.right_aligned_single_byte_op_read()

            return self.unaligned_single_byte_op_read()

        return self.multiple_byte_op_read()

    def op_write(self) -> list[WriteOperation]:
        if self.bytes_span == 1:
            if self.is_aligned:
                return self.aligned_single_byte_op_write()
            if self.is_aligned_left:
                return self.left_aligned_single_byte_op_write()
            if self.is_aligned_right:
                return self.right_aligned_single_byte_op_write()

            return self.unaligned_single_byte_op_write()

        return self.multiple_byte_op_write()

    def aligned_single_byte_op_write(self) -> list[WriteOperation]:
        return [
            WriteOperation(
                Var("payload")[self.byte_offset],
                Var("value"),
            )
        ]

    def aligned_single_byte_op_read(self) -> ReadOperation:
        return ReadOperation(Var("payload")[self.byte_offset])

    def left_aligned_single_byte_op_write(self) -> list[WriteOperation]:
        return [
            WriteOperation(
                Var("payload")[self.byte_offset],
                Var("value") << (self.byte_size - self.bit_size),
                or_write=True,
            )
        ]

    def left_aligned_single_byte_op_read(self) -> ReadOperation:
        return ReadOperation(
            Var("payload")[self.byte_offset] >> (self.byte_size - self.bit_size)
        )

    def right_aligned_single_byte_op_write(self) -> list[WriteOperation]:

        return [
            WriteOperation(
                Var("payload")[self.byte_offset],
                Var("value"),
                or_write=True,
            )
        ]

    def right_aligned_single_byte_op_read(self) -> ReadOperation:
        return ReadOperation(Var("payload")[self.byte_offset] & self.first_byte_mask)

    def unaligned_single_byte_op_write(self) -> list[WriteOperation]:
        return [
            WriteOperation(
                Var("payload")[self.byte_offset],
                Var("value") << (self.byte_size - self.bit_size - self.bit_start),
                or_write=True,
            )
        ]

    def unaligned_single_byte_op_read(self) -> ReadOperation:
        return ReadOperation(
            (Var("payload")[self.byte_offset] & self.first_byte_mask)
            >> (self.byte_size - self.bit_size - self.bit_start)
        )

    def multiple_byte_op_write(self) -> list[WriteOperation]:

        w_op: list[WriteOperation] = []

        part_calc: Var

        if self.is_aligned:
            for i in range(self.bytes_span - 1):
                part_calc = Var("value") >> ((self.bytes_span - i - 1) * self.byte_size)

                if self.use_safety_mask:
                    part_calc &= 0xFF

                w_op.append(
                    WriteOperation(
                        Var("payload")[self.byte_offset + i],
                        part_calc,
                    )
                )

            part_calc = Var("value")

            if self.use_safety_mask:
                part_calc &= 0xFF

            w_op.append(
                WriteOperation(
                    Var("payload")[self.byte_offset + self.bytes_span - 1],
                    part_calc,
                )
            )

            return w_op

        if not self.is_aligned_left:

            w_op.append(
                WriteOperation(
                    Var("payload")[self.byte_offset],
                    Var("value") >> (self.bit_size + self.bit_start - self.byte_size)
                    & self.first_byte_mask,
                    or_write=True,
                )
            )

        else:
            part_calc = Var("value") >> (self.bit_size - self.byte_size)

            if self.use_safety_mask:
                part_calc &= 0xFF

            w_op.append(
                WriteOperation(
                    Var("payload")[self.byte_offset],
                    part_calc,
                )
            )

        if self.bytes_span >= 2:
            for i in range(self.bytes_span - 2):
                part_calc = Var("value") >> (
                    self.bit_size + self.bit_start - self.byte_size * (i + 2)
                )

                if self.use_safety_mask:
                    part_calc &= 0xFF

                w_op.append(
                    WriteOperation(
                        Var("payload")[self.byte_offset + i + 1],
                        part_calc,
                    )
                )

        if not self.is_aligned_right:
            part_calc = Var("value") << (
                self.bytes_span * self.byte_size - self.bit_size - self.bit_start
            )

            if self.use_safety_mask:
                part_calc &= 0xFF

            w_op.append(
                WriteOperation(
                    Var("payload")[self.byte_offset + self.bytes_span - 1],
                    part_calc,
                    or_write=True,
                )
            )

        else:
            part_calc = Var("value")

            if self.use_safety_mask:
                part_calc &= 0xFF

            w_op.append(
                WriteOperation(
                    Var("payload")[self.byte_offset + self.bytes_span - 1],
                    part_calc,
                )
            )

        return w_op

    def multiple_byte_op_read(self) -> BundeledReadOperation:

        read_ops: list[ReadOperation] = []

        if self.is_aligned:

            for i in range(self.bytes_span - 1):

                read_ops.append(
                    ReadOperation(
                        Var("payload")[self.byte_offset + i]
                        << ((self.bytes_span - i - 1) * self.byte_size)
                    )
                )

            read_ops.append(
                ReadOperation(Var("payload")[self.byte_offset + self.bytes_span - 1])
            )

            return BundeledReadOperation(read_ops)

        if not self.is_aligned_left:
            read_ops.append(
                ReadOperation(
                    (Var("payload")[self.byte_offset] & self.first_byte_mask)
                    << (self.bit_size + self.bit_start - self.byte_size)
                )
            )

        else:
            read_ops.append(
                ReadOperation(
                    Var("payload")[self.byte_offset] << (self.bit_size - self.byte_size)
                )
            )

        if self.bytes_span >= 2:
            for i in range(self.bytes_span - 2):
                read_ops.append(
                    ReadOperation(
                        Var("payload")[self.byte_offset + i + 1]
                        << (self.bit_size + self.bit_start - self.byte_size * (i + 2))
                    )
                )

        if not self.is_aligned_right:
            read_ops.append(
                ReadOperation(
                    Var("payload")[self.byte_offset + self.bytes_span - 1]
                    >> (
                        self.bytes_span * self.byte_size
                        - self.bit_size
                        - self.bit_start
                    )
                )
            )

        else:
            read_ops.append(
                ReadOperation(Var("payload")[self.byte_offset + self.bytes_span - 1])
            )

        return BundeledReadOperation(read_ops)
