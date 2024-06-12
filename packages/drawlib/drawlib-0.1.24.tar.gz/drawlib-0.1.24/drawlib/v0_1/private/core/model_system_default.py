from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.fonts import Font
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

SYSTEM_DEFAULT_ICON_STYLE = IconStyle(
    style="thin",
    color=Colors.Black,
    alpha=None,
    halign="center",
    valign="center",
)

SYSTEM_DEFAULT_IMAGE_STYLE = ImageStyle(
    halign="center",
    valign="center",
    lstyle="solid",
    lcolor=Colors.Black,
    lwidth=0,
    fcolor=None,
    alpha=None,
)

SYSTEM_DEFAULT_LINE_STYLE = LineStyle(
    width=1.0,
    style="solid",
    color=Colors.Black,
    alpha=None,
)

SYSTEM_DEFAULT_LINE_ARROW_STYLE = LineArrowStyle(
    lwidth=1.0,
    lstyle="solid",
    hstyle="->",
    hscale=20.0,
    color=Colors.Black,
    alpha=None,
)

SYSTEM_DEFAULT_SHAPE_STYLE = ShapeStyle(
    halign="center",
    valign="center",
    lwidth=1.0,
    lstyle="solid",
    lcolor=Colors.Black,
    fcolor=Colors.White,
    alpha=None,
)

SYSTEM_DEFAULT_SHAPE_TEXT_STYLE = ShapeTextStyle(
    alpha=None,
    color=Colors.Black,
    size=16,
    halign="center",
    valign="center",
    font=Font.SANSSERIF_REGULAR,
    angle=None,
    flip=False,
    xy_shift=None,
)

SYSTEM_DEFAULT_TEXT_STYLE = TextStyle(
    alpha=None,
    color=Colors.Black,
    size=16,
    halign="center",
    valign="center",
    font=Font.SANSSERIF_REGULAR,
    bgalpha=None,
    bgfcolor=None,
    # they will be applied if one of them is not None
    bglcolor=Colors.Black,
    bglstyle="solid",
    bglwidth=1.0,
)
