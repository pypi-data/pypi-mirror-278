# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for importing functions and classes at API v0.1.

drawlib posses lots of functions and classes on various modules.
This module provides single interface for importing public API v1.0 objects.

``from drawlib.v0_1.apis import *``

If you requires latest API, import root module instead.

``from drawlib.apis import *``

"""

# pylint: disable=unused-import

#############
### Class ###
#############

from drawlib.v0_1.private.core.colors import (
    Colors,
    Colors140,
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
    # ColorsThemeFlatUI,
    ColorsBase,
)

from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

from drawlib.v0_1.private.core.fonts import (
    FontFile,
    # fonts
    Font,
    FontArabic,
    FontBrahmic,
    FontChinese,
    FontJapanese,
    FontKorean,
    FontMonoSpace,
    FontRoboto,
    FontSansSerif,
    FontSerif,
    FontSourceCode,
    FontThai,
)

from drawlib.v0_1.private.core.dimage import (
    Dimage,
)

######################
### Canvas Methods ###
######################

from drawlib.v0_1.private.core_canvas.canvas import (
    # base
    clear,
    config,
    shape,
    # image
    image,
    # line
    line,
    line_curved,
    line_bezier1,
    line_bezier2,
    lines,
    lines_bezier,
    # shape patches
    arc,
    circle,
    ellipse,
    polygon,
    rectangle,
    regularpolygon,
    wedge,
    donuts,
    fan,
    # shape original
    arrow,
    rhombus,
    parallelogram,
    trapezoid,
    triangle,
    star,
    chevron,
    # text
    text,
    text_vertical,
    # canvas
    save,
)


from drawlib.v0_1.private.icons.util import (
    icon,
)

from drawlib.v0_1.private.icons import (
    phosphor as icon_phosphor,
)

######################
### Other Drawings ###
######################

from drawlib.v0_1.private.core.theme import (
    dtheme,
)
from drawlib.v0_1.private.smartarts import (
    dsart,
)

#################
### Utilities ###
#################

from drawlib.v0_1.private.dutil import (
    dutil_script,
    dutil_canvas,
)
from drawlib.v0_1.private.dutil.settings import (
    dutil_settings,
)
