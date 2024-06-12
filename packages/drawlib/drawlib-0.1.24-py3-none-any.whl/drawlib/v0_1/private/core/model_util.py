from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)


class IconUtil:
    @staticmethod
    def merge_style(primary: IconStyle, secondary: IconStyle):
        primary = primary.copy()

        if primary.style is None:
            primary.style = secondary.style
        if primary.color is None:
            primary.color = secondary.color
        if primary.alpha is None:
            primary.alpha = secondary.alpha
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign

        return primary


class ImageUtil:
    @staticmethod
    def merge_style(primary: ImageStyle, secondary: ImageStyle):
        primary = primary.copy()

        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.lcolor is None:
            primary.lcolor = secondary.lcolor
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.fcolor is None:
            primary.fcolor = secondary.fcolor
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        return primary


class LineUtil:
    @staticmethod
    def merge_line_style(primary: LineStyle, secondary: LineStyle):
        primary = primary.copy()

        if primary.width is None:
            primary.width = secondary.width
        if primary.color is None:
            primary.color = secondary.color
        if primary.style is None:
            primary.style = secondary.style
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        return primary

    @staticmethod
    def merge_linearrow_style(primary: LineArrowStyle, secondary: LineArrowStyle):
        primary = primary.copy()

        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.hstyle is None:
            primary.hstyle = secondary.hstyle
        if primary.hscale is None:
            primary.hscale = secondary.hscale
        if primary.color is None:
            primary.color = secondary.color
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        return primary


class ShapeUtil:
    @staticmethod
    def merge_shape_style(primary: ShapeStyle, secondary: ShapeStyle):
        primary = primary.copy()

        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.lwidth is None:
            primary.lwidth = secondary.lwidth
        if primary.lcolor is None:
            primary.lcolor = secondary.lcolor
        if primary.lstyle is None:
            primary.lstyle = secondary.lstyle
        if primary.fcolor is None:
            primary.fcolor = secondary.fcolor
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        return primary

    @staticmethod
    def merge_shapetext_style(primary: ShapeTextStyle, secondary: ShapeTextStyle):
        primary = primary.copy()

        if primary.color is None:
            primary.color = secondary.color
        if primary.size is None:
            primary.size = secondary.size
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.font is None:
            primary.font = secondary.font
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        return primary


class TextUtil:
    @staticmethod
    def merge_style(
        primary: TextStyle,
        secondary: TextStyle,
        apply_system_default: bool = False,
    ):
        primary = primary.copy()

        if primary.color is None:
            primary.color = secondary.color
        if primary.size is None:
            primary.size = secondary.size
        if primary.halign is None:
            primary.halign = secondary.halign
        if primary.valign is None:
            primary.valign = secondary.valign
        if primary.font is None:
            primary.font = secondary.font
        if primary.alpha is None:
            primary.alpha = secondary.alpha

        merge_background = False
        if not apply_system_default:
            merge_background = True
        elif (
            primary.bglcolor is not None
            or primary.bglstyle is not None
            or primary.bglwidth is not None
            or primary.bgfcolor is not None
        ):
            merge_background = True

        if merge_background:
            if primary.bgalpha is None:
                primary.bgalpha = secondary.bgalpha
            if primary.bglcolor is None:
                primary.bglcolor = secondary.bglcolor
            if primary.bglstyle is None:
                primary.bglstyle = secondary.bglstyle
            if primary.bglwidth is None:
                primary.bglwidth = secondary.bglwidth
            if primary.bgfcolor is None:
                primary.bgfcolor = secondary.bgfcolor

        return primary
