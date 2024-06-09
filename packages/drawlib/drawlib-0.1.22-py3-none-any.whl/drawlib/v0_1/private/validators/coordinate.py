# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


from typing import Tuple, Union, List


def validate_halign(name: str, value: str):
    supported = ["left", "center", "right"]
    if value not in supported:
        raise ValueError(f'Arg/Attr {name} must be one of {supported}. But "{value}" is given.')


def validate_valign(name: str, value: str):
    supported = ["bottom", "center", "top"]
    if value not in supported:
        raise ValueError(f'Arg/Attr {name} must be one of {supported}. But "{value}" is given.')


def validate_xy(arg_name: str, value: Tuple[float, float]) -> None:
    message = f'Arg/Attr "{arg_name}" must be (int/float, int/float) format. But "{value}" is given.'

    if not isinstance(value, tuple):
        raise ValueError(message)
    if len(value) != 2:
        raise ValueError(message)

    x, y = value
    for c in [x, y]:
        if not (isinstance(c, float) or isinstance(c, int)):
            raise ValueError(message)


def validate_xys(arg_name: str, value: List[Tuple[float, float]]) -> None:
    message = f'Arg/Attr "{arg_name}" must be list[tuple[int|float, int|float]] format. But "{value}" is given.'

    if not isinstance(value, list):
        raise ValueError(message)

    for e in value:
        if not isinstance(e, tuple):
            raise ValueError(message)
        if len(e) != 2:
            raise ValueError(message)

        x, y = e
        for c in [x, y]:
            if not (isinstance(c, float) or isinstance(c, int)):
                raise ValueError(message)


def validate_path_points(
    arg_name: str,
    value: List[
        Union[
            Tuple[float, float],
            Tuple[float, float, float, float],
            Tuple[float, float, float, float, float, float],
        ]
    ],
):
    message = f'Arg/Attr "{arg_name}" must be list[tuple[int|float, ..., int|float]] format. But "{value}" is given.'

    if not isinstance(value, list):
        raise ValueError()

    for e in value:
        if not isinstance(e, tuple):
            raise ValueError()
        if len(e) not in [2, 4, 6]:
            raise ValueError()

        for c in e:
            if not (isinstance(c, float) or isinstance(c, int)):
                raise ValueError()


def validate_angle(arg_name: str, value: Union[int, float]) -> None:
    message = f'Arg/Attr "{arg_name}" must be int/float 0~360. But "{value}" is given.'

    if isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(message)

    if not 0 <= value <= 360:
        raise ValueError(message)


def validate_angle_max90(arg_name: str, value: Union[int, float]) -> None:
    message = f'Arg/Attr "{arg_name}" must be int/float 0~90. But "{value}" is given.'

    if isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(message)

    if not 0 <= value <= 90:
        raise ValueError(message)
