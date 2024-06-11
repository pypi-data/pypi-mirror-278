# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib style theme

Define style theme at class ``Theme``.
Default or choosed theme is applied if style is not provided.
Instance ``dtheme``  is provided to user to control theme.

"""

from __future__ import annotations
from typing import Optional, Dict, Tuple, Union, Literal, List
from copy import deepcopy

from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
    ThemeStyles,
)
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.fonts import FontSourceCode
from drawlib.v0_1.private.core.theme_style_caches import (
    ThemeColorCache,
    BackgroundColorCache,
    SourceCodeFontCache,
    AbstractStyleCache,
    IconStyleCache,
    ImageStyleCache,
    LineStyleCache,
    LineArrowStyleCache,
    ShapeStyleCache,
    ShapeTextStyleCache,
    TextStyleCache,
    # Patch Styles
    ArcStyleCache,
    ArcTextStyleCache,
    CircleStyleCache,
    CircleTextStyleCache,
    DonutsStyleCache,
    DonutsTextStyleCache,
    EllipseStyleCache,
    EllipseTextStyleCache,
    FanStyleCache,
    FanTextStyleCache,
    PolygonStyleCache,
    PolygonTextStyleCache,
    RectangleStyleCache,
    RectangleTextStyleCache,
    RegularpolygonStyleCache,
    RegularpolygonTextStyleCache,
    WedgeStyleCache,
    WedgeTextStyleCache,
    # Original arrows
    ArrowStyleCache,
    ArrowTextStyleCache,
    # Original polygons
    ChevronStyleCache,
    ChevronTextStyleCache,
    ParallelogramStyleCache,
    ParallelogramTextStyleCache,
    RhombusStyleCache,
    RhombusTextStyleCache,
    StarStyleCache,
    StarTextStyleCache,
    TrapezoidStyleCache,
    TrapezoidTextStyleCache,
    TriangleStyleCache,
    TriangleTextStyleCache,
    # Smart art
    BubblespeechStyleCache,
    BubblespeechTextStyleCache,
)
import drawlib.v0_1.private.core.theme_officials as theme_officials


class AllStyleNameModifier:
    def __init__(self, theme: Theme):
        self._theme = theme

    @error_handler
    def list(self) -> List[str]:
        return self._theme._style_names.copy()

    @error_handler
    def copy(self, from_name: str, to_name: str) -> None:
        if from_name not in self._theme._style_names:
            raise ValueError(f'Original style name "{from_name}" does not exist.')

        for style in self._theme._get_style_caches():
            if not style.has(from_name):
                continue
            style.set(style.get(from_name), to_name)

    @error_handler
    def delete(self, name: str) -> None:
        if name == "":
            raise ValueError("Deleting default style name is prohibited.")

        for style in self._theme._get_style_caches():
            if not style.has(name):
                continue
            style.delete(name)

    @error_handler
    def rename(self, from_name: str, to_name: str) -> None:
        if from_name == "":
            raise ValueError("Renaming default style name is prohibited.")
        if from_name not in self._theme._style_names:
            raise ValueError(f'Original style name "{from_name}" does not exist.')

        index = self._theme._style_names.index(from_name)
        self.copy(from_name, to_name)
        self.delete(from_name)
        self._theme._style_names.pop()
        self._theme._style_names.insert(index, to_name)

    @error_handler
    def merge(self, theme_styles: ThemeStyles):
        # basics
        if theme_styles.iconstyle is not None:
            self._theme.iconstyles.merge(theme_styles.iconstyle)
        if theme_styles.imagestyle is not None:
            self._theme.imagestyles.merge(theme_styles.imagestyle)
        if theme_styles.linestyle is not None:
            self._theme.linestyles.merge(theme_styles.linestyle)
        if theme_styles.linearrowstyle is not None:
            self._theme.linearrowstyles.merge(theme_styles.linearrowstyle)
        if theme_styles.shapestyle is not None:
            self._theme.shapestyles.merge(theme_styles.shapestyle)
        if theme_styles.shapetextstyle is not None:
            self._theme.shapetextstyles.merge(theme_styles.shapetextstyle)
        if theme_styles.textstyle is not None:
            self._theme.textstyles.merge(theme_styles.textstyle)

        # patchs
        if theme_styles.arcstyle is not None:
            self._theme.arcstyles.merge(theme_styles.arcstyle)
        if theme_styles.arctextstyle is not None:
            self._theme.arctextstyles.merge(theme_styles.arctextstyle)
        if theme_styles.circlestyle is not None:
            self._theme.circlestyles.merge(theme_styles.circlestyle)
        if theme_styles.circletextstyle is not None:
            self._theme.circletextstyles.merge(theme_styles.circletextstyle)
        if theme_styles.donutsstyle is not None:
            self._theme.donutsstyles.merge(theme_styles.donutsstyle)
        if theme_styles.donutstextstyle is not None:
            self._theme.donutstextstyles.merge(theme_styles.donutstextstyle)
        if theme_styles.ellipsestyle is not None:
            self._theme.ellipsestyles.merge(theme_styles.ellipsestyle)
        if theme_styles.ellipsetextstyle is not None:
            self._theme.ellipsetextstyles.merge(theme_styles.ellipsetextstyle)
        if theme_styles.fanstyle is not None:
            self._theme.fanstyles.merge(theme_styles.fanstyle)
        if theme_styles.fantextstyle is not None:
            self._theme.fantextstyles.merge(theme_styles.fantextstyle)
        if theme_styles.polygonstyle is not None:
            self._theme.polygonstyles.merge(theme_styles.polygonstyle)
        if theme_styles.polygontextstyle is not None:
            self._theme.polygontextstyles.merge(theme_styles.polygontextstyle)
        if theme_styles.rectanglestyle is not None:
            self._theme.rectanglestyles.merge(theme_styles.rectanglestyle)
        if theme_styles.rectangletextstyle is not None:
            self._theme.rectangletextstyles.merge(theme_styles.rectangletextstyle)
        if theme_styles.regularpolygonstyle is not None:
            self._theme.regularpolygonstyles.merge(theme_styles.regularpolygonstyle)
        if theme_styles.regularpolygontextstyle is not None:
            self._theme.regularpolygontextstyles.merge(theme_styles.regularpolygontextstyle)
        if theme_styles.wedgestyle is not None:
            self._theme.wedgestyles.merge(theme_styles.wedgestyle)
        if theme_styles.wedgetextstyle is not None:
            self._theme.wedgetextstyles.merge(theme_styles.wedgetextstyle)

        # original
        if theme_styles.arrowstyle is not None:
            self._theme.arrowstyles.merge(theme_styles.arrowstyle)
        if theme_styles.arrowtextstyle is not None:
            self._theme.arrowtextstyles.merge(theme_styles.arrowtextstyle)
        if theme_styles.chevronstyle is not None:
            self._theme.chevronstyles.merge(theme_styles.chevronstyle)
        if theme_styles.chevrontextstyle is not None:
            self._theme.chevrontextstyles.merge(theme_styles.chevrontextstyle)
        if theme_styles.parallelogramstyle is not None:
            self._theme.parallelogramstyles.merge(theme_styles.parallelogramstyle)
        if theme_styles.parallelogramtextstyle is not None:
            self._theme.parallelogramtextstyles.merge(theme_styles.parallelogramtextstyle)
        if theme_styles.rhombusstyle is not None:
            self._theme.rhombusstyles.merge(theme_styles.rhombusstyle)
        if theme_styles.rhombustextstyle is not None:
            self._theme.rhombustextstyles.merge(theme_styles.rhombustextstyle)
        if theme_styles.starstyle is not None:
            self._theme.starstyles.merge(theme_styles.starstyle)
        if theme_styles.startextstyle is not None:
            self._theme.startextstyles.merge(theme_styles.startextstyle)
        if theme_styles.trapezoidstyle is not None:
            self._theme.trapezoidstyles.merge(theme_styles.trapezoidstyle)
        if theme_styles.trapezoidtextstyle is not None:
            self._theme.trapezoidtextstyles.merge(theme_styles.trapezoidtextstyle)
        if theme_styles.trianglestyle is not None:
            self._theme.trianglestyles.merge(theme_styles.trianglestyle)
        if theme_styles.triangletextstyle is not None:
            self._theme.triangletextstyles.merge(theme_styles.triangletextstyle)

        # smart art
        if theme_styles.bubblespeechstyle is not None:
            self._theme.bubblespeechstyles.merge(theme_styles.bubblespeechstyle)
        if theme_styles.bubblespeechtextstyle is not None:
            self._theme.bubblespeechtextstyles.merge(theme_styles.bubblespeechtextstyle)


class Theme:
    """Drawlib Thema control class.

    * define theme here
    * provide theme access methods

    """

    ThemeStyles = ThemeStyles

    @error_handler
    def __init__(self):
        self.allstyles = AllStyleNameModifier(self)
        self.apply_official_theme("default")

    @error_handler
    def list_official_themes(self) -> List[str]:
        return ["default", "simple", "rich", "monochrome"]

    @error_handler
    def apply_official_theme(
        self,
        name: Literal[
            "default",
            "default2",
            "essentials",
            "monochrome",
            # "flatui",
        ],
    ) -> None:
        if name == "default":
            t = theme_officials.get_default()
        elif name == "default2":
            t = theme_officials.get_default2()
        elif name == "essentials":
            t = theme_officials.get_essentials()
        elif name == "monochrome":
            t = theme_officials.get_monochrome()
        # elif name == "flatui":
        #     t = theme_officials.get_flatui()
        else:
            raise ValueError(f'Theme "{name}" is not supported.')

        self.apply_custom_theme(
            default_style=t.default_style,
            named_styles=t.named_styles,
            theme_colors=t.theme_colors,
            backgroundcolor=t.backgroundcolor,
            sourcecodefont=t.sourcecodefont,
        )

    @error_handler
    def apply_custom_theme(
        self,
        default_style: Theme.ThemeStyles,
        named_styles: List[
            Tuple[
                str,
                Theme.ThemeStyles,
            ]
        ] = [],
        theme_colors: List[Tuple[str, Union[Tuple[int, int, int], Tuple[int, int, int, float]]]] = [],
        backgroundcolor: Union[Tuple[int, int, int], Tuple[int, int, int, float]] = Colors.White,
        sourcecodefont: Optional[FontSourceCode] = FontSourceCode.SOURCECODEPRO,
    ) -> None:

        # initialize
        self._initialize()

        # set default background color
        _check_color(
            backgroundcolor,
            "default_style.backgroundcolor is mandatory. "
            "Format is (R, G, B) or (R, G, B, A). Where R,G,B is 0~255 and A is 0.0~1.0.",
        )
        self.backgroundcolors.set(backgroundcolor)

        # set default soucecode font
        if not isinstance(sourcecodefont, FontSourceCode):
            raise ValueError("default_style.sourcecodefont is mandatory. Type must be FontSourceCode.")
        self.sourcecodefonts.set(sourcecodefont)

        # set default styles
        if not isinstance(default_style.iconstyle, IconStyle):
            raise ValueError("default_style.iconstyle is mandatory. Type must be IconStyle.")
        self.iconstyles.set(default_style.iconstyle)

        if not isinstance(default_style.imagestyle, ImageStyle):
            raise ValueError("default_style.imagestyle is mandatory. Type must be ImageStyle.")
        self.imagestyles.set(default_style.imagestyle)

        if not isinstance(default_style.linestyle, LineStyle):
            raise ValueError("default_style.linestyle is mandatory. Type must be LineStyle.")
        self.linestyles.set(default_style.linestyle)

        if not isinstance(default_style.linearrowstyle, LineArrowStyle):
            raise ValueError("default_style.linearrowstyle is mandatory. Type must be LineArrowStyle.")
        self.linearrowstyles.set(default_style.linearrowstyle)

        if not isinstance(default_style.shapestyle, ShapeStyle):
            raise ValueError("default_style.shapestyle is mandatory. Type must be ShapeStyle.")
        self.shapestyles.set(default_style.shapestyle)

        if not isinstance(default_style.shapetextstyle, ShapeTextStyle):
            raise ValueError("default_style.shapetextstyle is mandatory. Type must be ShapeTextStyle.")
        self.shapetextstyles.set(default_style.shapetextstyle)

        if not isinstance(default_style.textstyle, TextStyle):
            raise ValueError("default_style.textstyle is mandatory. Type must be TextStyle.")
        self.textstyles.set(default_style.textstyle)

        for (
            shapestyle_name,
            shapestyle_object,
            shapestyle_setter,
            shapetextstyle_name,
            shapetextstyle_object,
            shapetextstyle_setter,
        ) in [
            (
                "default_style.arcstyle",
                default_style.arcstyle,
                self.arcstyles.set,
                "default_style.arctextstyle",
                default_style.arctextstyle,
                self.arctextstyles.set,
            ),
            (
                "default_style.circlestyle",
                default_style.circlestyle,
                self.circlestyles.set,
                "default_style.circletextstyle",
                default_style.circletextstyle,
                self.circletextstyles.set,
            ),
            (
                "default_style.ellipsestyle",
                default_style.ellipsestyle,
                self.ellipsestyles.set,
                "default_style.ellipsetextstyle",
                default_style.ellipsetextstyle,
                self.ellipsetextstyles.set,
            ),
            (
                "default_style.polygonstyle",
                default_style.polygonstyle,
                self.polygonstyles.set,
                "default_style.polygontextstyle",
                default_style.polygontextstyle,
                self.polygontextstyles.set,
            ),
            (
                "default_style.rectanglestyle",
                default_style.rectanglestyle,
                self.rectanglestyles.set,
                "default_style.rectangletextstyle",
                default_style.rectangletextstyle,
                self.rectangletextstyles.set,
            ),
            (
                "default_style.regularpolygonstyle",
                default_style.regularpolygonstyle,
                self.regularpolygonstyles.set,
                "default_style.regularpolygontextstyle",
                default_style.regularpolygontextstyle,
                self.regularpolygontextstyles.set,
            ),
            (
                "default_style.wedgestyle",
                default_style.wedgestyle,
                self.wedgestyles.set,
                "default_style.wedgetextstyle",
                default_style.wedgetextstyle,
                self.wedgetextstyles.set,
            ),
            (
                "default_style.donutsstyle",
                default_style.donutsstyle,
                self.donutsstyles.set,
                "default_style.donutstextstyle",
                default_style.donutstextstyle,
                self.donutstextstyles.set,
            ),
            (
                "default_style.fanstyle",
                default_style.fanstyle,
                self.fanstyles.set,
                "default_style.fantextstyle",
                default_style.fantextstyle,
                self.fantextstyles.set,
            ),
            (
                "default_style.arrowstyle",
                default_style.arrowstyle,
                self.arrowstyles.set,
                "default_style.arrowtextstyle",
                default_style.arrowtextstyle,
                self.arrowtextstyles.set,
            ),
            (
                "default_style.rhombusstyle",
                default_style.rhombusstyle,
                self.rhombusstyles.set,
                "default_style.rhombustextstyle",
                default_style.rhombustextstyle,
                self.rhombustextstyles.set,
            ),
            (
                "default_style.parallelogramstyle",
                default_style.parallelogramstyle,
                self.parallelogramstyles.set,
                "default_style.parallelogramtextstyle",
                default_style.parallelogramtextstyle,
                self.parallelogramtextstyles.set,
            ),
            (
                "default_style.trapezoidstyle",
                default_style.trapezoidstyle,
                self.trapezoidstyles.set,
                "default_style.trapezoidtextstyle",
                default_style.trapezoidtextstyle,
                self.trapezoidtextstyles.set,
            ),
            (
                "default_style.trianglestyle",
                default_style.trianglestyle,
                self.trianglestyles.set,
                "default_style.triangletextstyle",
                default_style.triangletextstyle,
                self.triangletextstyles.set,
            ),
            (
                "default_style.starstyle",
                default_style.starstyle,
                self.starstyles.set,
                "default_style.startextstyle",
                default_style.startextstyle,
                self.startextstyles.set,
            ),
            (
                "default_style.chevronstyle",
                default_style.chevronstyle,
                self.chevronstyles.set,
                "default_style.chevrontextstyle",
                default_style.chevrontextstyle,
                self.chevrontextstyles.set,
            ),
            (
                "default_style.bubblespeechstyle",
                default_style.bubblespeechstyle,
                self.bubblespeechstyles.set,
                "default_style.bubblespeechtextstyle",
                default_style.bubblespeechtextstyle,
                self.bubblespeechtextstyles.set,
            ),
        ]:

            if shapestyle_object is not None:
                if not isinstance(shapestyle_object, ShapeStyle):
                    raise ValueError(f"{shapestyle_name} is optional. But type must be None or ShapeStyle")
                shapestyle_setter(shapestyle_object)

            if shapetextstyle_object is not None:
                if not isinstance(shapetextstyle_object, ShapeTextStyle):
                    raise ValueError(f"{shapetextstyle_name} is optional. But type must be None or ShapeTextStyle")
                shapetextstyle_setter(shapetextstyle_object)

        # named styles
        for name, styles in named_styles:

            if styles.iconstyle is not None:
                if not isinstance(styles.iconstyle, IconStyle):
                    raise ValueError(f"name={name}, ThemeStyle.iconstyle type must be IconStyle.")
                self.iconstyles.set(styles.iconstyle, name)

            if styles.imagestyle is not None:
                if not isinstance(styles.imagestyle, ImageStyle):
                    raise ValueError(f"name={name}, ThemeStyle.imagestyle type must be ImageStyle.")
                self.imagestyles.set(styles.imagestyle, name)

            if styles.linestyle is not None:
                if not isinstance(styles.linestyle, LineStyle):
                    raise ValueError(f"name={name}, ThemeStyle.linestyle type must be LineStyle.")
                self.linestyles.set(styles.linestyle, name)

            if styles.linearrowstyle is not None:
                if not isinstance(styles.linearrowstyle, LineArrowStyle):
                    raise ValueError(f"name={name}, ThemeStyle.linearrowstyle type must be LineArrowStyle.")
                self.linearrowstyles.set(styles.linearrowstyle, name)

            if styles.shapestyle is not None:
                if not isinstance(styles.shapestyle, ShapeStyle):
                    raise ValueError(f"name={name}, ThemeStyle.shapestyle type must be ShapeStyle.")
                self.shapestyles.set(styles.shapestyle, name)

            if styles.shapetextstyle is not None:
                if not isinstance(styles.shapetextstyle, ShapeTextStyle):
                    raise ValueError(f"name={name}, ThemeStyle.shapetextstyle type must be ShapeTextStyle.")
                self.shapetextstyles.set(styles.shapetextstyle, name)

            if styles.textstyle is not None:
                if not isinstance(styles.textstyle, TextStyle):
                    raise ValueError(f"name={name}, ThemeStyle.textstyle type must be TextStyle.")
                self.textstyles.set(styles.textstyle, name)

            for (
                shapestyle_name,
                shapestyle_object,
                shapestyle_setter,
                shapetextstyle_name,
                shapetextstyle_object,
                shapetextstyle_setter,
            ) in [
                (
                    "arcstyle",
                    styles.arcstyle,
                    self.arcstyles.set,
                    "arctextstyle",
                    styles.arctextstyle,
                    self.arctextstyles.set,
                ),
                (
                    "circlestyle",
                    styles.circlestyle,
                    self.circlestyles.set,
                    "circletextstyle",
                    styles.circletextstyle,
                    self.circletextstyles.set,
                ),
                (
                    "ellipsestyle",
                    styles.ellipsestyle,
                    self.ellipsestyles.set,
                    "ellipsetextstyle",
                    styles.ellipsetextstyle,
                    self.ellipsetextstyles.set,
                ),
                (
                    "polygonstyle",
                    styles.polygonstyle,
                    self.polygonstyles.set,
                    "polygontextstyle",
                    styles.polygontextstyle,
                    self.polygontextstyles.set,
                ),
                (
                    "rectanglestyle",
                    styles.rectanglestyle,
                    self.rectanglestyles.set,
                    "rectangletextstyle",
                    styles.rectangletextstyle,
                    self.rectangletextstyles.set,
                ),
                (
                    "regularpolygonstyle",
                    styles.regularpolygonstyle,
                    self.regularpolygonstyles.set,
                    "regularpolygontextstyle",
                    styles.regularpolygontextstyle,
                    self.regularpolygontextstyles.set,
                ),
                (
                    "wedgestyle",
                    styles.wedgestyle,
                    self.wedgestyles.set,
                    "wedgetextstyle",
                    styles.wedgetextstyle,
                    self.wedgetextstyles.set,
                ),
                (
                    "donutsstyle",
                    styles.donutsstyle,
                    self.donutsstyles.set,
                    "donutstextstyle",
                    styles.donutstextstyle,
                    self.donutstextstyles.set,
                ),
                (
                    "fanstyle",
                    styles.fanstyle,
                    self.fanstyles.set,
                    "fantextstyle",
                    styles.fantextstyle,
                    self.fantextstyles.set,
                ),
                (
                    "arrowstyle",
                    styles.arrowstyle,
                    self.arrowstyles.set,
                    "arrowtextstyle",
                    styles.arrowtextstyle,
                    self.arrowtextstyles.set,
                ),
                (
                    "rhombusstyle",
                    styles.rhombusstyle,
                    self.rhombusstyles.set,
                    "rhombustextstyle",
                    styles.rhombustextstyle,
                    self.rhombustextstyles.set,
                ),
                (
                    "parallelogramstyle",
                    styles.parallelogramstyle,
                    self.parallelogramstyles.set,
                    "parallelogramtextstyle",
                    styles.parallelogramtextstyle,
                    self.parallelogramtextstyles.set,
                ),
                (
                    "trapezoidstyle",
                    styles.trapezoidstyle,
                    self.trapezoidstyles.set,
                    "trapezoidtextstyle",
                    styles.trapezoidtextstyle,
                    self.trapezoidtextstyles.set,
                ),
                (
                    "trianglestyle",
                    styles.trianglestyle,
                    self.trianglestyles.set,
                    "triangletextstyle",
                    styles.triangletextstyle,
                    self.triangletextstyles.set,
                ),
                (
                    "starstyle",
                    styles.starstyle,
                    self.starstyles.set,
                    "startextstyle",
                    styles.startextstyle,
                    self.startextstyles.set,
                ),
                (
                    "chevronstyle",
                    styles.chevronstyle,
                    self.chevronstyles.set,
                    "chevrontextstyle",
                    styles.chevrontextstyle,
                    self.chevrontextstyles.set,
                ),
                (
                    "bubblespeechstyle",
                    styles.bubblespeechstyle,
                    self.bubblespeechstyles.set,
                    "bubblespeechtextstyle",
                    styles.bubblespeechtextstyle,
                    self.bubblespeechtextstyles.set,
                ),
            ]:

                if shapestyle_object is not None:
                    if not isinstance(shapestyle_object, ShapeStyle):
                        raise ValueError(
                            f'name="{name}" ThemeStyles.{shapestyle_name} is optional.'
                            " But type must be None or ShapeStyle"
                        )
                    shapestyle_setter(shapestyle_object, name)

                if shapetextstyle_object is not None:
                    if not isinstance(shapetextstyle_object, ShapeTextStyle):
                        raise ValueError(
                            f'name="{name}" ThemeStyles.{shapetextstyle_name} is optional.'
                            " But type must be None or ShapeTextStyle"
                        )
                    shapetextstyle_setter(shapetextstyle_object, name)

        for t in theme_colors:
            if not isinstance(t, tuple):
                raise ValueError()
            if len(t) != 2:
                raise ValueError()

            name, theme_color = t
            if not isinstance(name, str):
                raise ValueError()
            _check_color(
                theme_color,
                f"name={name}, ThemeStyle.themecolors format must be (R,G,B) or (R,G,B,A). "
                "Format is (R, G, B) or (R, G, B, A). Where R,G,B is 0~255 and A is 0.0~1.0.",
            )

            self.colors.set(theme_color, name)

    @error_handler
    def print_theme_colors(self) -> None:
        print(self._get_theme_colors())

    @error_handler
    def print_style_table(self, max_columns: int = 11) -> None:
        print(self._get_style_table(max_columns))

    ###############
    ### Private ###
    ###############

    @error_handler
    def _initialize(self) -> None:
        """Initialize theme.

        This method need to be called before setting manual theme.

        Returns:
            None

        """

        self._style_names: List[str] = []

        self.colors = ThemeColorCache()
        self.backgroundcolors = BackgroundColorCache()
        self.sourcecodefonts = SourceCodeFontCache()
        self.iconstyles = IconStyleCache(self._callback_set, self._callback_delete)
        self.imagestyles = ImageStyleCache(self._callback_set, self._callback_delete)
        self.linestyles = LineStyleCache(self._callback_set, self._callback_delete)
        self.linearrowstyles = LineArrowStyleCache(self._callback_set, self._callback_delete)
        self.shapestyles = ShapeStyleCache(self._callback_set, self._callback_delete)
        self.shapetextstyles = ShapeTextStyleCache(self._callback_set, self._callback_delete)
        self.textstyles = TextStyleCache(self._callback_set, self._callback_delete)

        # patchs
        self.arcstyles = ArcStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.arctextstyles = ArcTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.circlestyles = CircleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.circletextstyles = CircleTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.donutsstyles = DonutsStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.donutstextstyles = DonutsTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.ellipsestyles = EllipseStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.ellipsetextstyles = EllipseTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.fanstyles = FanStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.fantextstyles = FanTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.polygonstyles = PolygonStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.polygontextstyles = PolygonTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.rectanglestyles = RectangleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.rectangletextstyles = RectangleTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.regularpolygonstyles = RegularpolygonStyleCache(
            self.shapestyles, self._callback_set, self._callback_delete
        )
        self.regularpolygontextstyles = RegularpolygonTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.wedgestyles = WedgeStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.wedgetextstyles = WedgeTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)

        # original arrows
        self.arrowstyles = ArrowStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.arrowtextstyles = ArrowTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)

        # original polygons
        self.chevronstyles = ChevronStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.chevrontextstyles = ChevronTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.parallelogramstyles = ParallelogramStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.parallelogramtextstyles = ParallelogramTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.rhombusstyles = RhombusStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.rhombustextstyles = RhombusTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.starstyles = StarStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.startextstyles = StarTextStyleCache(self.shapetextstyles, self._callback_set, self._callback_delete)
        self.trapezoidstyles = TrapezoidStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.trapezoidtextstyles = TrapezoidTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )
        self.trianglestyles = TriangleStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.triangletextstyles = TriangleTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )

        # smart art
        self.bubblespeechstyles = BubblespeechStyleCache(self.shapestyles, self._callback_set, self._callback_delete)
        self.bubblespeechtextstyles = BubblespeechTextStyleCache(
            self.shapetextstyles, self._callback_set, self._callback_delete
        )

    def _get_style_caches(self) -> List[AbstractStyleCache]:
        styles: List[AbstractStyleCache] = [
            self.iconstyles,
            self.imagestyles,
            self.linestyles,
            self.linearrowstyles,
            self.shapestyles,
            self.shapetextstyles,
            self.textstyles,
            # patchs
            self.arcstyles,
            self.arctextstyles,
            self.circlestyles,
            self.circletextstyles,
            self.donutsstyles,
            self.donutstextstyles,
            self.ellipsestyles,
            self.ellipsetextstyles,
            self.fanstyles,
            self.fantextstyles,
            self.polygonstyles,
            self.polygontextstyles,
            self.rectanglestyles,
            self.rectangletextstyles,
            self.regularpolygonstyles,
            self.regularpolygontextstyles,
            self.wedgestyles,
            self.wedgetextstyles,
            # original arrows
            self.arrowstyles,
            self.arrowtextstyles,
            # original polygons
            self.chevronstyles,
            self.chevrontextstyles,
            self.parallelogramstyles,
            self.parallelogramtextstyles,
            self.rhombusstyles,
            self.rhombustextstyles,
            self.starstyles,
            self.startextstyles,
            self.trapezoidstyles,
            self.trapezoidtextstyles,
            self.trianglestyles,
            self.triangletextstyles,
            # smart art
            self.bubblespeechstyles,
            self.bubblespeechtextstyles,
        ]
        return styles

    def _get_theme_colors(self) -> str:
        max_len = 0
        for name in self.colors.list():
            if len(name) > max_len:
                max_len = len(name)

        lines = []
        for name in self.colors.list():
            c = self.colors.get(name)
            c0 = str(c[0]).rjust(3)
            c1 = str(c[1]).rjust(3)
            c2 = str(c[2]).rjust(3)
            color_text = f"({c0}, {c1}, {c2}, {c[3]})"
            lines.append(f"{name.ljust(max_len)}: {color_text}")

        return "\n".join(lines).strip()

    def _get_style_table(self, max_columns: int = 11) -> str:
        if not isinstance(max_columns, int):
            raise ValueError("Arg max_columns must be int 2+")
        if max_columns < 2:
            raise ValueError("Arg max_columns must be int 2+")

        col1: List[str] = [
            "class \\ name",
            "IconStyle",
            "ImageStyle",
            "LineStyle",
            "LineArrowStyle",
            "ShapeStyle",
            "ShapeTextStyle",
            "TextStyle",
        ]

        row_objects = [
            self.iconstyles,
            self.imagestyles,
            self.linestyles,
            self.linearrowstyles,
            self.shapestyles,
            self.shapetextstyles,
            self.textstyles,
        ]

        def get_text(style_names: List[str]) -> str:
            lines: List[str] = []

            # create columns
            cols: List[List[str]] = [col1]
            for style_name in style_names:
                col: List[str] = [style_name]
                for row_object in row_objects:
                    if row_object.has(style_name):
                        col.append("x")
                    else:
                        col.append("")
                cols.append(col)

            # modify text length
            cols2 = []
            for col in cols:
                max_length = max(len(s) for s in col)
                padded_strings = [s.ljust(max_length) for s in col]
                cols2.append(padded_strings)

            def draw_border():
                text = "+"
                for col in cols2:
                    t = "-" * (len(col[0]) + 2)
                    text += f"{t}+"
                lines.append(text)

            for i in range(len(col1)):
                if i == 0:
                    draw_border()

                text = "|"
                for col in cols2:
                    text += f" {col[i]} |"
                lines.append(text)

                if i == 0:
                    draw_border()

                if i == len(col1) - 1:
                    draw_border()

            return "\n".join(lines).strip()

        def split_list(input_list, chunk_size):
            result = []
            for i in range(0, len(input_list), chunk_size):
                chunk = input_list[i : i + chunk_size]
                result.append(chunk)
            return result

        texts = []
        list_of_list = split_list(self._style_names, max_columns - 1)
        for style_names in list_of_list:
            texts.append(get_text(style_names))

        return "\n\n".join(texts).strip()

    def _callback_set(self, name: str):
        if name in self._style_names:
            return

        self._style_names.append(name)

    def _callback_delete(self, name: str):
        if name not in self._style_names:
            return

        name_exist = False
        for style in self._get_style_caches():
            if style.has(name):
                name_exist = True
                break

        if not name_exist:
            self._style_names.remove(name)


def _check_color(color, error_message: str):

    if not isinstance(color, tuple):
        raise ValueError(error_message)
    if len(color) not in [3, 4]:
        raise ValueError(error_message)

    for i in [color[0], color[1], color[2]]:
        if not isinstance(i, int):
            raise ValueError(error_message)
        if not 0 <= i <= 255:
            raise ValueError(error_message)

    if len(color) == 4:
        alpha = color[3]
        if isinstance(alpha, int) or isinstance(alpha, float):
            if 0.0 <= alpha <= 1.0:
                # ok
                ...
            else:
                raise ValueError(error_message)
        else:
            raise ValueError(error_message)


dtheme = Theme()
"""Singleton instance of class ``Theme``."""
