# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""wrapper of writing phosphor font icons

Supports phosphor v2.1 icons.
This code is auto generated.

"""

import os
import typing
import urllib.parse
import drawlib.assets.v0_1.fonticons
import drawlib.v0_1.private.core.model
import drawlib.v0_1.private.core.util
import drawlib.v0_1.private.icons.util
import drawlib.v0_1.private.util
import drawlib.v0_1.private.download
import drawlib.v0_1.private.core.theme


def _get_fontfile_tuple(path: str, md5_hash: str) -> typing.Tuple[str, str, str]:
    paths = [p for p in path.split("/") if p]

    # font path
    dir_path = os.path.dirname(drawlib.assets.v0_1.fonticons.__file__)
    font_path = os.path.join(dir_path, *paths)

    # url
    url = urllib.parse.urljoin(
        "https://raw.githubusercontent.com/yuichi110/drawlib_assets/main/assets/v0_1/fonticons/",
        "/".join(paths),
    )

    return (font_path, url, md5_hash)


def _get_font_path(style: str) -> str:

    file_path, download_url, md5_hash = {
        "thin": _get_fontfile_tuple("phosphor/thin.ttf", "9ca0acf8bc84ec2421f96f835017f321"),
        "light": _get_fontfile_tuple("phosphor/light.ttf", "6c53da4ecc310dd5dbcfafe3d916a346"),
        "regular": _get_fontfile_tuple("phosphor/regular.ttf", "c2ecd49d10b76c3f9b9c072966cc0c3c"),
        "bold": _get_fontfile_tuple("phosphor/bold.ttf", "4f59e81563e413635c57d78338d33b92"),
        "fill": _get_fontfile_tuple("phosphor/fill.ttf", "612af00267f5e8a429531399700db66e"),
    }[style]

    # download if local cache doesn't exist
    drawlib.v0_1.private.download.download_if_not_exist(
        file_path=file_path,
        download_url=download_url,
        md5_hash=md5_hash,
    )

    return file_path


def _write(
    xy: typing.Tuple[float, float],
    width: float,
    code: str,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:

    style = drawlib.v0_1.private.core.util.IconUtil.format_style(
        style=style,
        default_icon_style="thin",
    )

    # style.style varies on icon types.
    # check whther it is supported on this set.
    if style.style not in ["thin", "light", "regular", "bold", "fill"]:
        raise ValueError(f'icon_phosphor does not support style "{style.style}".')

    # set icon file path
    file = _get_font_path(style.style)

    # draw phosphor icon with generic function
    drawlib.v0_1.private.icons.util.icon(
        xy=xy,
        width=width,
        code=code,
        file=file,
        angle=angle,
        style=style,
    )


#####################################
### Auto generated code from here ###
#####################################


@drawlib.v0_1.private.util.error_handler
def acorn(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon acorn. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb9a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def address_book(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon address-book. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def address_book_tabs(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon address-book-tabs. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee4e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def air_traffic_control(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon air-traffic-control. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecd8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue002", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane_in_flight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane-in-flight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane_landing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane-landing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue502", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane_takeoff(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane-takeoff. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue504", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane_taxiing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane-taxiing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue500", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplane_tilt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplane-tilt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def airplay(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon airplay. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue004", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def alarm(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon alarm. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue006", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def alien(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon alien. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_bottom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-bottom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue506", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_bottom_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-bottom-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb0c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_center_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-center-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue50a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_center_horizontal_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-center-horizontal-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb0e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_center_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-center-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue50c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_center_vertical_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-center-vertical-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb10", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue50e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_left_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-left-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue510", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_right_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-right-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb12", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_top(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-top. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue512", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def align_top_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon align-top-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb14", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def amazon_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon amazon-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue96c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ambulance(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ambulance. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue572", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def anchor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon anchor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue514", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def anchor_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon anchor-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def android_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon android-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue008", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def angle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon angle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def angular_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon angular-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb80", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def aperture(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon aperture. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue00a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def app_store_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon app-store-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue974", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def app_window(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon app-window. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def apple_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon apple-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue516", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def apple_podcasts_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon apple-podcasts-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb96", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def approximate_equals(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon approximate-equals. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedaa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def archive(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon archive. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue00c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def armchair(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon armchair. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue012", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_arc_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-arc-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue014", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_arc_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-arc-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue016", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_double_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-double-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue03a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_double_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-double-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue03c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue018", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue01a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_left_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-left-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue01c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_left_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-left-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue01e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_right_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-right-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue020", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_right_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-right-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue022", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue024", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_bend_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-bend-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue026", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue028", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue02a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue02c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue05a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue02e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue030", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue032", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_circle_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-circle-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue034", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue036", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_counter_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-counter-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue038", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue03e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue040", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue042", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue044", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue046", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue048", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_left_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-left-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue04a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_left_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-left-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue04c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue04e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_right_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-right-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue050", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_right_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-right-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue052", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue054", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_elbow_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-elbow-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue056", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue518", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue51a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_line_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-line-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue51c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_line_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-line-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue51e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_line_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-line-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue520", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_line_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-line-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue522", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_lines_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-lines-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue524", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_lines_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-lines-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue526", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_lines_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-lines-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue528", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_lines_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-lines-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue52a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue52c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_fat_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-fat-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue52e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue058", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue05c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue05e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue060", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue062", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue064", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue066", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue068", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_line_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-line-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue06a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue06c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue06e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue070", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue072", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_in(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-in. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue074", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_out(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-out. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue076", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue078", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue07a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_square_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-square-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue07c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_down_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-down-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue07e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_down_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-down-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue080", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_left_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-left-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue082", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_left_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-left-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue084", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_right_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-right-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue086", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_right_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-right-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue088", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue08a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_u_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-u-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue08c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue08e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_up_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-up-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue090", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrow_up_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrow-up-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue092", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue094", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_counter_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-counter-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue096", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_down_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-down-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue098", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb06", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_in(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-in. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue09a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_in_cardinal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-in-cardinal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue09c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_in_line_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-in-line-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue530", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_in_line_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-in-line-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue532", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_in_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-in-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue09e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_left_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-left-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_merge(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-merge. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued3e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_out(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-out. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_out_cardinal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-out-cardinal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_out_line_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-out-line-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue534", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_out_line_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-out-line-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue536", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_out_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-out-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_split(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-split. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued3c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def arrows_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon arrows-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb04", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def article(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon article. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def article_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon article-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def article_ny_times(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon article-ny-times. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def asclepius(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon asclepius. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caduceus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caduceus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def asterisk(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon asterisk. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def asterisk_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon asterisk-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue832", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def at(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon at. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def atom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon atom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def avocado(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon avocado. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee04", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def axe(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon axe. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def baby(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon baby. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue774", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def baby_carriage(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon baby-carriage. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue818", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def backpack(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon backpack. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue922", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def backspace(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon backspace. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bag_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bag-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def balloon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon balloon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue76c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bandaids(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bandaids. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bank(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bank. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def barbell(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon barbell. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def barcode(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon barcode. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def barn(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon barn. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec72", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def barricade(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon barricade. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue948", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def baseball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon baseball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue71a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def baseball_cap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon baseball-cap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea28", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def baseball_helmet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon baseball-helmet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee4a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def basket(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon basket. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue964", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def basketball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon basketball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue724", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bathtub(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bathtub. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue81e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_charging(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-charging. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_charging_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-charging-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_empty(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-empty. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_full(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-full. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue808", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_plus_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-plus-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec50", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_vertical_empty(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-vertical-empty. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_vertical_full(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-vertical-full. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_vertical_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-vertical-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_vertical_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-vertical-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_vertical_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-vertical-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def battery_warning_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon battery-warning-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def beach_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon beach-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued24", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def beanie(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon beanie. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea2a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def beer_bottle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon beer-bottle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def beer_stein(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon beer-stein. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb62", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def behance_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon behance-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_ringing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-ringing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_simple_ringing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-simple-ringing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_simple_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-simple-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_simple_z(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-simple-z. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bell_z(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bell-z. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def belt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon belt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea2c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bezier_curve(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bezier-curve. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb00", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bicycle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bicycle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def binary(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon binary. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee60", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def binoculars(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon binoculars. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea64", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def biohazard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon biohazard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bird(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bird. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue72c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def blueprint(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon blueprint. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueda0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bluetooth(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bluetooth. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bluetooth_connected(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bluetooth-connected. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bluetooth_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bluetooth-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bluetooth_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bluetooth-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def boat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon boat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue786", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bomb(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bomb. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee0a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def book(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon book. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def book_bookmark(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon book-bookmark. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def book_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon book-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def book_open_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon book-open-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def book_open_user(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon book-open-user. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uede0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bookmark(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bookmark. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bookmark_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bookmark-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bookmarks(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bookmarks. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bookmarks_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bookmarks-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def books(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon books. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue758", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def boot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon boot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def boules(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon boules. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue722", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bounding_box(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bounding-box. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bowl_food(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bowl-food. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaa4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bowl_steam(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bowl-steam. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bowling_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bowling-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def box_arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon box-arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue00e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def archive_box(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon archive-box. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue00e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def box_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon box-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee54", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def boxing_glove(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon boxing-glove. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea36", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brackets_angle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brackets-angle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue862", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brackets_curly(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brackets-curly. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue860", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brackets_round(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brackets-round. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue864", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brackets_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brackets-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue85e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brain(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brain. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue74e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def brandy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon brandy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bread(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bread. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue81c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bridge(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bridge. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea68", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def briefcase(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon briefcase. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def briefcase_metal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon briefcase-metal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def broadcast(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon broadcast. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def broom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon broom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec54", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def browser(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon browser. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def browsers(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon browsers. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bug(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bug. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bug_beetle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bug-beetle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bug_droid(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bug-droid. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def building(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon building. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue100", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def building_apartment(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon building-apartment. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def building_office(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon building-office. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0ff", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def buildings(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon buildings. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue102", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bulldozer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bulldozer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec6c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def bus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon bus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue106", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def butterfly(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon butterfly. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea6e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cable_car(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cable-car. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue49c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cactus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cactus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue918", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cake(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cake. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue780", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calculator(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calculator. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue538", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue108", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_blank(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-blank. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue10a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue712", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_dot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-dot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_dots(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-dots. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_heart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-heart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea14", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue714", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea12", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def calendar_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon calendar-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue10c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def call_bell(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon call-bell. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def camera(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon camera. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue10e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def camera_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon camera-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec58", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def camera_rotate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon camera-rotate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def camera_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon camera-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue110", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def campfire(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon campfire. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def car(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon car. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue112", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def car_battery(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon car-battery. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee30", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def car_profile(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon car-profile. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def car_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon car-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue114", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cardholder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cardholder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cards(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cards. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue0f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cards_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cards-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee50", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_double_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-double-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue116", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_double_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-double-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue118", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_double_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-double-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue11a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_double_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-double-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue11c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue11e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue120", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue122", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue124", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_circle_up_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-circle-up-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue13e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_double_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-double-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue126", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_double_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-double-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue128", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_double_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-double-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue12a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_double_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-double-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue12c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue136", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue138", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_line_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-line-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue134", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_line_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-line-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue132", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_line_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-line-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue130", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_line_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-line-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue12e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue13a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue13c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def caret_up_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon caret-up-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue140", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def carrot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon carrot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued38", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cash_register(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cash-register. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued80", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cassette_tape(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cassette-tape. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued2e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def castle_turret(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon castle-turret. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue748", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_full(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-full. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue142", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue144", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue146", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue148", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_none(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-none. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue14a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue14c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_signal_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-signal-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue14e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cell_tower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cell-tower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebaa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def certificate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon certificate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue766", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chair(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chair. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue950", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chalkboard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chalkboard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chalkboard_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chalkboard-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chalkboard_teacher(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chalkboard-teacher. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue600", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def champagne(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon champagne. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def charging_station(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon charging-station. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_bar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-bar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue150", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_bar_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-bar-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue152", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_donut(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-donut. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaa6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue154", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_line_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-line-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_line_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-line-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue156", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_pie(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-pie. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue158", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_pie_slice(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-pie-slice. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue15a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_polar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-polar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaa8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chart_scatter(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chart-scatter. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue15c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_centered(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-centered. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue160", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_centered_dots(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-centered-dots. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue164", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_centered_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-centered-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue162", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_centered_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-centered-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue166", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue168", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_circle_dots(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-circle-dots. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue16c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_circle_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-circle-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue16a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_circle_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-circle-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue16e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_dots(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-dots. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue170", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue15e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_teardrop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-teardrop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue172", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_teardrop_dots(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-teardrop-dots. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue176", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_teardrop_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-teardrop-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue174", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_teardrop_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-teardrop-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue178", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chat_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chat-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue17a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chats(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chats. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue17c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chats_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chats-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue17e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chats_teardrop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chats-teardrop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue180", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue182", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def check_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon check-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue184", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def check_fat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon check-fat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueba6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def check_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon check-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue186", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def check_square_offset(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon check-square-offset. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue188", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def checkerboard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon checkerboard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def checks(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon checks. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue53a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cheers(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cheers. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea4a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cheese(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cheese. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def chef_hat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon chef-hat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued8e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cherries(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cherries. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue830", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def church(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon church. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cigarette(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cigarette. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued90", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cigarette_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cigarette-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued92", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue18a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue602", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_half(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-half. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue18c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_half_tilt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-half-tilt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue18e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_notch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-notch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb44", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circles_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circles-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue190", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circles_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circles-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue192", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circles_three_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circles-three-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue194", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circuitry(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circuitry. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def city(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon city. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea6a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clipboard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clipboard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue196", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clipboard_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clipboard-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue198", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue19a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock_afternoon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock-afternoon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue19c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue19e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock_countdown(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock-countdown. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued2c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock_counter_clockwise(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock-counter-clockwise. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clock_user(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clock-user. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def closed_captioning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon closed-captioning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_fog(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-fog. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue53c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_lightning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-lightning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_moon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-moon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue53e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_rain(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-rain. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_snow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-snow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_sun(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-sun. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue540", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea98", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cloud_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cloud-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea96", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def clover(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon clover. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedc8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def club(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon club. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coat_hanger(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coat-hanger. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coda_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coda-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def code(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon code. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def code_block(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon code-block. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueafe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def code_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon code-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def codepen_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon codepen-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue978", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def codesandbox_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon codesandbox-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea06", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coffee(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coffee. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coffee_bean(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coffee-bean. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coin(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coin. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue60e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coin_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coin-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb48", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def coins(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon coins. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue78e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def columns(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon columns. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue546", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def columns_plus_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon columns-plus-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue544", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def columns_plus_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon columns-plus-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue542", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def command(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon command. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def compass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon compass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def compass_rose(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon compass-rose. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def compass_tool(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon compass-tool. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea0e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def computer_tower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon computer-tower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue548", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def confetti(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon confetti. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue81a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def contactless_payment(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon contactless-payment. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued42", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def control(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon control. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueca6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cookie(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cookie. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cooking_pot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cooking-pot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue764", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def copy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon copy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def copy_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon copy-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def copyleft(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon copyleft. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue86a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def copyright(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon copyright. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue54a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def corners_in(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon corners-in. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def corners_out(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon corners-out. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def couch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon couch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def court_basketball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon court-basketball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee36", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueabe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cowboy_hat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cowboy-hat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued12", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cpu(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cpu. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue610", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crane(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crane. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued48", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crane_tower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crane-tower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued49", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def credit_card(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon credit-card. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cricket(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cricket. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee12", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cross(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cross. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crosshair(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crosshair. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crosshair_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crosshair-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crown(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crown. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue614", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crown_cross(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crown-cross. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee5e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def crown_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon crown-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue616", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cube(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cube. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cube_focus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cube-focus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued0a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cube_transparent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cube-transparent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec7c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_btc(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-btc. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue618", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_circle_dollar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-circle-dollar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue54c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_cny(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-cny. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue54e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_dollar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-dollar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue550", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_dollar_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-dollar-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue552", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_eth(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-eth. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueada", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_eur(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-eur. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue554", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_gbp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-gbp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue556", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_inr(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-inr. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue558", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_jpy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-jpy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue55a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_krw(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-krw. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue55c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_kzt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-kzt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec4c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_ngn(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-ngn. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb52", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def currency_rub(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon currency-rub. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue55e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cursor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cursor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cursor_click(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cursor-click. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cursor_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cursor-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def cylinder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon cylinder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def database(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon database. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def desk(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon desk. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued16", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def desktop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon desktop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue560", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def desktop_tower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon desktop-tower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue562", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def detective(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon detective. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue83e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dev_to_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dev-to-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued0e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_mobile(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-mobile. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_mobile_camera(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-mobile-camera. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_mobile_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-mobile-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee46", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_mobile_speaker(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-mobile-speaker. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_rotate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-rotate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedf2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_tablet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-tablet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_tablet_camera(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-tablet-camera. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def device_tablet_speaker(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon device-tablet-speaker. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def devices(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon devices. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueba4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def diamond(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon diamond. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def diamonds_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon diamonds-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_five(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-five. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_one(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-one. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dice_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dice-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def disc(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon disc. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue564", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def disco_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon disco-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued98", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def discord_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon discord-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue61a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def divide(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon divide. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dna(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dna. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue924", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dog(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dog. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue74a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def door(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon door. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue61c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def door_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon door-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecde", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dot_outline(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dot-outline. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uece0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_nine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-nine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue794", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_six_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-six-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueae2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue200", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three_circle_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three-circle-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue202", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three_outline(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three-outline. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue204", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three_outline_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three-outline-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue206", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dots_three_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dots-three-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue208", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def download(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon download. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue20a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def download_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon download-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue20c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dress(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dress. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea7e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dresser(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dresser. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue94e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dribbble_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dribbble-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue20e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued74", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue210", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drop_half(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drop-half. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue566", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drop_half_bottom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drop-half-bottom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb40", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drop_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drop-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee32", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def drop_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon drop-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue954", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def dropbox_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon dropbox-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ear(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ear. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue70c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ear_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ear-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue70e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def egg(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon egg. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue812", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def egg_crack(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon egg-crack. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb64", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eject(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eject. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue212", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eject_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eject-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def elevator(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon elevator. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecc0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def empty(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon empty. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedbc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def engine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon engine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea80", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def envelope(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon envelope. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue214", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def envelope_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon envelope-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue216", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def envelope_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon envelope-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue218", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def envelope_simple_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon envelope-simple-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue21a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def equalizer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon equalizer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebbc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def equals(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon equals. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue21c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eraser(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eraser. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue21e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def escalator_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon escalator-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def escalator_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon escalator-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecbc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def exam(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon exam. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue742", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def exclamation_mark(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon exclamation-mark. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee44", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def exclude(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon exclude. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue882", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def exclude_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon exclude-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue880", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def export(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon export. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaf0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eye(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eye. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue220", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eye_closed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eye-closed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue222", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eye_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eye-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue224", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eyedropper(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eyedropper. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue568", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eyedropper_sample(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eyedropper-sample. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueac4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eyeglasses(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eyeglasses. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def eyes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon eyes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee5c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def face_mask(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon face-mask. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue56a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def facebook_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon facebook-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue226", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def factory(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon factory. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue760", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def faders(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon faders. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue228", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def faders_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon faders-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue22a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fallout_shelter(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fallout-shelter. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fan(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fan. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def farm(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon farm. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec70", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fast_forward(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fast-forward. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fast_forward_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fast-forward-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue22c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def feather(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon feather. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fediverse_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fediverse-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued66", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def figma_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon figma-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue22e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue230", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_archive(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-archive. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb2a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue232", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue61e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_audio(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-audio. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea20", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_c(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-c. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb32", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_c_sharp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-c-sharp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb30", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_cloud(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-cloud. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue95e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_code(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-code. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue914", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_cpp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-cpp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb2e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_css(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-css. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_csv(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-csv. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb1c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue704", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_dotted(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-dotted. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue704", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_doc(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-doc. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb1e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_html(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-html. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb38", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_image(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-image. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea24", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_ini(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-ini. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb33", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_jpg(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-jpg. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb1a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_js(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-js. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb24", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_jsx(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-jsx. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb3a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_lock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-lock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue95c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_magnifying_glass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-magnifying-glass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue238", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_search(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-search. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue238", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_md(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-md. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued50", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue234", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_pdf(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-pdf. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue702", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue236", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_png(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-png. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb18", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_ppt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-ppt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb20", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_py(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-py. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb2c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_rs(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-rs. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb28", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_sql(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-sql. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued4e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_svg(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-svg. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued08", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_text(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-text. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue23a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_ts(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-ts. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb26", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_tsx(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-tsx. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb3c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_txt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-txt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb35", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_video(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-video. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea22", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_vue(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-vue. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb3e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue23c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_xls(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-xls. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb22", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def file_zip(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon file-zip. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue958", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def files(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon files. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue710", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def film_reel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon film-reel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def film_script(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon film-script. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb50", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def film_slate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon film-slate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def film_strip(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon film-strip. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue792", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fingerprint(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fingerprint. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue23e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fingerprint_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fingerprint-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue240", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def finn_the_human(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon finn-the-human. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue56c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fire(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fire. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue242", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fire_extinguisher(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fire-extinguisher. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fire_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fire-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue620", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fire_truck(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fire-truck. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue574", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def first_aid(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon first-aid. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue56e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def first_aid_kit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon first-aid-kit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue570", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fish(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fish. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue728", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fish_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fish-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue72a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue244", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flag_banner(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flag-banner. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue622", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flag_banner_fold(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flag-banner-fold. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecf2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flag_checkered(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flag-checkered. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea38", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flag_pennant(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flag-pennant. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecf0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flame(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flame. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue624", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flashlight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flashlight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue246", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flask(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flask. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue79e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flip_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flip-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued6a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flip_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flip-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued6c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def floppy_disk(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon floppy-disk. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue248", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def floppy_disk_back(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon floppy-disk-back. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaf4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flow_arrow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flow-arrow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue75e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flower_lotus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flower-lotus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flower_tulip(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flower-tulip. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueacc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def flying_saucer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon flying-saucer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb4a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue24a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_notch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-notch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue24a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_dotted(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-dotted. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_lock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-lock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea3c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue254", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_notch_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-notch-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue254", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue256", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_notch_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-notch-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue256", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue258", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_notch_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-notch-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue258", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue25a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec2a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_dotted(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-dotted. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec2a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_lock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-lock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb5e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue25c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue25e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec2e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_simple_user(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-simple-user. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb60", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea86", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folder_user(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folder-user. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb46", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def folders(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon folders. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue260", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def football(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon football. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue718", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def football_helmet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon football-helmet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee4c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def footprints(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon footprints. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea88", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def fork_knife(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon fork-knife. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue262", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def four_k(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon four-k. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea5c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def frame_corners(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon frame-corners. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue626", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def framer_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon framer-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue264", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def function(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon function. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebe4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def funnel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon funnel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue266", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def funnel_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon funnel-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue268", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def funnel_simple_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon funnel-simple-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue26a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def funnel_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon funnel-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue26c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def game_controller(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon game-controller. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue26e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def garage(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon garage. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecd6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gas_can(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gas-can. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gas_pump(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gas-pump. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue768", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gauge(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gauge. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue628", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gavel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gavel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea32", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gear(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gear. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue270", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gear_fine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gear-fine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue87c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gear_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gear-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue272", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_female(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-female. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_intersex(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-intersex. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_male(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-male. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_neuter(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-neuter. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_nonbinary(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-nonbinary. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gender_transgender(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gender-transgender. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ghost(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ghost. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue62a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gif(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gif. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue274", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gift(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gift. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue276", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_branch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-branch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue278", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_commit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-commit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue27a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_diff(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-diff. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue27c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_fork(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-fork. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue27e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_merge(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-merge. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue280", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def git_pull_request(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon git-pull-request. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue282", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def github_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon github-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue576", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gitlab_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gitlab-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue694", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gitlab_logo_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gitlab-logo-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue696", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue288", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_hemisphere_east(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-hemisphere-east. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue28a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_hemisphere_west(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-hemisphere-west. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue28c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue28e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_simple_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-simple-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue284", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_stand(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-stand. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue290", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def globe_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon globe-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue286", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def goggles(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon goggles. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecb4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def golf(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon golf. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea3e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def goodreads_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon goodreads-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued10", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_cardboard_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-cardboard-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_chrome_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-chrome-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue976", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_drive_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-drive-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue292", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_photos_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-photos-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb92", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_play_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-play-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue294", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def google_podcasts_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon google-podcasts-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb94", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gps(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gps. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedd8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gps_fix(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gps-fix. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedd6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gps_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gps-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedd4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def gradient(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon gradient. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb42", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def graduation_cap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon graduation-cap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue62c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def grains(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon grains. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec68", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def grains_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon grains-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec6a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def graph(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon graph. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb58", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def graphics_card(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon graphics-card. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue612", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def greater_than(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon greater-than. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedc4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def greater_than_or_equal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon greater-than-or-equal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueda2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def grid_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon grid-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue296", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def grid_nine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon grid-nine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec8c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def guitar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon guitar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea8a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hair_dryer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hair-dryer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea66", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hamburger(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hamburger. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue790", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hammer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hammer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue80e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue298", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea4e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee5a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_coins(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-coins. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea8c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_deposit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-deposit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee82", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_eye(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-eye. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea4c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_fist(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-fist. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue57a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_grabbing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-grabbing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue57c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_heart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-heart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue810", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_palm(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-palm. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue57e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_peace(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-peace. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_pointing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-pointing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue29a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_soap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-soap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue630", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_swipe_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-swipe-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec94", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_swipe_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-swipe-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec92", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_tap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-tap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec90", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_waving(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-waving. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue580", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hand_withdraw(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hand-withdraw. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee80", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def handbag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon handbag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue29c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def handbag_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon handbag-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue62e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hands_clapping(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hands-clapping. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hands_praying(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hands-praying. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecc8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def handshake(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon handshake. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue582", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hard_drive(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hard-drive. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue29e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hard_drives(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hard-drives. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hard_hat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hard-hat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued46", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hash_straight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hash-straight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def head_circuit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon head-circuit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def headlights(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon headlights. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def headphones(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon headphones. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def headset(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon headset. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue584", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heart_break(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heart-break. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebe8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heart_half(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heart-half. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec48", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heart_straight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heart-straight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heart_straight_break(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heart-straight-break. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb98", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def heartbeat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon heartbeat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hexagon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hexagon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def high_definition(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon high-definition. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea8e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def high_heel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon high-heel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def highlighter(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon highlighter. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec76", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def highlighter_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon highlighter-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue632", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hockey(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hockey. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec86", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hoodie(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hoodie. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecd0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def horse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon horse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hospital(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hospital. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue844", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_simple_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-simple-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_simple_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-simple-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hourglass_simple_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hourglass-simple-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def house(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon house. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def house_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon house-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def house_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon house-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def hurricane(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon hurricane. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue88e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ice_cream(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ice-cream. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue804", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def identification_badge(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon identification-badge. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def identification_card(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon identification-card. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def image(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon image. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def image_broken(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon image-broken. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def image_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon image-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def images(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon images. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue836", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def images_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon images-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue834", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def infinity(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon infinity. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue634", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lemniscate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lemniscate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue634", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def info(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon info. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def instagram_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon instagram-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def intersect(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon intersect. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def intersect_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon intersect-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue87a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def intersect_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon intersect-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecc4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def intersection(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon intersection. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def invoice(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon invoice. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee42", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def island(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon island. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee06", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def jar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon jar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def jar_label(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon jar-label. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7e1", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def jeep(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon jeep. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def joystick(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon joystick. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea5e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def kanban(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon kanban. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb54", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def key(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon key. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def key_return(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon key-return. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue782", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def keyboard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon keyboard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def keyhole(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon keyhole. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea78", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def knife(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon knife. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue636", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ladder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ladder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ladder_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ladder-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec26", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lamp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lamp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue638", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lamp_pendant(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lamp-pendant. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee2e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def laptop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon laptop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue586", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lasso(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lasso. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedc6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lastfm_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lastfm-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue842", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def layout(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon layout. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def leaf(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon leaf. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lectern(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lectern. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue95a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lego(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lego. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lego_smiley(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lego-smiley. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8c7", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def less_than(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon less-than. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def less_than_or_equal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon less-than-or-equal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueda4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def letter_circle_h(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon letter-circle-h. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebf8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def letter_circle_p(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon letter-circle-p. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec08", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def letter_circle_v(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon letter-circle-v. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec14", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lifebuoy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lifebuoy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue63a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lightbulb(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lightbulb. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lightbulb_filament(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lightbulb-filament. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue63c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lighthouse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lighthouse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lightning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lightning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lightning_a(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lightning-a. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea84", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lightning_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lightning-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def line_segment(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon line-segment. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def line_segments(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon line-segments. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def line_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon line-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued70", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link_break(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link-break. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link_simple_break(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link-simple-break. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link_simple_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link-simple-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def link_simple_horizontal_break(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon link-simple-horizontal-break. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def linkedin_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon linkedin-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def linktree_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon linktree-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def linux_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon linux-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb02", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_bullets(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-bullets. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_checks(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-checks. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueadc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_dashes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-dashes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_heart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-heart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebde", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_magnifying_glass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-magnifying-glass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebe0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_numbers(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-numbers. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def list_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon list-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebdc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_key(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-key. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue2fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_key_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-key-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue300", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_laminated(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-laminated. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue302", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_laminated_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-laminated-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue304", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue306", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue308", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lock_simple_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lock-simple-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue30a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def lockers(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon lockers. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecb8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def log(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon log. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued82", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magic_wand(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magic-wand. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magnet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magnet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue680", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magnet_straight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magnet-straight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue682", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magnifying_glass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magnifying-glass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue30c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magnifying_glass_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magnifying-glass-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue30e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def magnifying_glass_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon magnifying-glass-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue310", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mailbox(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mailbox. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec1e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue316", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_area(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-area. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee3a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue318", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue314", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee3e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_simple_area(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-simple-area. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee3c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_pin_simple_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-pin-simple-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee38", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def map_trifold(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon map-trifold. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue31a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def markdown_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon markdown-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue508", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def marker_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon marker-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue640", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def martini(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon martini. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue31c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mask_happy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mask-happy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mask_sad(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mask-sad. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb9e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mastodon_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mastodon-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued68", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def math_operations(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon math-operations. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue31e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def matrix_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon matrix-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued64", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def medal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon medal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue320", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def medal_military(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon medal-military. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecfc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def medium_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon medium-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue322", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def megaphone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon megaphone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue324", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def megaphone_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon megaphone-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue642", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def member_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon member-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedc2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def memory(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon memory. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def messenger_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon messenger-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def meta_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon meta-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued02", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def meteor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon meteor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def metronome(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon metronome. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec8e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microphone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microphone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue326", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microphone_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microphone-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue328", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microphone_stage(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microphone-stage. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue75c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microscope(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microscope. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec7a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microsoft_excel_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microsoft-excel-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb6c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microsoft_outlook_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microsoft-outlook-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb70", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microsoft_powerpoint_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microsoft-powerpoint-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueace", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microsoft_teams_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microsoft-teams-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb66", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def microsoft_word_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon microsoft-word-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb6a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue32a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def minus_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon minus-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue32c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def minus_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon minus-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued4c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def money(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon money. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue588", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def money_wavy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon money-wavy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee68", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def monitor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon monitor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue32e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def monitor_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon monitor-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue58a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def monitor_play(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon monitor-play. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue58c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def moon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon moon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue330", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def moon_stars(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon moon-stars. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue58e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def moped(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon moped. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue824", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def moped_front(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon moped-front. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue822", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mosque(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mosque. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def motorcycle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon motorcycle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue80a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mountains(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mountains. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue33a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse_left_click(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse-left-click. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue334", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse_middle_click(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse-middle-click. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue338", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse_right_click(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse-right-click. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue336", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse_scroll(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse-scroll. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue332", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def mouse_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon mouse-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue644", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_note(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-note. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue33c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_note_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-note-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue33e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_notes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-notes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue340", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_notes_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-notes-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee0c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_notes_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-notes-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb7c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def music_notes_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon music-notes-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue342", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def navigation_arrow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon navigation-arrow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueade", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def needle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon needle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue82e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def network(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon network. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedde", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def network_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon network-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueddc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def network_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon network-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedda", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def newspaper(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon newspaper. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue344", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def newspaper_clipping(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon newspaper-clipping. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue346", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def not_equals(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon not-equals. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueda6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def not_member_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon not-member-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def not_subset_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon not-subset-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedb0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def not_superset_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon not-superset-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedb2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def notches(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon notches. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued3a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def note(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon note. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue348", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def note_blank(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon note-blank. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue34a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def note_pencil(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon note-pencil. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue34c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def notebook(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon notebook. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue34e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def notepad(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon notepad. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue63e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def notification(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon notification. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def notion_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon notion-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def nuclear_plant(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon nuclear-plant. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued7c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_eight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-eight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue352", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_five(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-five. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue358", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue35e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_nine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-nine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue364", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_one(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-one. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue36a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_seven(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-seven. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue370", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue376", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue37c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue382", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_circle_zero(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-circle-zero. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue388", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_eight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-eight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue350", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_five(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-five. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue356", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue35c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_nine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-nine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue362", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_one(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-one. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue368", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_seven(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-seven. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue36e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue374", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_eight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-eight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue354", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_five(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-five. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue35a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue360", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_nine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-nine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue366", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_one(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-one. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue36c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_seven(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-seven. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue372", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue378", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue37e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue384", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_square_zero(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-square-zero. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue38a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue37a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue380", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def number_zero(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon number-zero. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue386", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def numpad(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon numpad. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def nut(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon nut. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue38c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ny_times_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ny-times-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue646", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def octagon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon octagon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue38e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def office_chair(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon office-chair. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea46", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def onigiri(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon onigiri. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee2c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def open_ai_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon open-ai-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def option(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon option. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def orange(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon orange. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee40", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def orange_slice(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon orange-slice. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued36", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def oven(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon oven. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued8c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def package(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon package. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue390", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paint_brush(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paint-brush. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paint_brush_broad(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paint-brush-broad. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue590", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paint_brush_household(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paint-brush-household. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paint_bucket(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paint-bucket. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue392", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paint_roller(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paint-roller. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def palette(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon palette. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def panorama(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon panorama. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaa2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pants(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pants. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec88", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paper_plane(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paper-plane. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue394", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paper_plane_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paper-plane-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue396", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paper_plane_tilt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paper-plane-tilt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue398", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paperclip(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paperclip. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue39a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paperclip_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paperclip-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue592", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def parachute(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon parachute. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea7c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paragraph(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paragraph. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue960", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def parallelogram(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon parallelogram. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecc6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def park(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon park. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecb2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def password(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon password. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue752", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def path(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon path. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue39c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def patreon_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon patreon-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue98a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pause(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pause. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue39e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pause_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pause-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paw_print(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paw-print. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue648", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def paypal_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon paypal-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue98c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def peace(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon peace. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pen(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pen. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pen_nib(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pen-nib. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pen_nib_straight(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pen-nib-straight. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue64a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_ruler(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-ruler. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue906", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_simple_line(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-simple-line. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebc6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_simple_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-simple-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecf6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pencil_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pencil-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecf8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pentagon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pentagon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec7e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pentagram(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pentagram. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec5c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pepper(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pepper. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue94a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def percent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon percent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_arms_spread(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-arms-spread. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecfe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue72e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_bike(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-bike. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue734", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee58", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_hike(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-hike. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued54", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_run(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-run. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue730", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_ski(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-ski. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue71c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_snowboard(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-snowboard. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue71e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_swim(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-swim. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue736", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_tai_chi(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-tai-chi. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued5c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_throw(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-throw. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue732", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def person_simple_walk(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon person-simple-walk. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue73a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def perspective(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon perspective. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebe6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_call(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-call. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_disconnect(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-disconnect. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_incoming(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-incoming. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_list(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-list. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_outgoing(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-outgoing. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_pause(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-pause. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec56", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_transfer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-transfer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phone_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phone-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def phosphor_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon phosphor-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pi(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pi. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec80", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def piano_keys(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon piano-keys. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def picnic_table(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon picnic-table. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee26", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def picture_in_picture(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon picture-in-picture. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue64c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def piggy_bank(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon piggy-bank. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea04", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pill(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pill. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue700", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ping_pong(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ping-pong. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea42", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pint_glass(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pint-glass. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedd0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pinterest_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pinterest-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue64e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pinwheel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pinwheel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb9c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pipe(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pipe. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued86", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pipe_wrench(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pipe-wrench. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued88", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pix_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pix-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecc2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pizza(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pizza. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue796", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def placeholder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon placeholder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue650", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def planet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon planet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue652", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plant(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plant. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def play(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon play. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def play_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon play-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def play_pause(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon play-pause. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def playlist(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon playlist. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plug(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plug. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue946", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plug_charging(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plug-charging. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb5c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plugs(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plugs. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb56", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plugs_connected(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plugs-connected. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb5a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plus_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plus-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plus_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plus-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def plus_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon plus-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued4a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def poker_chip(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon poker-chip. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue594", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def police_car(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon police-car. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec4a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def polygon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon polygon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def popcorn(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon popcorn. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb4e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def popsicle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon popsicle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebbe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def potted_plant(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon potted-plant. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec22", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def power(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon power. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def prescription(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon prescription. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def presentation(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon presentation. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue654", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def presentation_chart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon presentation-chart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue656", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def printer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon printer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def prohibit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon prohibit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def prohibit_inset(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon prohibit-inset. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def projector_screen(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon projector-screen. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue658", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def projector_screen_chart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon projector-screen-chart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue65a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def pulse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon pulse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue000", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def activity(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon activity. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue000", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def push_pin(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon push-pin. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def push_pin_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon push-pin-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue65c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def push_pin_simple_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon push-pin-simple-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue65e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def push_pin_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon push-pin-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def puzzle_piece(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon puzzle-piece. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue596", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def qr_code(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon qr-code. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def question(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon question. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def question_mark(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon question-mark. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3e9", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def queue(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon queue. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def quotes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon quotes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue660", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rabbit(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rabbit. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueac2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def racquet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon racquet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee02", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def radical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon radical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def radio(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon radio. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue77e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def radio_button(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon radio-button. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb08", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def radioactive(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon radioactive. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rainbow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rainbow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue598", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rainbow_cloud(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rainbow-cloud. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue59a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ranking(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ranking. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued62", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def read_cv_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon read-cv-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued0c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def receipt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon receipt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def receipt_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon receipt-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued40", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def record(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon record. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rectangle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rectangle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rectangle_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rectangle-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def recycle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon recycle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue75a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def reddit_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon reddit-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue59c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def repeat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon repeat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def repeat_once(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon repeat-once. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def replit_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon replit-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb8a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def resize(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon resize. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued6e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rewind(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rewind. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rewind_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rewind-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def road_horizon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon road-horizon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue838", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def robot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon robot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue762", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rocket(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rocket. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rocket_launch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rocket-launch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3fe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rows(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rows. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rows_plus_bottom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rows-plus-bottom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue59e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rows_plus_top(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rows-plus-top. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rss(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rss. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue400", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rss_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rss-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue402", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def rug(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon rug. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea1a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ruler(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ruler. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sailboat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sailboat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue78a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scales(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scales. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue750", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scan(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scan. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebb6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scan_smiley(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scan-smiley. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebb4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scissors(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scissors. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueae0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scooter(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scooter. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue820", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def screencast(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon screencast. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue404", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def screwdriver(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon screwdriver. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue86e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scribble(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scribble. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue806", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scribble_loop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scribble-loop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue662", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def scroll(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon scroll. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb7a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue604", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_wavy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-wavy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue604", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seal_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seal-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue606", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_wavy_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-wavy-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue606", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seal_percent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seal-percent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue60a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seal_question(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seal-question. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue608", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_wavy_question(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-wavy-question. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue608", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seal_warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seal-warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue60c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def circle_wavy_warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon circle-wavy-warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue60c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb8e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def seatbelt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon seatbelt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedfe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def security_camera(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon security-camera. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueca4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue69a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_all(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-all. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue746", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_background(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-background. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaf8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_foreground(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-foreground. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaf6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_inverse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-inverse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue744", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue69c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def selection_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon selection-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue69e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shapes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shapes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec5e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def share(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon share. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue406", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def share_fat(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon share-fat. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued52", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def share_network(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon share-network. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue408", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue40a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue40c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_checkered(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-checkered. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue708", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_chevron(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-chevron. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue40e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue706", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue410", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shield_warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shield-warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue412", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shipping_container(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shipping-container. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue78c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shirt_folded(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shirt-folded. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea92", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shooting_star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shooting-star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecfa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shopping_bag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shopping-bag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue416", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shopping_bag_open(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shopping-bag-open. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue418", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shopping_cart(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shopping-cart. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue41e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shopping_cart_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shopping-cart-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue420", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shovel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shovel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shower(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shower. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue776", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shrimp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shrimp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueab4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shuffle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shuffle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue422", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shuffle_angular(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shuffle-angular. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue424", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def shuffle_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon shuffle-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue426", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sidebar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sidebar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueab6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sidebar_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sidebar-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec24", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sigma(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sigma. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueab8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sign_in(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sign-in. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue428", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sign_out(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sign-out. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue42a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def signature(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon signature. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def signpost(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon signpost. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue89c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sim_card(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sim-card. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue664", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def siren(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon siren. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sketch_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sketch-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue42c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skip_back(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skip-back. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skip_back_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skip-back-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue42e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skip_forward(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skip-forward. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skip_forward_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skip-forward-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue430", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skull(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skull. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue916", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def skype_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon skype-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def slack_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon slack-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sliders(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sliders. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue432", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sliders_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sliders-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue434", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def slideshow(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon slideshow. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued32", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue436", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_angry(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-angry. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec62", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_blank(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-blank. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue438", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_meh(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-meh. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue43a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_melting(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-melting. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee56", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_nervous(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-nervous. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue43c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_sad(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-sad. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue43e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_sticker(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-sticker. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue440", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_wink(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-wink. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue666", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def smiley_x_eyes(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon smiley-x-eyes. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue442", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def snapchat_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon snapchat-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue668", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sneaker(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sneaker. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue80c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sneaker_move(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sneaker-move. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued60", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def snowflake(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon snowflake. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def soccer_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon soccer-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue716", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sock(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sock. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def solar_panel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon solar-panel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued7a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def solar_roof(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon solar-roof. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued7b", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sort_ascending(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sort-ascending. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue444", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sort_descending(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sort-descending. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue446", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def soundcloud_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon soundcloud-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spade(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spade. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue448", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sparkle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sparkle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_hifi(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-hifi. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea08", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue44a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue44c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_none(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-none. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue44e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_simple_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-simple-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue450", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_simple_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-simple-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue452", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_simple_none(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-simple-none. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue454", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_simple_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-simple-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue456", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_simple_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-simple-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue458", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue45a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speaker_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speaker-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue45c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def speedometer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon speedometer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee74", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sphere(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sphere. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee66", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spinner(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spinner. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue66a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spinner_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spinner-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee28", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spinner_gap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spinner-gap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue66c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spiral(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spiral. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def split_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon split-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue872", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def split_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon split-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue876", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spotify_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spotify-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue66e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def spray_bottle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon spray-bottle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue45e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square_half(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square-half. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue462", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square_half_bottom(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square-half-bottom. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb16", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue690", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square_split_horizontal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square-split-horizontal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue870", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def square_split_vertical(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon square-split-vertical. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue874", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def squares_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon squares-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue464", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stack(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stack. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue466", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stack_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stack-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedf4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stack_overflow_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stack-overflow-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb78", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stack_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stack-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedf6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stack_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stack-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue468", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stairs(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stairs. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stamp(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stamp. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea48", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def standard_definition(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon standard-definition. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea90", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def star(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon star. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue46a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def star_and_crescent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon star-and-crescent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecf4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def star_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon star-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6a4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def star_half(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon star-half. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue70a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def star_of_david(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon star-of-david. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue89e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def steam_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon steam-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uead4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def steering_wheel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon steering-wheel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def steps(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon steps. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecbe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stethoscope(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stethoscope. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sticker(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sticker. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stool(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stool. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea44", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stop(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stop. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue46c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stop_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stop-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue46e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def storefront(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon storefront. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue470", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def strategy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon strategy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea3a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def stripe_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon stripe-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue698", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def student(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon student. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue73e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subset_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subset-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedc0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subset_proper_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subset-proper-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedb6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subtitles(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subtitles. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subtitles_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subtitles-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue1a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subtract(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subtract. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebd6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subtract_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subtract-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uebd4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def subway(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon subway. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue498", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def suitcase(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon suitcase. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def suitcase_rolling(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon suitcase-rolling. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def suitcase_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon suitcase-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sun(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sun. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue472", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sun_dim(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sun-dim. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue474", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sun_horizon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sun-horizon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sunglasses(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sunglasses. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue816", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def superset_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon superset-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedb8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def superset_proper_of(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon superset-proper-of. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedb4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def swap(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon swap. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue83c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def swatches(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon swatches. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def swimming_pool(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon swimming-pool. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecb6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def sword(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon sword. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def synagogue(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon synagogue. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def syringe(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon syringe. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue968", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def t_shirt(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon t-shirt. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue670", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def table(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon table. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue476", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tabs(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tabs. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue778", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue478", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tag_chevron(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tag-chevron. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue672", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tag_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tag-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue47a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def target(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon target. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue47c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def taxi(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon taxi. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue902", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tea_bag(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tea-bag. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def telegram_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon telegram-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def television(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon television. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue754", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def television_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon television-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueae6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tennis_ball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tennis-ball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue720", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def terminal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon terminal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue47e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def terminal_window(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon terminal-window. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueae8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def test_tube(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon test-tube. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_a_underline(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-a-underline. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued34", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_aa(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-aa. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_align_center(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-align-center. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue480", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_align_justify(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-align-justify. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue482", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_align_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-align-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue484", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_align_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-align-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue486", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_b(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-b. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_bolder(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-bolder. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_columns(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-columns. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec96", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_five(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-five. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_one(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-one. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_six(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-six. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_h_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-h-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_indent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-indent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea1e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_italic(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-italic. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_outdent(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-outdent. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea1c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_strikethrough(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-strikethrough. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_subscript(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-subscript. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec98", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_superscript(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-superscript. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec9a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_t(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-t. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue48a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_t_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-t-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue488", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def text_underline(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon text-underline. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def textbox(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon textbox. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueb0a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thermometer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thermometer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thermometer_cold(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thermometer-cold. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thermometer_hot(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thermometer-hot. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thermometer_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thermometer-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def threads_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon threads-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued9e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def three_d(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon three-d. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea5a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thumbs_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thumbs-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue48c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def thumbs_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon thumbs-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue48e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def ticket(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon ticket. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue490", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tidal_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tidal-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued1c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tiktok_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tiktok-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaf2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tilde(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tilde. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueda8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def timer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon timer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue492", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tip_jar(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tip-jar. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tipi(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tipi. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued30", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tire(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tire. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedd2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def toggle_left(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon toggle-left. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue674", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def toggle_right(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon toggle-right. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue676", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def toilet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon toilet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue79a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def toilet_paper(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon toilet-paper. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue79c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def toolbox(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon toolbox. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueca0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tooth(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tooth. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tornado(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tornado. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue88c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tote(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tote. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue494", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tote_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tote-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue678", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def towel(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon towel. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uede6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tractor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tractor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec6e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trademark(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trademark. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trademark_registered(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trademark-registered. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue3f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def traffic_cone(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon traffic-cone. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def traffic_sign(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon traffic-sign. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue67a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def traffic_signal(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon traffic-signal. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def train(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon train. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue496", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def train_regional(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon train-regional. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue49e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def train_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon train-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4a0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tram(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tram. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def translate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon translate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4a2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4a6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trash_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trash-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4a8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tray(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tray. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4aa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tray_arrow_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tray-arrow-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue010", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def archive_tray(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon archive-tray. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue010", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tray_arrow_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tray-arrow-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee52", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def treasure_chest(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon treasure-chest. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uede2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tree(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tree. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tree_evergreen(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tree-evergreen. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tree_palm(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tree-palm. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue91a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tree_structure(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tree-structure. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue67c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tree_view(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tree-view. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee48", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trend_down(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trend-down. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trend_up(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trend-up. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def triangle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon triangle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4b0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def triangle_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon triangle-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trolley(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trolley. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trolley_suitcase(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trolley-suitcase. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def trophy(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon trophy. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue67e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def truck(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon truck. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4b4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def truck_trailer(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon truck-trailer. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4b6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def tumblr_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon tumblr-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def twitch_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon twitch-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def twitter_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon twitter-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ba", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def umbrella(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon umbrella. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue684", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def umbrella_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon umbrella-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue686", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def union(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon union. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedbe", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def unite(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon unite. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue87e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def unite_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon unite-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue878", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def upload(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon upload. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4be", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def upload_simple(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon upload-simple. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4c0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def usb(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon usb. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue956", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4c2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueafa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4c4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle_check(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle-check. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec38", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle_dashed(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle-dashed. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uec36", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle_gear(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle-gear. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4c6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4c8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_circle_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-circle-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ca", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_focus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-focus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_gear(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-gear. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4cc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_list(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-list. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue73c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_minus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-minus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_plus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-plus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_rectangle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-rectangle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_sound(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-sound. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueca8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def user_switch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon user-switch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue756", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def users(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon users. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def users_four(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon users-four. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue68c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def users_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon users-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue68e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def van(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon van. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue826", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vault(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vault. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue76e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vector_three(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vector-three. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee62", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vector_two(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vector-two. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee64", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vibrate(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vibrate. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4d8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def video(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon video. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue740", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def video_camera(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon video-camera. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4da", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def video_camera_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon video-camera-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4dc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def video_conference(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon video-conference. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uedce", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vignette(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vignette. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueba2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def vinyl_record(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon vinyl-record. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecac", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def virtual_reality(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon virtual-reality. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7b8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def virus(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon virus. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7d6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def visor(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon visor. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uee2a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def voicemail(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon voicemail. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def volleyball(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon volleyball. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue726", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wall(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wall. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue688", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wallet(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wallet. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue68a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def warehouse(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon warehouse. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecd4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def warning(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon warning. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4e0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def warning_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon warning-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4e2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def warning_diamond(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon warning-diamond. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue7fc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def warning_octagon(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon warning-octagon. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4e4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def washing_machine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon washing-machine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uede8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def watch(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon watch. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4e6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wave_sawtooth(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wave-sawtooth. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea9c", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wave_sine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wave-sine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea9a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wave_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wave-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uea9e", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wave_triangle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wave-triangle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ueaa0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def waveform(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon waveform. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue802", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def waveform_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon waveform-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue800", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def waves(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon waves. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6de", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def webcam(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon webcam. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def webcam_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon webcam-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecdc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def webhooks_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon webhooks-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\uecae", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wechat_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wechat-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue8d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def whatsapp_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon whatsapp-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5d0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wheelchair(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wheelchair. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4e8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wheelchair_motion(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wheelchair-motion. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue89a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_high(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-high. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ea", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_low(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-low. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ec", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_medium(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-medium. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4ee", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_none(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-none. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4f0", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_slash(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-slash. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4f2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wifi_x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wifi-x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4f4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wind(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wind. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5d2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def windmill(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon windmill. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue9f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def windows_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon windows-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue692", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wine(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wine. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue6b2", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def wrench(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon wrench. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue5d4", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def x(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon x. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4f6", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def x_circle(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon x-circle. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4f8", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def x_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon x-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4bc", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def x_square(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon x-square. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4fa", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def yarn(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon yarn. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ued9a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def yin_yang(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon yin-yang. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue92a", angle=angle, style=style)


@drawlib.v0_1.private.util.error_handler
def youtube_logo(
    xy: typing.Tuple[float, float],
    width: float,
    angle: typing.Union[int, float] = 0.0,
    style: typing.Union[drawlib.v0_1.private.core.model.IconStyle, str, None] = None,
) -> None:
    """Draw phosphor icon youtube-logo. This is auto generated code.

    Args:
        xy: default align is center, center.
        width: horizontal icon size.
        angle: rotation. 0.0 ~ 360.0
        style: icon style

    Returns:
        None

    """

    _write(xy=xy, width=width, code="\ue4fc", angle=angle, style=style)
