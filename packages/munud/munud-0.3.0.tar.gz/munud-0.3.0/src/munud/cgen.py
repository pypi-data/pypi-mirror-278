from munud.munud_types import UnalignedUInt
from munud.utils import C_LARGE_HEX_TOKEN

from .cgen_types import (CCodeBlock, CCodeStatement, CFunc, CFuncArg, CStruct,
                         CStructArg, get_header_with_date, get_includes)

ALLOWED_VAR_TYPES = (
    "uint64_t",
    "uint32_t",
    "uint16_t",
    "uint8_t",
)


def build_getter(
    var_name,
    var_type,
    bit_size,
    offset,
    newline="\n",
    payload_type="uint8_t",
    func_prefix="",
) -> str:

    get_function_args = [
        CFuncArg("payload", payload_type),
    ]

    ub = UnalignedUInt(
        offset,
        bit_size,
    )

    get_function = CFunc(
        var_type,
        f"{func_prefix}get_{var_name}",
        get_function_args,
        CCodeBlock(
            [
                CCodeStatement(
                    ub.op_read().to_c_expr(),
                ),
            ],
        ),
        ub.getter_c_docstring(var_name, newline),
        newline,
    )

    return str(get_function)


def build_setter(
    var_name,
    var_type,
    bit_size,
    offset,
    newline="\n",
    safety_mask=True,
    payload_type="uint8_t",
    use_assert=False,
    func_prefix="",
) -> str:

    set_function_args = [
        CFuncArg("payload", payload_type),
        CFuncArg("value", var_type),
    ]

    ub = UnalignedUInt(
        offset,
        bit_size,
        use_safety_mask=safety_mask,
    )

    cstatements: list[CCodeStatement] = []

    if use_assert:
        cstatements.append(
            CCodeStatement(f"assert(value <= {C_LARGE_HEX_TOKEN(2**bit_size-1)})")
        )

    for statement in ub.op_write():
        cstatements.append(
            CCodeStatement(
                statement.to_c_expr(),
            ),
        )

    get_function = CFunc(
        "void",
        f"{func_prefix}set_{var_name}",
        set_function_args,
        CCodeBlock(
            cstatements,
            newline,
        ),
        ub.setter_c_docstring(var_name, newline),
        newline,
    )

    return str(get_function)


def payload_generator(payload: list[dict]):
    offset = 0

    for var in payload:

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

        yield var_name, offset, var_size, var_type

        offset += var_size


def build_code_from_payload_format(
    format_list: list[dict],
    newline="\n",
    use_assert=False,
    generate_getters=True,
    generate_setters=True,
    generate_struct=True,
    packed_struct=False,
    safety_mask=True,
    cpp=False,
    namespace=None,
    payload_type="uint8_t*",
    struct_name="Payload",
) -> str:
    """Generates C code from a payload representation.

    Args:
        format_list (list[dict]): The format of the payload.
        newline (str, optional): The newline to use in the C code representation. Defaults to "\n".
        no_assert (bool, optional): Generate an assert at the begenning of a write function, checking if the value is not too big to fit. Defaults to False.
        generate_getters (bool, optional): Generate the getter functions. Defaults to True.
        generate_setters (bool, optional): Generate the setter functions. Defaults to True.
        generate_struct (bool, optional): Generate the according struct. Defaults to True.
        safety_mask (bool, optional): Add a safety mask (0xff) when writing to the patload. Defaults to True.
        payload_type (str, optional): The type of the payload. Defaults to "uint8_t*".
        struct_name (str, optional): The name of the struct. Defaults to "Payload".

    Returns:
        str: The according c code.
    """

    generated_c_code = ""

    header_guard = "DEFAULT_MUNUD_HEADER_GUARD_H"

    if namespace:
        header_guard = f"{namespace.upper()}_H"

    generated_c_code += get_header_with_date()
    generated_c_code += get_includes(no_assert=use_assert)

    generated_c_code += f"\n#ifndef {header_guard}"
    generated_c_code += f"\n#define {header_guard}\n"

    funcs_prefix = ""

    if namespace:
        if cpp:
            generated_c_code += f"\nnamespace {namespace} {{"
        else:
            funcs_prefix = namespace

    if funcs_prefix:
        funcs_prefix += "_"

    struct_components: list[CStructArg] = []

    for var_name, offset, var_size, var_type in payload_generator(format_list):

        if var_type not in ALLOWED_VAR_TYPES:
            raise ValueError(
                f"{var_type} : unknown variable type (should be one of uint8_t, uint16_t, uint32_t, uint64_t)"
            )

        struct_components.append(CStructArg(var_name, var_type))

        if generate_getters:

            generated_c_code += newline * 2

            generated_c_code += build_getter(
                var_name,
                var_type,
                var_size,
                offset,
                newline=newline,
                payload_type=payload_type,
                func_prefix=funcs_prefix,
            )

        if generate_setters:

            generated_c_code += newline * 2

            generated_c_code += build_setter(
                var_name,
                var_type,
                var_size,
                offset,
                newline=newline,
                safety_mask=safety_mask,
                payload_type=payload_type,
                use_assert=use_assert,
                func_prefix=funcs_prefix,
            )

        generated_c_code += "\n"

    if generate_struct:

        generated_c_code += newline * 2
        generated_c_code += str(
            CStruct(struct_name, struct_components, "", packed_struct, newline)
        )
        generated_c_code += newline * 2

    if generate_getters and generate_struct:

        decode_all = CFunc(
            "void",
            f"{funcs_prefix}decode",
            [
                CFuncArg("payload", f"struct {struct_name}*"),
                CFuncArg("packed", "uint8_t*"),
            ],
            CCodeBlock(
                [
                    *[
                        CCodeStatement(
                            f"payload->{sc.arg_name} = get_{sc.arg_name}(packed)"
                        )
                        for (sc) in struct_components
                    ]
                ]
            ),
            "",
        )

        generated_c_code += newline * 2
        generated_c_code += str(decode_all)

    if generate_setters and generate_struct:

        encode_all = CFunc(
            "void",
            f"{funcs_prefix}encode",
            [
                CFuncArg("payload", f"struct {struct_name}*"),
                CFuncArg("packed", "uint8_t*"),
            ],
            CCodeBlock(
                [
                    *[
                        CCodeStatement(
                            f"set_{sc.arg_name}(packed, payload->{sc.arg_name})"
                        )
                        for (sc) in struct_components
                    ]
                ]
            ),
            "",
        )

        generated_c_code += newline * 2
        generated_c_code += str(encode_all)

    if namespace and cpp:
        generated_c_code += "\n"
        generated_c_code += f"\n}} // namespace {namespace}"

    generated_c_code += "\n"
    generated_c_code += "\n"

    generated_c_code += f"#endif //{header_guard}\n"

    return generated_c_code
