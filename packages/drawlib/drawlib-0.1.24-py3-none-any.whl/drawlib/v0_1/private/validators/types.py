# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


from typing import Union


def validate_bool(arg_name: str, value: bool) -> None:
    message = f'Arg/Attr "{arg_name}" must be bool. But "{value}" is given.'

    if not isinstance(value, bool):
        raise ValueError(message)


def validate_plus_int(arg_name: str, value: int, is_0_ok=True) -> None:

    if not isinstance(value, int):
        raise ValueError(f'Arg/Attr "{arg_name}" must be int >= 0. But "{value}" is given.')

    if not is_0_ok:
        if 0 >= value:
            raise ValueError(f'Arg/Attr "{arg_name}" must be int > 0. But "{value}" is given.')


def validate_plus_float(arg_name: str, value: Union[int, float], is_0_ok=True) -> None:

    if isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(f'Arg/Attr "{arg_name}" must be int/float >= 0. But "{value}" is given.')

    if not is_0_ok:
        if 0 >= value:
            raise ValueError(f'Arg/Attr "{arg_name}" must be int/float > 0. But "{value}" is given.')


def validate_float_0_to_1(name: str, value: int, is_0_ok=True) -> None:
    message = f'Arg/Attr "{name}" must be between 0.0~1.0. But "{value}" is given.'

    if isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(message)

    if not 0.0 <= value <= 1.0:
        raise ValueError(message)


def validate_plusminus_float_or_none(arg_name: str, value: Union[int, float, None]) -> None:
    message = f'Arg/Attr "{arg_name}" must be int/float. But "{value}" is given.'

    if value is None:
        ...
    elif isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(message)


def validate_str(arg_name: str, value: str) -> None:
    message = f'Arg/Attr "{arg_name}" must be str. But "{value}" is given.'

    if not isinstance(value, str):
        raise ValueError(message)
