def C_HEX_TOKEN(value: int) -> str:
    """Convert a number between 0-255 into its c string hexadecimal representation.

    Args:
        value int: An int between 0-255

    Returns:
        string: The C string reprensetation of this number
    """
    assert (
        0 <= value <= 0xFF
    ), f"{value} > 0xff, cowardly refusing to convert to c hex token."
    mask = f"{value:#04X}"
    return "0x" + mask[2:]


def C_LARGE_HEX_TOKEN(value: int) -> str:
    """Convert a number between into its c string hexadecimal representation.

    Args:
        value int: An int

    Returns:
        string: The C string representation of this number
    """
    mask = f"{value:#04X}"
    return "0x" + mask[2:]
