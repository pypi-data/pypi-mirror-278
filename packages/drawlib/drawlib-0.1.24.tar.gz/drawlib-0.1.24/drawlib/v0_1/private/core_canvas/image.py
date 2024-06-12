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

from typing import Optional, Union, Any, Tuple
from PIL.Image import Image
import numpy
from matplotlib import offsetbox
from drawlib.v0_1.private.core.model import ImageStyle, ShapeStyle
from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.core.util import ImageUtil
from drawlib.v0_1.private.core_canvas.patches import CanvasPatchesFeature
from drawlib.v0_1.private.logging import logger
from drawlib.v0_1.private.validators.args import validate_args


class CanvasImageFeature(CanvasPatchesFeature):
    def __init__(self) -> None:
        super().__init__()

    @error_handler
    def image(
        self,
        xy: Tuple[float, float],
        width: float,
        image: Union[str, Image, Dimage],
        angle: Union[int, float] = 0.0,
        style: Union[ImageStyle, str, None] = None,
    ) -> None:
        """Draw image

        Args:
            xy: Left bottom of image
            width: Width of image. Height is calculated automatically.
            image: Image path or image itself.
            angle: Rotation degree.
            style: Image style.

        Returns:
            None

        """

        validate_args(locals())
        style = ImageUtil.format_style(style)

        # standadize

        x, y = xy
        dimg = Dimage(image, copy=True)

        # apply effects
        if style.fcolor is not None:
            dimg = dimg.fill(style.fcolor)
        # alpha will be applied to OffsetImage later.

        image_width, image_height = dimg.get_image_size()
        height = image_height / image_width * width
        zoom = self.get_image_zoom_from_width(dimg, width)

        # rotate image
        if angle != 0:
            has_wrong_style = False
            if style.halign != "center":
                has_wrong_style = True
                style.halign = "center"
            if style.valign != "center":
                has_wrong_style = True
                style.valign = "center"
            if has_wrong_style:
                logger.warn("image() with angle only accepts ShapeTextStyle alignment center.")
            dimg = dimg._rotate(angle)

        # xy shift
        if style.halign != "center" or style.valign != "center":
            #
            # memo. calculation
            # (image_width / 2) * (zoom / 0.72) * (canvas_width / 100)
            #   -> image_width * zoom * self._width / 1440

            image_width, image_height = dimg.get_image_size()
            x_shift = image_width * zoom * self._width / 1440
            y_shift = image_height * zoom * self._width / 1440

            if style.halign == "left":
                x += x_shift
            elif style.halign == "center":
                ...
            elif style.halign == "right":
                x -= x_shift
            else:
                raise ValueError(f'halign "{style.halign}" is not supported.')

            if style.valign == "bottom":
                y += y_shift
            elif style.valign == "center":
                ...
            elif style.valign == "top":
                y -= y_shift
            else:
                raise ValueError(f'valign "{style.valign}" is not supported.')

        # create image drawing object
        pil_image = dimg.get_pil_image()
        im = numpy.array(pil_image)

        # grayscale doesn't work fine on matplotlib. convert to RGBA.
        if im.ndim == 3:
            if im.shape[2] == 2:
                gray = im[:, :, 0]
                alpha = im[:, :, 1]
                rgb_array = numpy.stack((gray, gray, gray), axis=-1)
                im = numpy.concatenate((rgb_array, alpha[:, :, numpy.newaxis]), axis=-1)

        imagebox = offsetbox.OffsetImage(im, zoom=zoom, alpha=style.alpha)
        ab = offsetbox.AnnotationBbox(imagebox, (x, y), frameon=False, alpha=0.3)

        # draw later
        self._artists.append(ab)

        # border
        if style.lwidth is None:
            return
        if style.lwidth == 0:
            return

        shapestyle = ShapeStyle(
            halign=style.halign,
            valign=style.valign,
            lstyle=style.lstyle,
            lwidth=style.lwidth,
            lcolor=style.lcolor,
            fcolor=Colors.Transparent,
            alpha=style.alpha,
        )
        self.rectangle(xy=xy, width=width, height=height, angle=angle, style=shapestyle)
