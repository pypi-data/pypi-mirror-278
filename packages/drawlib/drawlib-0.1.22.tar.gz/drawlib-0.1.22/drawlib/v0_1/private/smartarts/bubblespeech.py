# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from matplotlib.patches import Polygon

from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.model import *
from drawlib.v0_1.private.core_canvas.canvas import canvas
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.validators.args import validate_args


@error_handler
def bubblespeech(
    xy: Tuple[float, float],
    width: float,
    height: float,
    tail_edge: Literal["left", "top", "right", "bottom"],
    tail_from_ratio: float,
    tail_vertex_xy: Tuple[float, float],
    tail_to_ratio: float,
    style: Union[ShapeStyle, str, None] = None,
    text: str = "",
    textstyle: Union[ShapeTextStyle, str, None] = None,
) -> None:
    """Draw bubble speech.

    Almost same to rectangle. But having tail.

    Args:
        xy: always left bottom. Aligns are ignored.
        width: width of rectangle
        height: height of rectangle
        tail_edge: which edge tail exist.
        tail_start: ratio where tail start
        tail_vertex: vertex xy of tail.
        tail_width: ratio where tail end (start + width)
        style: ShapeStyle
        text: text
        textstyle: ShapeTextStyle

    Returns:
        None

    """

    validate_args(locals())
    style, textstyle = ShapeUtil.format_styles(
        style,
        textstyle,
        dtheme.bubblespeechstyles.get,
        dtheme.bubblespeechtextstyles.has,
        dtheme.bubblespeechtextstyles.get,
    )

    if tail_from_ratio > tail_to_ratio:
        raise ValueError("tail_from_ratio must be smaller than tail_to_ratio.")
    if tail_to_ratio > 1.0:
        raise ValueError(f"tail_from_ratio and tail_to_ratio must be smaller than 1.0")

    x, y = xy
    xys = []
    xys.append((x, y))  # left bottom
    if tail_edge == "left":
        xys.append((x, y + height * tail_from_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x, y + height * tail_to_ratio))
    xys.append((x, y + height))  # left top
    if tail_edge == "top":
        xys.append((x + width * tail_from_ratio, y + height))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_to_ratio, y + height))
    xys.append((x + width, y + height))  # right top
    if tail_edge == "right":
        xys.append((x + width, y + height * tail_to_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x + width, y + height * tail_from_ratio))
    xys.append((x + width, y))  # right bottom
    if tail_edge == "bottom":
        xys.append((x + width * tail_to_ratio, y))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_from_ratio, y))

    options = ShapeUtil.get_shape_options(style)
    canvas._artists.append(Polygon(xy=xys, closed=True, **options))

    if text:
        center_x = x + width / 2
        center_y = y + height / 2
        canvas._artists.append(
            ShapeUtil.get_shape_text(
                xy=(center_x, center_y),
                text=text,
                angle=0,
                style=textstyle,
            )
        )
