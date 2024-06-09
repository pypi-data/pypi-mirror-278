# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib shape draw

Matplotlib is difficult for just drawing shapes.
This module wraps it and provides easy to use interfaces.

"""

# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

from typing import Optional, List, Tuple, Union
import math
from matplotlib.patches import (
    Arc,
    Circle,
    Ellipse,
    Polygon,
    RegularPolygon,
    FancyBboxPatch,
    Wedge,
)
import matplotlib as mpl

from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.util import error_handler, get_center_and_size
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.validators.args import validate_args


class CanvasPatchesFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def arc(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        from_angle: Union[int, float] = 0.0,
        to_angle: Union[int, float] = 360.0,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw arc.

        Args:
            xy: center of arc.
            width: width of arc.
            height: height of arc.
            from_angle(optional): where drawing arc start. default is angle 0.0
            to_angle(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate arc with specified angle
            style(optional): style of arc.
            text(optional): text which is shown at center of arc.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.arcstyles.get,
            dtheme.arctextstyles.has,
            dtheme.arctextstyles.get,
        )

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style, default_no_line=False)
        self._artists.append(
            Arc(
                xy,
                width=width,
                height=height,
                angle=angle,
                theta1=from_angle,
                theta2=to_angle,
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def circle(
        self,
        xy: Tuple[float, float],
        radius: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw cicle.

        Args:
            xy: center of circle.
            radius: radius of circle.
            angle(optional): rotate inside text with specified angle
            style(optional): style of circle.
            text(optional): text which is shown at center of arc.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.circlestyles.get,
            dtheme.circletextstyles.has,
            dtheme.circletextstyles.get,
        )

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Circle(
                xy=xy,
                radius=radius,
                **options,
            ),
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def ellipse(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw ellipse

        Args:
            xy: center of ellipse
            width: width of ellipse.
            height: height of ellipse.
            angle(optional): rotate ellipse with specified angle.
            style(optional): style of arc.
            text(optional): text which is shown at center of ellipse.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals(), argnames_accept_none=["text"])
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.ellipsestyles.get,
            dtheme.ellipsestyles.has,
            dtheme.ellipsetextstyles.get,
        )

        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Ellipse(
                xy=xy,
                width=width,
                height=height,
                angle=angle,
                **options,
            ),
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def polygon(
        self,
        xys: List[Tuple[float, float]],
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw polygon.

        Args:
            xys: List of points. [(x1, y1), ...(x_n, y_n)].
            style(optional): style of polygon.
            text(optional): text which is shown at center of ellipse.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.polygonstyles.get,
            dtheme.polygontextstyles.has,
            dtheme.polygontextstyles.get,
        )

        style.halign = None
        style.valign = None
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(Polygon(xy=xys, closed=True, **options))

        if not text:
            return
        center, (_, _) = get_center_and_size(xys)
        self._artists.append(
            ShapeUtil.get_shape_text(
                center,
                text=text,
                angle=0,
                style=textstyle,
            ),
        )

    @error_handler
    def regularpolygon(
        self,
        xy: Tuple[float, float],
        radius: float,
        num_vertex: int,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw regular polygon.

        Args:
            xy: center of regular polygon
            radius: radius of regular polygon's vertex.
            num_vertex: number of vertex.
            style(optional): style of regular polygon.
            angle(optional): rotation angle
            text(optional): text which is shown at center of regular polygon.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.regularpolygonstyles.get,
            dtheme.regularpolygontextstyles.has,
            dtheme.regularpolygontextstyles.get,
        )

        width = radius * 2
        height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, width, height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            RegularPolygon(
                xy,
                radius=radius,
                numVertices=num_vertex,
                orientation=math.radians(angle),
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def rectangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        r: float = 0.0,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw rectangle

        Args:
            xy: left bottom of rectangle.
            width: width of rounded rectangle.
            height: height of rounded rectangle.
            r(optional): size of R. default is 0.0.
            angle(optional): rotate rectangle with specified angle. Requires Matplotlib's ax to achieve it.
            style(optional): style of rounded rectangle.
            text(optional): text which is shown at center of rounded rectangle.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.rectanglestyles.get,
            dtheme.rectangletextstyles.has,
            dtheme.rectangletextstyles.get,
        )

        (x, y), style = ShapeUtil.apply_alignment(xy, width, height, angle, style)
        options = ShapeUtil.get_shape_options(style)
        rectangle = FancyBboxPatch(
            (x + r, y + r),
            width - r * 2,
            height - r * 2,
            boxstyle=f"round,pad={r}",
            **options,
        )
        if angle != 0:
            cx = x + width / 2
            cy = y + height / 2
            t2 = mpl.transforms.Affine2D().rotate_deg_around(cx, cy, angle) + self._ax.transData
            rectangle.set_transform(t2)
        self._artists.append(rectangle)

        if not text:
            return
        center_x = x + width / 2
        center_y = y + height / 2
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=(center_x, center_y),
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def wedge(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        from_angle: float = 0,
        to_angle: float = 360,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw wedge

        Args:
            xy: center of wedge
            radius: radius of wedge.
            width(optional): length from outer to inner circumference. default is same to radius value.
            from_angle(optional): where drawing arc start. default is angle 0.0
            to_angle(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        validate_args(locals(), argnames_accept_none=["width"])
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.wedgestyles.get,
            dtheme.wedgetextstyles.has,
            dtheme.wedgetextstyles.get,
        )

        ext_width = radius * 2
        ext_height = radius * 2
        xy, style = ShapeUtil.apply_alignment(xy, ext_width, ext_height, angle, style, is_default_center=True)
        options = ShapeUtil.get_shape_options(style)
        self._artists.append(
            Wedge(
                center=xy,
                r=radius,
                width=width,  # None makes no hole
                theta1=from_angle + angle,
                theta2=to_angle + angle,
                **options,
            )
        )

        if not text:
            return
        self._artists.append(
            ShapeUtil.get_shape_text(
                xy=xy,
                text=text,
                angle=angle,
                style=textstyle,
            ),
        )

    @error_handler
    def donuts(
        self,
        xy: Tuple[float, float],
        radius: float,
        width: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw donuts

        Args:
            xy: center of donuts
            radius: radius of donuts.
            width(optional): length from outer to inner circumference. default is same to radius value.
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        validate_args(locals(), argnames_accept_none=["width"])
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.donutsstyles.get,
            dtheme.donutstextstyles.has,
            dtheme.donutstextstyles.get,
        )

        self.wedge(
            xy=xy,
            radius=radius,
            width=width,
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    @error_handler
    def fan(
        self,
        xy: Tuple[float, float],
        radius: float,
        from_angle: float = 0,
        to_angle: float = 180,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw fan

        Args:
            xy: center of fan
            radius: radius of fan.
            from_angle(optional): where drawing arc start. default is angle 0.0
            to_angle(optional): where drawing arc end. default is angle 360.0
            angle(optional): rotate wedge with specified angle
            style(optional): style of wedge.
            text(optional): text which is shown at center of wedge.
            textstyle(optional): style of text.

        Returns:
            None.

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.fanstyles.get,
            dtheme.fantextstyles.has,
            dtheme.fantextstyles.get,
        )

        self.wedge(
            xy=xy,
            radius=radius,
            width=None,
            from_angle=from_angle,
            to_angle=to_angle,
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )
