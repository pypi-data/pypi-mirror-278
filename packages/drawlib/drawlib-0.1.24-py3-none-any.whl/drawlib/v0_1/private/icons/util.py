# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawing icon utility module

If you want to draw your specific font icon, please use function dicon

"""

import typing
from drawlib.v0_1.private.core.fonts import FontFile
from drawlib.v0_1.private.core.model import IconStyle, TextStyle
from drawlib.v0_1.private.core.util import IconUtil
from drawlib.v0_1.private.core_canvas.canvas import text, get_fontsize_from_charwidth
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.validators.args import validate_args


def icon(
    xy: typing.Tuple[float, float],
    width: float,
    code: str,
    file: str,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[IconStyle, str, None] = None,
) -> None:
    """Draw provided iconfont's icon.

    Args:
        code: code point
        font_file: font file path
        x: default align left if angle is not specified. center if specified.
        y: default align bottom if angle is not specified. center if specified.
        width: icon width. icon might have transparent space on itself.
        angle(optional): rotation angle. 0.0 ~ 360.0.
        style(optional): icon style. Allignment etc.

    Returns:
        None

    """

    validate_args(locals())
    style = IconUtil.format_style(style)
    font_size = get_fontsize_from_charwidth(width)

    # convert IconStyle to TextStyle
    textstyle = TextStyle(
        color=style.color,
        size=font_size,
        font=FontFile(file),
        halign=style.halign,
        valign=style.valign,
    )

    # draw icon as text
    text(xy=xy, text=code, angle=angle, style=textstyle)
