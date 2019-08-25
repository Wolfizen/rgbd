import colour


def rgb(red, green, blue):
    """Returns an int representing an rgb combination; 0-255 each."""
    return (red << 16) + (green << 8) + blue


def unpack_color(color):
    """Return a tuple of red, green, blue values from a color returned by one of these library functions."""
    red = (color >> 16) & 0xFF
    green = (color >> 8) & 0xFF
    blue = color & 0xFF
    return red, green, blue


def from_colour(col):
    """Returns an int like above, from a Color object."""
    return int(col.hex_l[1:], 16)


def from_hex(col_str):
    """Returns int val from a hex string (must be rrggbb, not rgb)."""
    if col_str[0] == "#":
        col_str = col_str[1:]
    return int(col_str, 16)


def col_wheel(pos, size):
    """Color wheel stuffs."""
    return from_colour(colour.Color(hsl=(pos/size, 1, 0.5)))
