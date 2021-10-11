def hex_string_to_int(hex_string: str) -> int:
    """
    :param hex_string: a string formatted like 3f:8d:1a:35:a8:ff
    :return: integer value of the hex string
    """
    segments = hex_string.split(':')
    return int(''.join(segments), 16)


def test_hex_string_to_int():
    assert (hex_string_to_int("3f:8d:1a:35:a8:ff") == 69875262662911)
