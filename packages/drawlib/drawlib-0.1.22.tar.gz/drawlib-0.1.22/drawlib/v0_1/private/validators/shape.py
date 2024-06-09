# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


from typing import Union


def validate_num_vertex(arg_name: str, value: int) -> None:
    message = f'Arg/Attr "{arg_name}" must be int > 3. But "{value}" is given.'

    if not isinstance(value, int):
        raise ValueError(message)
    if value < 3:
        raise ValueError(message)


def validate_r(arg_name: str, value: Union[int, float]) -> None:
    message = f'Arg/Attr "{arg_name}" must be int|float >= 0. But "{value}" is given.'

    if isinstance(value, int) or isinstance(value, float):
        ...
    else:
        raise ValueError(message)

    if value < 0:
        raise ValueError(message)


def validate_head_style(arg_name: str, value: str) -> None:
    message = f'Arg/Attr "{arg_name}" must be one of "-|>","<|-","<|-|>". But "{value}" is given.'

    if not isinstance(value, str):
        raise ValueError(message)

    if value not in ["-|>", "<|-", "<|-|>"]:
        raise ValueError(message)
