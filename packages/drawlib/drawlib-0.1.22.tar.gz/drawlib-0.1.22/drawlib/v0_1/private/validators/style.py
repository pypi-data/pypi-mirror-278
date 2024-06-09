# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from typing import Union

from drawlib.v0_1.private.core.model import (
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ImageStyle,
    IconStyle,
)


def validate_iconstyle(name: str, value: IconStyle):
    if not isinstance(value, IconStyle):
        raise ValueError(f'Arg/Attr "{name}" requires IconStyle. But "{value}" is given.')


def validate_imagestyle(name: str, value: ImageStyle):
    if not isinstance(value, ImageStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ImageStyle. But "{value}" is given.')


def validate_linestyle(name: str, value: LineStyle):
    if not isinstance(value, LineStyle):
        raise ValueError(f'Arg/Attr "{name}" requires LineStyle. But "{value}" is given.')


def validate_linearrowstyle(name: str, value: LineArrowStyle):
    if not isinstance(value, LineArrowStyle):
        raise ValueError(f'Arg/Attr "{name}" requires LineArrowStyle. But "{value}" is given.')


def validate_linestyle_or_linearrowstyle(name: str, value: Union[LineStyle, LineArrowStyle]):
    if isinstance(value, LineStyle):
        ...
    elif isinstance(value, LineArrowStyle):
        ...
    else:
        raise ValueError(f'Arg/Attr "{name}" requires LineStyle or LineArrowStyle. But "{value}" is given.')


def validate_shapestyle(name: str, value: ShapeStyle):
    if not isinstance(value, ShapeStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ShapeStyle. But "{value}" is given.')


def validate_shapetextstyle(name: str, value: ShapeTextStyle):
    if not isinstance(value, ShapeTextStyle):
        raise ValueError(f'Arg/Attr "{name}" requires ShapeTextStyle. But "{value}" is given.')


def validate_textstyle(name: str, value: TextStyle):
    if not isinstance(value, TextStyle):
        raise ValueError(f'Arg/Attr "{name}" requires TextStyle. But "{value}" is given.')
