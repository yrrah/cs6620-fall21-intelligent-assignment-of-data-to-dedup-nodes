def hex_string_to_int(hex_string: str) -> int:
    """
    :param hex_string: a string formatted like 3f:8d:1a:35:a8:ff
    :return: integer value of the hex string
    """
    four_bit_numbers = hex_string.split(':')
    value = 0
    # parse string and add to lowest 4 bits of the integer until done
    for n in four_bit_numbers:
        value += int(n, 16)
        value = value << 4

    return value


def test_hex_string_to_int():
    assert (hex_string_to_int("3f:8d:1a:35:a8:ff") == 71206781936)
