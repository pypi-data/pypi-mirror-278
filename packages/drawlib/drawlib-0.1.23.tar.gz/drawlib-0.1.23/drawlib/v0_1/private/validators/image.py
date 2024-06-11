# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.


from typing import Union
from PIL.Image import Image
from drawlib.v0_1.private.core.dimage import Dimage


def validate_image(arg_name: str, value: Union[str, Image, Dimage]):
    message = f'Arg/Attr "{arg_name}" requires str or PIL.Image.Image or ShapeTextStyle. But "{value}" is given.'

    if isinstance(value, str):
        return
    elif isinstance(value, Image):
        return
    elif isinstance(value, Dimage):
        return
    else:
        raise ValueError(message)
