# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib image draw

Matplotlib is difficult for just drawing image.
This module wraps it and provides easy to use interfaces.

"""

from typing import Optional, List, Tuple, Literal, Union
from drawlib.v0_1.private.util import (
    error_handler,
    get_angle,
    get_distance,
)
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.validators.args import validate_args


class CanvasOriginalArrowFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def arrow(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        tail_width: float,
        head_width: float,
        head_length: float,
        head_style: Literal[
            "-|>",
            "<|-",
            "<|-|>",
        ] = "-|>",
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw sing and double heads arrow.

        Args:
            xy1: Arrow start point
            xy2: Arrow end point.
            tail_width: Arrow tail width.
            head_width: Arrow head width.
            head_length: Arrow head length.
            head_style(optional): Arrow head style. default is right head.
            style(optional): style of arc.
            text(optional): text which is shown at center of arc.
            textstyle(optional): style of text.

        Returns:
            None

        """

        # matplotlib FancyArrow, FancyArrowPatch seems not good
        # for implement this function.
        # Calculate arrow points pass it to shape().

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.arrowstyles.get,
            dtheme.arrowtextstyles.has,
            dtheme.arrowtextstyles.get,
        )

        x1, y1 = xy1
        x2, y2 = xy2
        x, y = ((x1 + x2) / 2, (y1 + y2) / 2)
        angle = get_angle(xy1, xy2)
        style.halign = "center"  # no choice
        style.valign = "center"  # no choice

        # arrow_tail_external_rectangle. left-bottom -> left-top ...
        distance = get_distance(xy1, xy2)
        p11 = (0, head_width / 2 - tail_width / 2)
        p12 = (0, head_width / 2 + tail_width / 2)
        p13 = (distance, head_width / 2 + tail_width / 2)
        p14 = (distance, head_width / 2 - tail_width / 2)

        # arrow_head_rectangle. left-bottom -> left-top ...
        distance2 = distance - head_length * 2
        p21 = (head_length, 0)
        p22 = (head_length, head_width)
        p23 = (head_length + distance2, head_width)
        p24 = (head_length + distance2, 0)

        # arrow_tail_internal_rectangle. left-bottom -> left-top ...
        p31 = (head_length, head_width / 2 - tail_width / 2)
        p32 = (head_length, head_width / 2 + tail_width / 2)
        p33 = (head_length + distance2, head_width / 2 + tail_width / 2)
        p34 = (head_length + distance2, head_width / 2 - tail_width / 2)

        # start, end
        p41 = (0, head_width / 2)
        p42 = (distance, head_width / 2)

        if head_style == "-|>":
            points = [p11, p12, p33, p23, p42, p24, p34]
        elif head_style == "<|-":
            points = [p41, p22, p32, p13, p14, p31, p21]
        elif head_style == "<|-|>":
            points = [p41, p22, p32, p33, p23, p42, p24, p34, p31, p21]
        else:
            raise Exception()

        self.shape(
            xy=(x, y),
            path_points=points,
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )
