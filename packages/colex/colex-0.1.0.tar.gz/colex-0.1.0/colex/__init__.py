"""
Colex
----

Library with constants and functions for working with colors

Includes:
- `ColorValue` (annotation)
- `colorize` (apply color to string)
- `ansi_color`
- `hex_color`
- `rand_color`
- `rgb_color`
- 8-bit colors
- 16-bit colors
- Styling constants (use `[color] + [style]`)
- HTML color constants
"""

from __future__ import annotations as _annotations

__version__ = "0.1.0"
__all__ = [
    # annotations
    "ColorValue",
    # functions
    "colorize",
    "ansi_color",
    "hex_color",
    "rand_color",
    "rgb_color",
    # constants
    "ALICE_BLUE",
    "ANTIQUE_WHITE",
    "AQUA",
    "AQUAMARINE",
    "AZURE",
    "BEIGE",
    "BISQUE",
    "BLACK",
    "BLANCHED_ALMOND",
    "BLUE",
    "BLUE_VIOLET",
    "BOLD",
    "BRIGHT_BLACK",
    "BRIGHT_BLUE",
    "BRIGHT_CYAN",
    "BRIGHT_GREEN",
    "BRIGHT_MAGENTA",
    "BRIGHT_RED",
    "BRIGHT_WHITE",
    "BRIGHT_YELLOW",
    "BROWN",
    "BURLY_WOOD",
    "CADET_BLUE",
    "CHARTREUSE",
    "CHOCOLATE",
    "CORAL",
    "CORNFLOWER_BLUE",
    "CORNSILK",
    "CRIMSON",
    "CYAN",
    "DARK_BLUE",
    "DARK_CYAN",
    "DARK_GOLDENROD",
    "DARK_GRAY",
    "DARK_GREEN",
    "DARK_KHAKI",
    "DARK_MAGENTA",
    "DARK_OLIVE_GREEN",
    "DARK_ORANGE",
    "DARK_ORCHID",
    "DARK_RED",
    "DARK_SALMON",
    "DARK_SEA_GREEN",
    "DARK_SLATE_BLUE",
    "DARK_SLATE_GRAY",
    "DARK_TURQUOISE",
    "DARK_VIOLET",
    "DEEP_PINK",
    "DEEP_SKY_BLUE",
    "DIM_GRAY",
    "DODGER_BLUE",
    "FIREBRICK",
    "FLORAL_WHITE",
    "FOREST_GREEN",
    "FUCHSIA",
    "GAINSBORO",
    "GHOST_WHITE",
    "GOLD",
    "GOLDENROD",
    "GRAY",
    "GREEN",
    "GREEN_YELLOW",
    "HONEYDEW",
    "HOT_PINK",
    "INDIAN_RED",
    "INDIGO",
    "IVORY",
    "KHAKI",
    "LAVENDER",
    "LAVENDER_BLUSH",
    "LAWN_GREEN",
    "LEMON_CHIFFON",
    "LIGHT_BLUE",
    "LIGHT_CORAL",
    "LIGHT_CYAN",
    "LIGHT_GOLDENROD_YELLOW",
    "LIGHT_GRAY",
    "LIGHT_GREEN",
    "LIGHT_PINK",
    "LIGHT_SALMON",
    "LIGHT_SEA_GREEN",
    "LIGHT_SKY_BLUE",
    "LIGHT_SLATE_GRAY",
    "LIGHT_STEEL_BLUE",
    "LIGHT_YELLOW",
    "LIME",
    "LIME_GREEN",
    "LINEN",
    "MAGENTA",
    "MAROON",
    "MEDIUM_AQUAMARINE",
    "MEDIUM_BLUE",
    "MEDIUM_ORCHID",
    "MEDIUM_PURPLE",
    "MEDIUM_SEA_GREEN",
    "MEDIUM_SLATE_BLUE",
    "MEDIUM_SPRING_GREEN",
    "MEDIUM_TURQUOISE",
    "MEDIUM_VIOLET_RED",
    "MIDNIGHT_BLUE",
    "MINT_CREAM",
    "MISTY_ROSE",
    "MOCCASIN",
    "NAVAJO_WHITE",
    "NAVY",
    "OLD_LACE",
    "OLIVE",
    "OLIVE_DRAB",
    "ORANGE",
    "ORANGE_RED",
    "ORCHID",
    "PALE_GOLDENROD",
    "PALE_GREEN",
    "PALE_TURQUOISE",
    "PALE_VIOLET_RED",
    "PAPAYA_WHIP",
    "PEACH_PUFF",
    "PERU",
    "PINK",
    "PLUM",
    "POWDER_BLUE",
    "PURPLE",
    "RED",
    "RESET",
    "REVERSE",
    "ROSY_BROWN",
    "ROYAL_BLUE",
    "SADDLE_BROWN",
    "SALMON",
    "SANDY_BROWN",
    "SEA_GREEN",
    "SEA_SHELL",
    "SIENNA",
    "SILVER",
    "SKY_BLUE",
    "SLATE_BLUE",
    "SLATE_GRAY",
    "SNOW",
    "SPRING_GREEN",
    "STEEL_BLUE",
    "STRIKETHROUGH",
    "TAN",
    "TEAL",
    "THISTLE",
    "TOMATO",
    "TURQUOISE",
    "UNDERLINE",
    "VIOLET",
    "WHEAT",
    "WHITE",
    "WHITE_SMOKE",
    "YELLOW",
    "YELLOW_GREEN"
]

import random as _random
from typing import TypeAlias as _TypeAlias

ColorValue: _TypeAlias = str
_ColorCode: _TypeAlias = int | str
_HexCode: _TypeAlias = str


def colorize(string: str, color: ColorValue) -> str:
    """Applies color to the given string. Appends RESET code to the end automatically

    Args:
        string (str): text to paint
        color (ColorValue): paint color

    Returns:
        str: colored string
    """
    return color + string + RESET


def ansi_color(fg: _ColorCode = 7, bg: _ColorCode | None = None, *, bold: bool = False, reverse: bool = False, underline: bool = False) -> ColorValue:
    """Creates a color from the given color code. Can be given both a foreground color and background color

    `NOTE`: colors made using this function will not be equivalent to other colors defined in the RGB format regarding ANSI formatting,
    when comparing using the `==` operator, as their string representations will be different
    
    Args:
        fg (_ColorCode, optional): foreground color. Defaults to 7.
        bg (_ColorCode | None, optional): background color. Defaults to None.
        bold (bool, optional): applies bold style. Defaults to False.
        reverse (bool, optional): swaps fg and bg. Defaults to False.
        underline (bool, optional): adds an underline. Defaults to False.

    Returns:
        ColorValue: ANSI color code as str
    """
    value = f"\x1b[38;5;{fg}m"
    if not (bold or reverse or underline):
        return value
    if bg is not None:
        value += f"\x1b[48;5;{bg}m"
    if bold:
        value += f"\x1b[1m"
    if underline:
        value += f"\x1b[4m"
    if reverse:
        value += f"\x1b[7m"
    return value


def rgb_color(red: int = 0, green: int = 0, blue: int = 0, *, background: bool = False, bold: bool = False, reverse: bool = False, underline: bool = False) -> ColorValue:
    """Creates a color from the given channels, which is red, green and blue. Can be given both a foreground color and background color

    Args:
        red (int, optional): red color channel. Defaults to 0.
        green (int, optional): green color channel. Defaults to 0.
        blue (int, optional): blue color channel. Defaults to 0.
        background (bool, optional): colors background instead of foreground. Defaults to False.
        bold (bool, optional): applies bold style. Defaults to False.
        reverse (bool, optional): swaps fg and bg. Defaults to False.
        underline (bool, optional): adds an underline. Defaults to False.

    Returns:
        ColorValue: ANSI color code as str
    """
    layer = 38 if not background else 48
    value = "\x1b[{};2;{};{};{}m".format(layer, red, green, blue)
    if bold:
        value += f"\x1b[1m"
    if underline:
        value += f"\x1b[4m"
    if reverse:
        value += f"\x1b[7m"
    return value


def hex_color(fg: _HexCode = "#ffffff", bg: _HexCode | None = None, *, bold: bool = False, reverse: bool = False, underline: bool = False) -> ColorValue:
    """Creates a color from the given hex code. Can be given both a foreground color and background color
    The "#" in the hex codes are optional

    Args:
        fg (_HexCode, optional): foreground hex color. Defaults to "#ffffff".
        bg (_HexCode | None, optional): background hex color. Defaults to None.
        bold (bool, optional): applies bold style. Defaults to False.
        reverse (bool, optional): swaps fg and bg. Defaults to False.
        underline (bool, optional): adds an underline. Defaults to False.

    Returns:
        ColorValue: ANSI color code as str
    """
    fg = fg.lower()
    if fg.startswith("#"):
        fg = fg.lstrip("#")
    if len(fg) == 3:
        fg = ''.join([c * 2 for c in fg])
    
    red = int(fg[0:2], 16)
    green = int(fg[2:4], 16)
    blue = int(fg[4:6], 16)
    value = "\x1b[38;2;{};{};{}m".format(red, green, blue)

    if bg is None:
        # does not compute background color
        if not (bold or reverse or underline):
            return value
        if bold:
            value += f"\x1b[1m"
        if underline:
            value += f"\x1b[4m"
        if reverse:
            value += f"\x1b[7m"
        return value

    bg = bg.lower()
    if bg.startswith("#"):
        bg = bg.lstrip("#")
    if len(bg) == 3:
        bg = "".join([c * 2 for c in bg])
    
    red = int(bg[0:2], 16)
    green = int(bg[2:4], 16)
    blue = int(bg[4:6], 16)
    value += "\x1b[48;2;{};{};{}m".format(red, green, blue)
    if not (bold or reverse or underline):
        return value
    if bold:
        value += f"\x1b[1m"
    if underline:
        value += f"\x1b[4m"
    if reverse:
        value += f"\x1b[7m"
    return value


def rand_color(fg: bool = True, bg: bool = False, *, bold: bool = False, reverse: bool = False, underline: bool = False) -> ColorValue:
    """Creates a random RGB color. Random background color is optional

    Args:
        fg (bool, optional): whether to colorize the foreground with a random color. Defaults to True.
        bg (bool, optional): whether to colorize the background with a random color. Defaults to False.
        bold (bool, optional): applies bold style. Defaults to False.
        reverse (bool, optional): swaps fg and bg. Defaults to False.
        underline (bool, optional): adds an underline. Defaults to False.

    Raises:
        ValueError: both 'fg' and 'bg' was set to be False

    Returns:
        ColorValue: ANSI color code as str
    """
    if not fg and not bg:
        raise ValueError("Either 'foreground' or 'background' has to be True")
    value = ""
    if fg:
        value += "\x1b[38;2;{};{};{}m".format(
            _random.randint(0, 255),
            _random.randint(0, 255),
            _random.randint(0, 255))
    if bg:
        value += "\x1b[48;2;{};{};{}m".format(
            _random.randint(0, 255),
            _random.randint(0, 255),
            _random.randint(0, 255))
    if not (bold or reverse or underline):
        return value
    if bold:
        value += f"\x1b[1m"
    if underline:
        value += f"\x1b[4m"
    if reverse:
        value += f"\x1b[7m"
    return value


# reset code
RESET = "\x1b[0m"

# modes
BOLD          = "\x1b[1m"
UNDERLINE     = "\x1b[4m"
REVERSE       = "\x1b[7m"
STRIKETHROUGH = "\x1b[9m"

# standard colors:
BLACK   = "\x1b[38;2;0;0;0m"
RED     = "\x1b[38;2;255;0;0m"
GREEN   = "\x1b[38;2;0;255;0m"
YELLOW  = "\x1b[38;2;255;255;0m"
BLUE    = "\x1b[38;2;0;0;255m"
MAGENTA = "\x1b[38;2;255;0;255m"
CYAN    = "\x1b[38;2;0;255;255m"
WHITE   = "\x1b[38;2;255;255;255m"

# bright standard colors:
BRIGHT_BLACK   = "\x1b[38;2;85;85;85m"
BRIGHT_RED     = "\x1b[38;2;255;85;85m"
BRIGHT_GREEN   = "\x1b[38;2;85;255;85m"
BRIGHT_YELLOW  = "\x1b[38;2;255;255;85m"
BRIGHT_BLUE    = "\x1b[38;2;85;85;255m"
BRIGHT_MAGENTA = "\x1b[38;2;255;85;255m"
BRIGHT_CYAN    = "\x1b[38;2;85;255;255m"
BRIGHT_WHITE   = "\x1b[38;2;255;255;255m"

# html/css colors:
ALICE_BLUE = "\x1b[38;2;240;248;255m"
ANTIQUE_WHITE = "\x1b[38;2;250;235;215m"
AQUA = "\x1b[38;2;0;255;255m"
AQUAMARINE = "\x1b[38;2;127;255;212m"
AZURE = "\x1b[38;2;240;255;255m"
BEIGE = "\x1b[38;2;245;245;220m"
BISQUE = "\x1b[38;2;255;228;196m"
BLANCHED_ALMOND = "\x1b[38;2;255;235;205m"
BLUE_VIOLET = "\x1b[38;2;138;43;226m"
BROWN = "\x1b[38;2;165;42;42m"
BURLY_WOOD = "\x1b[38;2;222;184;135m"
CADET_BLUE = "\x1b[38;2;95;158;160m"
CHARTREUSE = "\x1b[38;2;127;255;0m"
CHOCOLATE = "\x1b[38;2;210;105;30m"
CORAL = "\x1b[38;2;255;127;80m"
CORNFLOWER_BLUE = "\x1b[38;2;100;149;237m"
CORNSILK = "\x1b[38;2;255;248;220m"
CRIMSON = "\x1b[38;2;220;20;60m"
DARK_BLUE = "\x1b[38;2;0;0;139m"
DARK_CYAN = "\x1b[38;2;0;139;139m"
DARK_GOLDENROD = "\x1b[38;2;184;134;11m"
DARK_GRAY = "\x1b[38;2;169;169;169m"
DARK_GREEN = "\x1b[38;2;0;100;0m"
DARK_KHAKI = "\x1b[38;2;189;183;107m"
DARK_MAGENTA = "\x1b[38;2;139;0;139m"
DARK_OLIVE_GREEN = "\x1b[38;2;85;107;47m"
DARK_ORANGE = "\x1b[38;2;255;140;0m"
DARK_ORCHID = "\x1b[38;2;153;50;204m"
DARK_RED = "\x1b[38;2;139;0;0m"
DARK_SALMON = "\x1b[38;2;233;150;122m"
DARK_SEA_GREEN = "\x1b[38;2;143;188;143m"
DARK_SLATE_BLUE = "\x1b[38;2;72;61;139m"
DARK_SLATE_GRAY = "\x1b[38;2;47;79;79m"
DARK_TURQUOISE = "\x1b[38;2;0;206;209m"
DARK_VIOLET = "\x1b[38;2;148;0;211m"
DEEP_PINK = "\x1b[38;2;255;20;147m"
DEEP_SKY_BLUE = "\x1b[38;2;0;191;255m"
DIM_GRAY = "\x1b[38;2;105;105;105m"
DODGER_BLUE = "\x1b[38;2;30;144;255m"
FIREBRICK = "\x1b[38;2;178;34;34m"
FLORAL_WHITE = "\x1b[38;2;255;250;240m"
FOREST_GREEN = "\x1b[38;2;34;139;34m"
FUCHSIA = "\x1b[38;2;255;0;255m"
GAINSBORO = "\x1b[38;2;220;220;220m"
GHOST_WHITE = "\x1b[38;2;248;248;255m"
GOLD = "\x1b[38;2;255;215;0m"
GOLDENROD = "\x1b[38;2;218;165;32m"
GRAY = "\x1b[38;2;128;128;128m"
GREEN_YELLOW = "\x1b[38;2;173;255;47m"
HONEYDEW = "\x1b[38;2;240;255;240m"
HOT_PINK = "\x1b[38;2;255;105;180m"
INDIAN_RED = "\x1b[38;2;205;92;92m"
INDIGO = "\x1b[38;2;75;0;130m"
IVORY = "\x1b[38;2;255;255;240m"
KHAKI = "\x1b[38;2;240;230;140m"
LAVENDER = "\x1b[38;2;230;230;250m"
LAVENDER_BLUSH = "\x1b[38;2;255;240;245m"
LAWN_GREEN = "\x1b[38;2;124;252;0m"
LEMON_CHIFFON = "\x1b[38;2;255;250;205m"
LIGHT_BLUE = "\x1b[38;2;173;216;230m"
LIGHT_CORAL = "\x1b[38;2;240;128;128m"
LIGHT_CYAN = "\x1b[38;2;224;255;255m"
LIGHT_GOLDENROD_YELLOW = "\x1b[38;2;250;250;210m"
LIGHT_GRAY = "\x1b[38;2;211;211;211m"
LIGHT_GREEN = "\x1b[38;2;144;238;144m"
LIGHT_PINK = "\x1b[38;2;255;182;193m"
LIGHT_SALMON = "\x1b[38;2;255;160;122m"
LIGHT_SEA_GREEN = "\x1b[38;2;32;178;170m"
LIGHT_SKY_BLUE = "\x1b[38;2;135;206;250m"
LIGHT_SLATE_GRAY = "\x1b[38;2;119;136;153m"
LIGHT_STEEL_BLUE = "\x1b[38;2;176;196;222m"
LIGHT_YELLOW = "\x1b[38;2;255;255;224m"
LIME = "\x1b[38;2;0;255;0m"
LIME_GREEN = "\x1b[38;2;50;205;50m"
LINEN = "\x1b[38;2;250;240;230m"
MAROON = "\x1b[38;2;128;0;0m"
MEDIUM_AQUAMARINE = "\x1b[38;2;102;205;170m"
MEDIUM_BLUE = "\x1b[38;2;0;0;205m"
MEDIUM_ORCHID = "\x1b[38;2;186;85;211m"
MEDIUM_PURPLE = "\x1b[38;2;147;112;219m"
MEDIUM_SEA_GREEN = "\x1b[38;2;60;179;113m"
MEDIUM_SLATE_BLUE = "\x1b[38;2;123;104;238m"
MEDIUM_SPRING_GREEN = "\x1b[38;2;0;250;154m"
MEDIUM_TURQUOISE = "\x1b[38;2;72;209;204m"
MEDIUM_VIOLET_RED = "\x1b[38;2;199;21;133m"
MIDNIGHT_BLUE = "\x1b[38;2;25;25;112m"
MINT_CREAM = "\x1b[38;2;245;255;250m"
MISTY_ROSE = "\x1b[38;2;255;228;225m"
MOCCASIN = "\x1b[38;2;255;228;181m"
NAVAJO_WHITE = "\x1b[38;2;255;222;173m"
NAVY = "\x1b[38;2;0;0;128m"
OLD_LACE = "\x1b[38;2;253;245;230m"
OLIVE = "\x1b[38;2;128;128;0m"
OLIVE_DRAB = "\x1b[38;2;107;142;35m"
ORANGE = "\x1b[38;2;255;165;0m"
ORANGE_RED = "\x1b[38;2;255;69;0m"
ORCHID = "\x1b[38;2;218;112;214m"
PALE_GOLDENROD = "\x1b[38;2;238;232;170m"
PALE_GREEN = "\x1b[38;2;152;251;152m"
PALE_TURQUOISE = "\x1b[38;2;175;238;238m"
PALE_VIOLET_RED = "\x1b[38;2;219;112;147m"
PAPAYA_WHIP = "\x1b[38;2;255;239;213m"
PEACH_PUFF = "\x1b[38;2;255;218;185m"
PERU = "\x1b[38;2;205;133;63m"
PINK = "\x1b[38;2;255;192;203m"
PLUM = "\x1b[38;2;221;160;221m"
POWDER_BLUE = "\x1b[38;2;176;224;230m"
PURPLE = "\x1b[38;2;128;0;128m"
ROSY_BROWN = "\x1b[38;2;188;143;143m"
ROYAL_BLUE = "\x1b[38;2;65;105;225m"
SADDLE_BROWN = "\x1b[38;2;139;69;19m"
SALMON = "\x1b[38;2;250;128;114m"
SANDY_BROWN = "\x1b[38;2;244;164;96m"
SEA_GREEN = "\x1b[38;2;46;139;87m"
SEA_SHELL = "\x1b[38;2;255;245;238m"
SIENNA = "\x1b[38;2;160;82;45m"
SILVER = "\x1b[38;2;192;192;192m"
SKY_BLUE = "\x1b[38;2;135;206;235m"
SLATE_BLUE = "\x1b[38;2;106;90;205m"
SLATE_GRAY = "\x1b[38;2;112;128;144m"
SNOW = "\x1b[38;2;255;250;250m"
SPRING_GREEN = "\x1b[38;2;0;255;127m"
STEEL_BLUE = "\x1b[38;2;70;130;180m"
TAN = "\x1b[38;2;210;180;140m"
TEAL = "\x1b[38;2;0;128;128m"
THISTLE = "\x1b[38;2;216;191;216m"
TOMATO = "\x1b[38;2;255;99;71m"
TURQUOISE = "\x1b[38;2;64;224;208m"
VIOLET = "\x1b[38;2;238;130;238m"
WHEAT = "\x1b[38;2;245;222;179m"
WHITE_SMOKE = "\x1b[38;2;245;245;245m"
YELLOW_GREEN = "\x1b[38;2;154;205;50m"
