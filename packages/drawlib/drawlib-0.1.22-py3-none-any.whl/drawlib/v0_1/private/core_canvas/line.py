# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Wrapper of matplotlib line draw

Matplotlib is difficult for just drawing line.
This module wraps it and provides easy to use interfaces.

"""

# pylint: disable=too-many-arguments

from typing import List, Tuple, Union
from matplotlib.path import Path
from matplotlib.patches import ConnectionStyle, FancyArrowPatch
from drawlib.v0_1.private.core.model import LineStyle, LineArrowStyle
from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.util import LineUtil
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core_canvas.base import CanvasBase
from drawlib.v0_1.private.validators.args import validate_args


class CanvasLineFeature(CanvasBase):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def line(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw line from xy1 to xy2.

        Args:
            xy1: start point.
            xy2: end point.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        # validation at here for better error message.
        # validated again at lines_bezier().

        validate_args(locals())

        self.lines_bezier(
            xy1,
            path_points=[xy2],
            style=style,
        )

    @error_handler
    def line_curved(
        self,
        xy1: Tuple[float, float],
        xy2: Tuple[float, float],
        bend: float,
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw curved line from xy1 to xy2.

        Args:
            xy1: start point.
            xy2: end point.
            bend: additional line length between xy1 and xy2. 0 is straight.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        # validate args

        validate_args(locals())
        style = LineUtil.format_style(style)
        options = LineUtil.get_fancyarrowpatch_options(style)
        self._artists.append(
            FancyArrowPatch(
                posA=xy1,
                posB=xy2,
                connectionstyle=ConnectionStyle.Arc3(rad=bend),
                **options,
            )
        )

    @error_handler
    def line_bezier1(
        self,
        xy1: Tuple[float, float],
        cp: Tuple[float, float],
        xy2: Tuple[float, float],
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw bezier line from xy1 to xy2. Control line via 1 control point.

        Args:
            xy1: start point.
            cp: control point.
            xy2: end point.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        # validation at here for better error message.
        # validated again at lines_bezier().

        validate_args(locals())
        self.lines_bezier(
            xy1,
            path_points=[(cp[0], cp[1], xy2[0], xy2[1])],
            style=style,
        )

    @error_handler
    def line_bezier2(
        self,
        xy1: Tuple[float, float],
        cp1: Tuple[float, float],
        cp2: Tuple[float, float],
        xy2: Tuple[float, float],
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw bezier line from xy1 to xy2. Control line via 2 control point.

        Args:
            xy1: start point.
            cp1: control point 1.
            cp2: control point 2.
            xy2: end point.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        # validation at here for better error message.
        # validated again at lines_bezier().

        validate_args(locals())
        self.lines_bezier(
            xy1,
            path_points=[(cp1[0], cp1[1], cp2[0], cp2[1], xy2[0], xy2[1])],
            style=style,
        )

    @error_handler
    def lines(
        self,
        xys: List[Tuple[float, float]],
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw line which paths provided xys.

        Args:
            xys: list of xy.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        # validation at here for better error message.
        # validated again at lines_bezier().

        validate_args(locals())
        self.lines_bezier(
            xy=xys[0],
            path_points=xys[1:],
            style=style,
        )

    @error_handler
    def lines_bezier(
        self,
        xy: Tuple[float, float],
        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[float, float, float, float],
                Tuple[float, float, float, float, float, float],
            ]
        ],
        style: Union[LineStyle, LineArrowStyle, str, None] = None,
    ) -> None:
        """Draw bezier line which paths provided path points.

        Args:
            xy: start point.
            path_points: path point and control points.
            style(optional): LineStyle or LineArrowStyle.

        Returns:
            None

        """

        validate_args(locals())
        style = LineUtil.format_style(style)

        # create Path
        vertices = [xy]
        codes = [Path.MOVETO]
        for p in path_points:
            length = len(p)
            if length not in [2, 4, 6]:
                raise ValueError()
            if length == 2:
                vertices.append((p[0], p[1]))
                codes.append(Path.LINETO)
            elif length == 4:
                vertices.extend([(p[0], p[1]), (p[2], p[3])])
                codes.extend([Path.CURVE3] * 2)
            else:
                vertices.extend([(p[0], p[1]), (p[2], p[3]), (p[4], p[5])])
                codes.extend([Path.CURVE4] * 3)
        path = Path(vertices=vertices, codes=codes)

        options = LineUtil.get_fancyarrowpatch_options(style)
        self._artists.append(FancyArrowPatch(path=path, **options))
