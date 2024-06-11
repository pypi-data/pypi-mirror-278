# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""drawlib utility module

This module contains utility functions which is called many points.
Regarding drawing utility functions, they are defined at ``core.util``.

"""

# pylint: disable=logging-fstring-interpolation

import inspect
import math
import functools
import traceback
import sys
import os
import os.path
import shutil
from typing import Any, Tuple, List

from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.dutil.settings import dutil_settings
import drawlib.assets.v0_1.fonts
import drawlib.assets.v0_1.fonticons


# Please don't set type annotation for this decorator function.
# It will break IDE args, return type suggestion.
def error_handler(caller):  # type: ignore[no-untyped-def]
    """drawlib error handling decorator function.

    This function decorates almost all functions in drawlib.
    When error happens, this function catch it and trace the call stack.
    After finding user code, it tells which files which line makes trouble.
    It is less information rather than normal error behavior.
    But useful for users who is not familiar with Python and programming.

    This function's action depends on logging mode.

    * quiet: Shows only where the user code makes error and error message. then exit with 1.
    * normal: Same to above.
    * verbose: Above + stacktrace
    * developer: Disable this error handling. Developer can see error at library level

    Note:
        Please don't apply this function to
        functions/methods which raise error and caller handles it.
        If you apply to them, this decorator catch the error and then exit.

    Note:
        Please don't apply this functions to module ``settings``.
        This module depends on that module.
        Circular import will happen if you do it.

    """

    @functools.wraps(caller)
    def wrapper(*args: Any, **kwargs: Any) -> None:
        if dutil_settings.is_developer_debug_mode():
            return caller(*args, **kwargs)

        try:
            return caller(*args, **kwargs)
        except Exception as e:  # pylint: disable=broad-exception-caught
            package_root = _get_package_root_path()
            for frame in inspect.stack():
                file = frame.filename
                if not os.path.isfile(file):
                    continue
                if _is_path_under(package_root, file):
                    continue
                line = frame.lineno
                logger.critical(f'{type(e).__name__} at file:"{file}", line:"{line}"')
                logger.critical(str(e))
                logger.debug("")
                logger.debug(traceback.format_exc())
                break
            sys.exit(1)

    return wrapper


@error_handler
def get_angle(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Get angle from (x1, y1) to (x2, y2)

    Get angle from (x1, y1) to (x2, y2)

    Args:
        x1: x of start point
        y1: y of start point
        x2: x of end point
        y2: y of end point

    Returns:
        float: angle between (x1, y1) and (x2, y2)

    """

    _validate_xy(name="xy1", value=xy1)
    _validate_xy(name="xy2", value=xy2)

    x1, y1 = xy1
    x2, y2 = xy2
    dx = x2 - x1
    dy = y2 - y1
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return (angle_deg + 360) % 360


@error_handler
def get_distance(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> float:
    """Get distance from (x1, y1) to (x2, y2)

    Get distance from (x1, y1) to (x2, y2)

    Args:
        x1: x of start point
        y1: y of start point
        x2: x of end point
        y2: y of end point

    Returns:
        float: distance between (x1, y1) and (x2, y2)

    """
    _validate_xy(name="xy1", value=xy1)
    _validate_xy(name="xy2", value=xy2)

    x1, y1 = xy1
    x2, y2 = xy2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


@error_handler
def get_center_and_size(xys: list[Tuple[float, float]]) -> Tuple[float, float]:

    _validate_xys(name="xys", value=xys)

    minx = xys[0][0]
    maxx = xys[0][0]
    miny = xys[0][1]
    maxy = xys[0][1]
    for x, y in xys:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2

    return ((center_x, center_y), (maxx - minx, maxy - miny))


@error_handler
def plus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    _validate_xy(name="xy1", value=xy1)
    _validate_xy(name="xy2", value=xy2)
    return (xy1[0] + xy2[0], xy1[1] + xy2[1])


@error_handler
def minus_2points(xy1: Tuple[float, float], xy2: Tuple[float, float]) -> Tuple[float, float]:
    _validate_xy(name="xy1", value=xy1)
    _validate_xy(name="xy2", value=xy2)
    return (xy1[0] - xy2[0], xy1[1] - xy2[1])


@error_handler
def get_script_path() -> str:
    """Get absolute path of user script which calls this function.

    Get absolute path of user script which calls this function.
    This function trace the stack till finding
    user script(it means the code outside of drawlib library).

    Returns:
        str: absolute path of last user script which call this function.

    """

    package_root = _get_package_root_path()
    script_path = ""
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if _is_path_under(package_root, file):
            continue
        script_path = file
        break

    if script_path == "":
        message = "Critical Error. Unable to detect call script file"
        raise FileNotFoundError(message)

    return script_path


@error_handler
def get_script_relative_path(path: str) -> str:
    """Get absolute file path from script file path.

    Merge "user script path" and "provided relative path".
    This function help specifying files/directory at user script.
    User doesn't need to take care whether the script is called.
    But just take care relative path from the file.

    Args:
        path: relative path from user script path

    Returns:
        str: Merged path of "user script path" and "provided relative path".

    """

    if not isinstance(path, str):
        raise ValueError(f'Arg "path" must be str. But {path} is given.')

    if os.path.isabs(path):
        return path

    script_path = get_script_path()
    script_parent_dir = os.path.dirname(script_path)
    merged_path = os.path.join(script_parent_dir, path)
    return os.path.realpath(merged_path)


@error_handler
def get_script_function_name() -> str:
    """Get user script function name which call this function.

    This function trace the stack till finding
    user script(it means the code outside of drawlib library).
    After finding it, returns the function name.

    Note:
        This function is used at unittest.

    Returns:
        str: function name of user script which call this function()

    """

    package_root = _get_package_root_path()
    for frame in inspect.stack():
        file = frame.filename
        if not os.path.isfile(file):
            continue
        if _is_path_under(package_root, file):
            continue
        return frame[3]

    msg = "Critical Error. Unable to get last called user function name"
    raise RuntimeError(msg)


@error_handler
def purge_font_cache():
    """Delete downloaded font file cache.

    Returns:
        None

    """

    fonts_dir_path = os.path.dirname(drawlib.assets.v0_1.fonts.__file__)
    fonticons_dir_path = os.path.dirname(drawlib.assets.v0_1.fonticons.__file__)

    for dir in [fonts_dir_path, fonticons_dir_path]:
        for file_name in os.listdir(dir):
            if file_name == "__init__.py":
                continue

            file_path = os.path.join(dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)


###############
### private ###
###############


def _get_package_root_path() -> str:
    """write docstring later"""

    first_module = inspect.stack()[0].filename
    module_path = os.path.abspath(first_module)
    package_root = module_path
    while not os.path.exists(os.path.join(package_root, "__init__.py")):
        package_root = os.path.dirname(package_root)
    return package_root


def _is_path_under(parent_path: str, child_path: str) -> bool:
    """write docstring later"""

    common_parent = os.path.commonpath([parent_path, child_path])
    abs_parent_path = os.path.abspath(parent_path)
    abs_common_path = os.path.abspath(common_parent)
    return abs_parent_path == abs_common_path


def _validate_xy(name: str, value: Tuple[float, float]):
    """write docstring later"""

    message = f'Arg "{name}" must be format (x, y). But {value} is given.'

    if not isinstance(value, tuple):
        raise ValueError(message)
    if len(value) != 2:
        raise ValueError(message)

    x, y = value
    for c in [x, y]:
        if not (isinstance(c, float) or isinstance(c, int)):
            raise ValueError(message)


def _validate_xys(name: str, value: List[Tuple[float, float]]):
    """write docstring later"""

    message = f'Arg "{name}" must be format list[(x1, y1), (x2, y2), ...]. But {value} is given.'

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
