from __future__ import annotations
import dataclasses
from typing import Optional, Dict, Tuple, Union, Literal, List
from copy import deepcopy

from drawlib.v0_1.private.core.colors import (
    ColorsThemeDefault,
    ColorsThemeEssentials,
    ColorsThemeMonochrome,
)
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ThemeStyles,
    OfficialThemeStyle,
)
from drawlib.v0_1.private.core.fonts import (
    FontBase,
    Font,
    FontSourceCode,
)
from drawlib.v0_1.private.core.colors import Colors

#######################
### Official Themes ###
#######################


def get_default() -> OfficialThemeStyle:
    """Change theme to default.

    Returns:
        None

    """

    # blue, green, pink
    # https://coolors.co/6d7cc5-70c2bf-e4dfda-d4b483-c1666b

    # black
    # https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd

    """
    blue = _get_rgba_from_hex("#6D7CC5")
    green = _get_rgba_from_hex("#70C2BF")
    red = _get_rgba_from_hex("#C1666B")
    black = _get_rgba_from_hex("#1B263B")  # fill
    white = Colors.White
    """

    blue = ColorsThemeDefault.Blue
    green = ColorsThemeDefault.Green
    red = ColorsThemeDefault.Red
    black = ColorsThemeDefault.Black
    white = ColorsThemeDefault.White

    default_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template, is_default=True)
    blue_style = _get_fill_style(default_template, blue)
    green_style = _get_fill_style(default_template, green)
    red_style = _get_fill_style(default_template, red)
    black_style = _get_fill_style(default_template, black, white)
    white_style = _get_fill_style(default_template, white)

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=[
            ("red", red_style),
            ("green", green_style),
            ("blue", blue_style),
            ("black", black_style),
            ("white", white_style),
        ],
        theme_colors=[
            ("red", red),
            ("green", green),
            ("blue", blue),
            ("black", black),
            ("white", white),
        ],
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_default2() -> OfficialThemeStyle:
    """Change theme to default.

    Returns:
        None

    """

    blue = ColorsThemeDefault.Blue
    green = ColorsThemeDefault.Green
    red = ColorsThemeDefault.Red
    black = ColorsThemeDefault.Black
    white = ColorsThemeDefault.White

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_thin_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=black,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=black,
        shape_fill_color=blue,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("red", red),
        ("green", green),
        ("blue", blue),
        ("black", black),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_thin_template,
        default_bold_template,
        colors,
        black,
        blue,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_essentials() -> OfficialThemeStyle:
    """Change theme to default.

    Returns:
        None

    """

    red = ColorsThemeEssentials.Red
    lightred = ColorsThemeEssentials.LightRed
    green = ColorsThemeEssentials.Green
    lightgreen = ColorsThemeEssentials.LightGreen
    blue = ColorsThemeEssentials.Blue
    lightblue = ColorsThemeEssentials.LightBlue
    yellow = ColorsThemeEssentials.Yellow
    purple = ColorsThemeEssentials.Purple
    orange = ColorsThemeEssentials.Orange
    navy = ColorsThemeEssentials.Navy
    pink = ColorsThemeEssentials.Pink
    charcoal = ColorsThemeEssentials.Charcoal
    graphite = ColorsThemeEssentials.Graphite
    gray = ColorsThemeEssentials.Gray
    silver = ColorsThemeEssentials.Silver
    snow = ColorsThemeEssentials.Snow
    teal = ColorsThemeEssentials.Teal
    olive = ColorsThemeEssentials.Olive
    brown = ColorsThemeEssentials.Brown
    black = ColorsThemeEssentials.Black
    white = ColorsThemeEssentials.White
    aqua = ColorsThemeEssentials.Aqua
    greenyellow = ColorsThemeEssentials.GreenYellow
    ivory = ColorsThemeEssentials.Ivory
    steel = ColorsThemeEssentials.Steel

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=charcoal,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=charcoal,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=charcoal,
    )

    default_thin_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=charcoal,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=charcoal,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=charcoal,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=charcoal,
        arrowhead_style="->",
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=charcoal,
        shape_fill_color=lightblue,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=charcoal,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("red", red),
        ("lightred", lightred),
        ("pink", pink),
        ("brown", brown),
        ("orange", orange),
        ("green", green),
        ("lightgreen", lightgreen),
        ("greenyellow", greenyellow),
        ("teal", teal),
        ("olive", olive),
        ("blue", blue),
        ("lightblue", lightblue),
        ("aqua", aqua),
        ("navy", navy),
        ("steel", steel),
        ("yellow", yellow),
        ("purple", purple),
        ("ivory", ivory),
        ("black", black),
        ("charcoal", charcoal),
        ("graphite", graphite),
        ("gray", gray),
        ("silver", silver),
        ("snow", snow),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_thin_template,
        default_bold_template,
        colors,
        charcoal,
        lightblue,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_monochrome() -> OfficialThemeStyle:
    black = (0, 0, 0)
    gray1 = (64, 64, 64)
    gray2 = (128, 128, 128)
    gray3 = (192, 192, 192)
    white = (255, 255, 255)

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=black,
    )

    default_thin_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=black,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=black,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=black,
        arrowhead_style="->",
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=black,
        shape_fill_color=white,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=black,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=black,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("black", black),
        ("gray1", gray1),
        ("gray2", gray2),
        ("gray3", gray3),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_thin_template,
        default_bold_template,
        colors,
        black,
        black,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


def get_flatui() -> OfficialThemeStyle:
    # https://flatuicolors.com/palette/defo
    turquoise = (26, 188, 156)
    green_sea = (22, 160, 133)
    emerald = (46, 204, 113)
    nephritis = (39, 174, 96)
    peter_river = (52, 152, 219)
    belize_hole = (41, 128, 185)
    amethyst = (155, 89, 182)
    wisteria = (142, 68, 173)
    wet_asphalt = (52, 73, 94)
    midnight_blue = (44, 62, 80)
    sun_flower = (241, 196, 15)
    orange = (243, 156, 18)
    carrot = (230, 126, 34)
    pumpkin = (211, 84, 0)
    alizarin = (231, 76, 60)
    pomegranate = (192, 57, 43)
    clouds = (236, 240, 241)
    silver = (189, 195, 199)
    concrete = (149, 165, 166)
    asbestos = (127, 140, 141)
    black = (0, 0, 0)
    white = (255, 255, 255)

    default_template = OfficialThemeTemplate(
        icon_style="light",
        icon_color=midnight_blue,
        image_line_width=0,
        line_style="solid",
        line_width=2,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=1.5,
        shape_line_color=midnight_blue,
        shape_fill_color=peter_river,
        shapetext_font=Font.SANSSERIF_REGULAR,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_REGULAR,
        text_size=16,
        text_color=midnight_blue,
    )

    default_thin_template = OfficialThemeTemplate(
        icon_style="thin",
        icon_color=midnight_blue,
        image_line_width=0,
        line_style="solid",
        line_width=1,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=20,
        shape_line_style="solid",
        shape_line_width=0.75,
        shape_line_color=midnight_blue,
        shape_fill_color=peter_river,
        shapetext_font=Font.SANSSERIF_LIGHT,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_LIGHT,
        text_size=16,
        text_color=midnight_blue,
    )

    default_bold_template = OfficialThemeTemplate(
        icon_style="regular",
        icon_color=midnight_blue,
        image_line_width=0,
        line_style="solid",
        line_width=3,
        line_color=midnight_blue,
        arrowhead_style="->",
        arrowhead_scale=30,
        shape_line_style="solid",
        shape_line_width=2.25,
        shape_line_color=midnight_blue,
        shape_fill_color=peter_river,
        shapetext_font=Font.SANSSERIF_BOLD,
        shapetext_size=16,
        shapetext_color=white,
        text_font=Font.SANSSERIF_BOLD,
        text_size=16,
        text_color=midnight_blue,
    )

    default_style = _generate_styles(default_template, is_default=True)
    colors = [
        ("turquoise", turquoise),
        ("green_sea", green_sea),
        ("emerald", emerald),
        ("nephritis", nephritis),
        ("peter_river", peter_river),
        ("belize_hole", belize_hole),
        ("amethyst", amethyst),
        ("wisteria", wisteria),
        ("wet_asphalt", wet_asphalt),
        ("midnight_blue", midnight_blue),
        ("sun_flower", sun_flower),
        ("orange", orange),
        ("carrot", carrot),
        ("pumpkin", pumpkin),
        ("alizarin", alizarin),
        ("pomegranate", pomegranate),
        ("clouds", clouds),
        ("silver", silver),
        ("concrete", concrete),
        ("asbestos", asbestos),
        ("black", black),
        ("white", white),
    ]
    named_styles = get_named_styles(
        default_template,
        default_thin_template,
        default_bold_template,
        colors,
        midnight_blue,
        peter_river,
    )

    return OfficialThemeStyle(
        default_style=default_style,
        named_styles=named_styles,
        theme_colors=colors,
        backgroundcolor=(255, 255, 255, 1.0),
        sourcecodefont=FontSourceCode.SOURCECODEPRO,
    )


############
### Data ###
############


@dataclasses.dataclass
class OfficialThemeTemplate:
    """Helper dataclass for defining theme styles"""

    def copy(self) -> OfficialThemeTemplate:
        return deepcopy(self)

    # icon
    icon_style: Literal["thin", "light", "regular", "bold", "fill"]
    icon_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    image_line_width: float

    # line
    line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    line_width: float
    line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    arrowhead_style: Literal[
        "->",
        "<-",
        "<->",
        "-|>",
        "<|-",
        "<|-|>",
    ]
    arrowhead_scale: int

    # shape
    shape_line_style: Literal["solid", "dashed", "dotted", "dashdot"]
    shape_line_width: float
    shape_line_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]
    shape_fill_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # shapetext
    shapetext_font: FontBase
    shapetext_size: int
    shapetext_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]

    # text
    text_font: FontBase
    text_size: int
    text_color: Union[
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]


############
### Util ###
############


def _get_rgba_from_hex(hex_color: str) -> Tuple[int, int, int, float]:
    """
    Convert a hexadecimal color code to RGBA values.

    Args:
        hex_color (str): The hexadecimal color code (e.g., "#FF5733" or "#FFF").

    Returns:
        tuple[int, int, int, float]: A tuple containing the RGBA values (0-255 for R, G, B and 0.0-1.0 for A).
    """

    # Remove the '#' prefix if present
    hex_color = hex_color.lstrip("#")

    # Determine the length of the hex color code
    hex_length = len(hex_color)

    # Convert the hex code to RGB values
    if hex_length == 3:  # Short hex format (#RGB)
        r = int(hex_color[0] * 2, 16)
        g = int(hex_color[1] * 2, 16)
        b = int(hex_color[2] * 2, 16)
        a = 1.0
    elif hex_length in (6, 8):  # Full hex format (#RRGGBB)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        if hex_length == 8:  # With alpha
            a = int(hex_color[6:8], 16)
        else:
            a = 1.0
    else:
        raise ValueError("Invalid hex color code format")

    return (r, g, b, a)


def get_named_styles(
    default_template: OfficialThemeTemplate,
    thin_template: OfficialThemeTemplate,
    bold_template: OfficialThemeTemplate,
    colors: Tuple[str, Union[Tuple[int, int, int], Tuple[int, int, int, float]]],
    default_shapeline_color: Tuple[int, int, int],
    default_shapefill_color: Tuple[int, int, int],
) -> List[Tuple[str, ThemeStyles]]:

    named_styles = [
        ("thin", _generate_styles(thin_template, is_default=True)),
        ("bold", _generate_styles(bold_template, is_default=True)),
        ("flat", _get_flat_style(default_template, default_shapefill_color)),
        ("solid", _get_solid_style(default_template, default_shapeline_color)),
        ("solid_thin", _get_solid_style(thin_template, default_shapeline_color)),
        ("solid_bold", _get_solid_style(bold_template, default_shapeline_color)),
        ("dashed", _get_dashed_style(default_template, default_shapeline_color)),
        ("dashed_thin", _get_dashed_style(thin_template, default_shapeline_color)),
        ("dashed_bold", _get_dashed_style(bold_template, default_shapeline_color)),
    ]

    for name, color in colors:
        for style_type in ["", "_flat", "_solid", "_dashed"]:
            for width_type, template in [("", default_template), ("_thin", thin_template), ("_bold", bold_template)]:

                if style_type == "":
                    if name in ["midnight_blue", "black"]:
                        named_styles.append((f"{name}{width_type}", _get_fill_style(template, color, Colors.White)))
                    else:
                        named_styles.append(
                            (f"{name}{width_type}", _get_fill_style(template, color, default_shapeline_color))
                        )

                elif style_type == "_flat":
                    if width_type == "":
                        named_styles.append((f"{name}_flat", _get_flat_style(template, color)))

                elif style_type == "_solid":
                    named_styles.append((f"{name}_solid{width_type}", _get_solid_style(template, color)))

                elif style_type == "_dashed":
                    named_styles.append((f"{name}_dashed{width_type}", _get_dashed_style(template, color)))

    return named_styles


def _get_fill_style(template: OfficialThemeTemplate, color, shape_line_color=None) -> ThemeStyles:
    t = template.copy()
    t.icon_color = color
    t.image_line_width = t.shape_line_width
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    return _generate_styles(t)


def _get_flat_style(template: OfficialThemeTemplate, color, shape_line_color=None) -> ThemeStyles:
    # image doesn't have border
    # shape has white border with white background

    t = template.copy()
    t.icon_color = color
    t.icon_style = "fill"
    t.image_line_width = 0
    t.line_color = color
    if shape_line_color is not None:
        t.shape_line_color = shape_line_color
    else:
        t.shape_line_color = color
    t.shape_fill_color = color
    t.shapetext_color = color
    t.text_color = color
    s = _generate_styles(t)
    s.linestyle = None
    s.linearrowstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_solid_style(template: OfficialThemeTemplate, color) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.shape_line_width
    t.line_color = color
    t.shape_line_color = color
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _get_dashed_style(template: OfficialThemeTemplate, color) -> ThemeStyles:
    t = template.copy()
    t.image_line_width = t.shape_line_width
    t.line_color = color
    t.line_style = "dashed"
    t.shape_line_color = color
    t.shape_line_style = "dashed"
    t.shape_fill_color = Colors.Transparent
    s = _generate_styles(t)
    s.iconstyle = None
    s.shapetextstyle = None
    s.textstyle = None
    return s


def _generate_styles(
    template: OfficialThemeTemplate,
    is_default: bool = False,
) -> ThemeStyles:
    if is_default:
        imagestyle_fcolor = None
    elif template.shape_fill_color == Colors.Transparent:
        imagestyle_fcolor = None
    else:
        imagestyle_fcolor = template.shape_fill_color

    return ThemeStyles(
        iconstyle=IconStyle(
            style=template.icon_style,
            color=template.icon_color,
            halign="center",
            valign="center",
        ),
        imagestyle=ImageStyle(
            lwidth=template.image_line_width,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
            fcolor=imagestyle_fcolor,
            halign="center",
            valign="center",
        ),
        linestyle=LineStyle(
            style=template.line_style,
            width=template.line_width,
            color=template.line_color,
        ),
        linearrowstyle=LineArrowStyle(
            lstyle=template.line_style,
            lwidth=template.line_width,
            hstyle=template.arrowhead_style,
            hscale=template.arrowhead_scale,
            color=template.line_color,
        ),
        shapestyle=ShapeStyle(
            lwidth=template.shape_line_width,
            lstyle=template.shape_line_style,
            lcolor=template.shape_line_color,
            fcolor=template.shape_fill_color,
            halign="center",
            valign="center",
        ),
        shapetextstyle=ShapeTextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.shapetext_color,
            halign="center",
            valign="center",
        ),
        textstyle=TextStyle(
            font=template.text_font,
            size=template.text_size,
            color=template.text_color,
            halign="center",
            valign="center",
        ),
    )
