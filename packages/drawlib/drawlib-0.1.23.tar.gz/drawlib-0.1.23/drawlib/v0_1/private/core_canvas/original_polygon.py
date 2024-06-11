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

import math
from typing import Optional, List, Tuple, Literal, Union
from matplotlib.text import Text
from matplotlib.patches import Polygon
from matplotlib.path import Path
from matplotlib.patches import PathPatch

from drawlib.v0_1.private.util import error_handler, minus_2points
from drawlib.v0_1.private.core.model import ShapeStyle, ShapeTextStyle
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.validators.args import validate_args


class CanvasOriginalPolygonFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    def triangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        topvertex_x: Optional[float] = None,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw triangle.

        Args:
            xy: default left bottom.
            width: width of triangle bottom
            height: height of traiangle
            topvertex_x(option): topvertex x coordinate from left side. default make it center.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.trianglestyles.get,
            dtheme.triangletextstyles.has,
            dtheme.triangletextstyles.get,
        )

        if topvertex_x is None:
            topvertex_x = width / 2
        p1 = (0, 0)
        p2 = (topvertex_x, height)
        p3 = (width, 0)
        self.shape(
            xy=xy,
            path_points=[p1, p2, p3],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def parallelogram(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: Union[int, float],
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ):
        """Draw parallelogram.

        Args:
            xy: default left bottom.
            width: width of triangle bottom
            height: height of traiangle
            corner_angle: left bottom corner angle.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.parallelogramstyles.get,
            dtheme.parallelogramtextstyles.has,
            dtheme.parallelogramtextstyles.get,
        )

        def calculate_parallelogram_lefttop_coordinate():
            angle_rad = math.radians(corner_angle)
            x = height / math.tan(angle_rad)
            return x, height

        p1 = (0, 0)
        p2 = calculate_parallelogram_lefttop_coordinate()
        p3 = (p2[0] + width, height)
        p4 = (width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def trapezoid(
        self,
        xy: Tuple[float, float],
        height: float,
        bottomedge_width: float,
        topedge_width: float,
        topedge_x: Optional[float] = None,
        angle: float = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ):
        """Draw triangle.

        Args:
            xy: default left bottom.
            height: height of traiangle
            bottomedge_width: width of bottom
            topedge_width: width of top
            topedge_x(optional): start point of top edge. Default makes top edge center.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.trapezoidstyles.get,
            dtheme.trapezoidtextstyles.has,
            dtheme.trapezoidtextstyles.get,
        )

        if topedge_x is None:
            topedge_x = (bottomedge_width - topedge_width) / 2
        p1 = (0, 0)
        p2 = (topedge_x, height)
        p3 = (topedge_x + topedge_width, height)
        p4 = (bottomedge_width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def rhombus(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ):
        """Draw rhombus.

        Args:
            xy: default left bottom.
            width: width of rhombus
            height: height of rhombus
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.rhombusstyles.get,
            dtheme.rhombustextstyles.has,
            dtheme.rhombustextstyles.get,
        )

        p1 = (0, height / 2)
        p2 = (width / 2, height)
        p3 = (width, height / 2)
        p4 = (width / 2, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def chevron(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        corner_angle: float,
        mirror: bool = False,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw chevron.

        Vertex is right on default. Provide True for mirror makes left side vertex.

        Args:
            xy: default left bottom.
            width: width of bottom of chevron
            height: height of chevron
            corner_angle: left bottom corner angle. 0.0 ~ 90.0.
            mirror(optional): make vertex left side.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.chevronstyles.get,
            dtheme.chevrontextstyles.has,
            dtheme.chevrontextstyles.get,
        )

        if mirror:
            corner_angle = 180 - corner_angle

        p1 = (0, 0)
        p2x = height / 2 * math.cos(math.radians(corner_angle))
        p2 = (p2x, height / 2)
        p3 = (0, height)
        p4 = (width, height)
        p5 = (width + p2x, height / 2)
        p6 = (width, 0)

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6],
            angle=angle,
            style=style,
            text=text,
            textstyle=textstyle,
        )

    def star(
        self,
        xy: Tuple[float, float],
        num_vertex: int,
        radius_ext: float,
        radius_int: float,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw star.

        Args:
            xy: default center, center.
            num_vertex: numver of external vertex. 3 ~.
            radius_ext: radius of external vertex.
            radius_int: raidus of internal vertex.
            angle(optional): rotate degree
            style(optional): style of shape.
            text(optional): center text.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.starstyles.get,
            dtheme.startextstyles.has,
            dtheme.startextstyles.get,
        )
        if radius_ext < radius_int:
            raise ValueError("radius_ext must be bigger than radius_int.")

        # helper

        def get_rotate_point(x: float, y: float, angle: Optional[float], move_x: float, move_y: float):
            if angle is None:
                angle = 0.0
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

        # calculate points

        points = []
        start_angle = math.pi / 2
        for i in range(2 * num_vertex):
            r = radius_ext if i % 2 == 0 else radius_int
            point_angle = start_angle + i * 2 * math.pi / (2 * num_vertex)
            x = r * math.cos(point_angle)
            y = r * math.sin(point_angle)
            points.append((x, y))

        # move x, y which fit to alignment

        width = radius_ext * 2
        height = radius_ext * 2
        x, y = xy
        x -= width / 2
        y -= height / 2
        xy = (x, y)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy,
            width,
            height,
            angle,
            style,
            is_default_center=True,
        )

        # shift

        cx = x + width / 2
        cy = y + height / 2
        points2 = []
        for pp in points:
            x1, y1 = get_rotate_point(x=pp[0], y=pp[1], angle=angle, move_x=cx, move_y=cy)
            points2.append((x1, y1))

        # create Path

        vertices = [points2[0]]
        codes = [Path.MOVETO]
        for p in points2[1:]:
            vertices.append((p[0], p[1]))
            codes.append(Path.LINETO)
        vertices.append(points2[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )
