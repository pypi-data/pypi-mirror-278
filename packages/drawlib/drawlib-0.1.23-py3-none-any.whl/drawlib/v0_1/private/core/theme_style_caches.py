from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, Union, Any, Optional
import re

from drawlib.v0_1.private.util import error_handler
from drawlib.v0_1.private.core.model import (
    IconStyle,
    ImageStyle,
    LineStyle,
    LineArrowStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_1.private.core.model_util import (
    IconUtil,
    ImageUtil,
    LineUtil,
    ShapeUtil,
    TextUtil,
)
from drawlib.v0_1.private.core.fonts import FontSourceCode
import drawlib.v0_1.private.validators.color as color_validator
import drawlib.v0_1.private.validators.style as style_validator
import drawlib.v0_1.private.validators.types as type_validator

list_ = list


def _get_name_and_widthtimes(style: str) -> Tuple[str, float]:
    match = re.search(r"\.(\d+)$", style)
    if match is None:
        return style, 1.0

    value = int(match.group(1))
    return style.replace(f".{value}", ""), value / 100


class ThemeColorCache:
    def __init__(self) -> None:
        self._colors: Dict[str, Tuple[int, int, int, float]] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._colors

    @error_handler
    def get(self, name: str = "") -> Tuple[int, int, int, float]:
        if not self.has(name):
            raise ValueError(f'Theme colors name "' + name + '" does not exist.')
        return self._colors[name]

    @error_handler
    def list(self) -> List[str]:
        return list_(self._colors.keys())

    @error_handler
    def set(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        name: str = "",
    ) -> None:
        color_validator.validate_color("color", color)
        type_validator.validate_str("name", name)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 1.0)
        self._colors[name] = color

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme colors name "' + name + '" does not exist.')
        del self._colors[name]


class BackgroundColorCache:
    def __init__(self) -> None:
        self._colors: Dict[str, Tuple[int, int, int, float]] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._colors

    @error_handler
    def get(self, name: str = "") -> Tuple[int, int, int, float]:
        if not self.has(name):
            raise ValueError(f'Theme background-color name "' + name + '" does not exist.')
        return self._colors[name]

    @error_handler
    def list(self) -> List[str]:
        return list_(self._colors.keys())

    @error_handler
    def set(
        self,
        color: Union[Tuple[int, int, int], Tuple[int, int, int, float]],
        name: str = "",
    ) -> None:
        color_validator.validate_color("color", color)
        type_validator.validate_str("name", name)
        if len(color) == 3:
            color = (color[0], color[1], color[2], 1.0)
        self._colors[name] = color

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme background-color name "' + name + '" does not exist.')
        del self._colors[name]


class SourceCodeFontCache:
    def __init__(self) -> None:
        self._fonts: Dict[str, FontSourceCode] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        return name in self._fonts

    @error_handler
    def get(self, name: str = "") -> FontSourceCode:
        if not self.has(name):
            raise ValueError(f'Theme sourcecode-font name "' + name + '" does not exist.')
        return self._fonts[name]

    @error_handler
    def list(self) -> List[str]:
        return list_(self._fonts.keys())

    @error_handler
    def set(
        self,
        font: FontSourceCode,
        name: str = "",
    ) -> None:
        if not isinstance(font, FontSourceCode):
            raise ValueError("Arg font must be FontSourceCode.")
        type_validator.validate_str("name", name)

        self._fonts[name] = font

    @error_handler
    def delete(self, name: str) -> None:
        if not self.has(name):
            raise ValueError(f'Theme sourcecode-font name "' + name + '" does not exist.')
        del self._fonts[name]


class AbstractStyleCache(ABC):
    @abstractmethod
    def has(self, name: str) -> bool: ...

    @abstractmethod
    def get(self, name: str = "") -> Any: ...

    @abstractmethod
    def list(self) -> List[str]: ...

    @abstractmethod
    def set(self, style: Any, name: str = "") -> None: ...

    @abstractmethod
    def delete(self, name: str) -> None: ...

    @abstractmethod
    def merge(self, style: Any, targets: Optional[List[str]] = None) -> None: ...


class IconStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, IconStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> IconStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: IconStyle, name: str = "") -> None:
        style_validator.validate_iconstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: IconStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_iconstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = IconUtil.merge_style(style, original_style)
            self.set(merged_style, target)


class ImageStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ImageStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ImageStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ImageStyle, name: str = "") -> None:
        style_validator.validate_imagestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ImageStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_imagestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ImageUtil.merge_style(style, original_style)
            self.set(merged_style, target)


class LineStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, LineStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> LineStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: LineStyle, name: str = "") -> None:
        style_validator.validate_linestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: LineStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_linestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = LineUtil.merge_line_style(style, original_style)
            self.set(merged_style, target)


class LineArrowStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, LineArrowStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> LineArrowStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: LineArrowStyle, name: str = "") -> None:
        style_validator.validate_linearrowstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: LineArrowStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_linearrowstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = LineUtil.merge_linearrow_style(style, original_style)
            self.set(merged_style, target)


class ShapeStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class ShapeTextStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> ShapeTextStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class TextStyleCache(AbstractStyleCache):
    def __init__(self, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, TextStyle] = dict()

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "") -> TextStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        style = self._styles[name].copy()
        if width_times == 1.0:
            ...
        elif hasattr(style, "width"):
            style.width = style.width * width_times
        elif hasattr(style, "lwidth"):
            style.lwidth = style.lwidth * width_times
        else:
            ...
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: TextStyle, name: str = "") -> None:
        style_validator.validate_textstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: TextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_textstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = TextUtil.merge_style(style, original_style)
            self.set(merged_style, target)


class ArcStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class CircleStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class DonutsStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class EllipseStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class FanStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class PolygonStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class RectangleStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class RegularpolygonStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class WedgeStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class ArrowStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class ChevronStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class ParallelogramStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class RhombusStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class StarStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class TrapezoidStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class TriangleStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class BubblespeechStyleCache(AbstractStyleCache):
    def __init__(self, shapestyles: ShapeStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeStyle] = dict()
        self._shapestyles = shapestyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapestyles_if_not_exist: bool = True) -> ShapeStyle:
        name, width_times = _get_name_and_widthtimes(name)
        if self.has(name):
            style = self._styles[name].copy()
        elif use_shapestyles_if_not_exist:
            style = self._shapestyles.get(name)
        else:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')

        if width_times == 1.0:
            return style

        style.lwidth = style.lwidth * width_times
        return style

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeStyle, name: str = "") -> None:
        style_validator.validate_shapestyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapestyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shape_style(style, original_style)
            self.set(merged_style, target)


class ArcTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class CircleTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class DonutsTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class EllipseTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class FanTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class PolygonTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class RectangleTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class RegularpolygonTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class WedgeTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class ArrowTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class ChevronTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class ParallelogramTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class RhombusTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class StarTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class TrapezoidTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class TriangleTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)


class BubblespeechTextStyleCache(AbstractStyleCache):
    def __init__(self, shapetextstyles: ShapeTextStyleCache, callback_set, callback_delete) -> None:
        self._callback_set = callback_set
        self._callback_delete = callback_delete
        self._styles: Dict[str, ShapeTextStyle] = dict()
        self._shapetextstyles = shapetextstyles

    @error_handler
    def has(self, name: str) -> bool:
        """Whether having theme name or not"""
        name, _ = _get_name_and_widthtimes(name)
        return name in self._styles

    @error_handler
    def get(self, name: str = "", use_shapetextstyles_if_not_exist: bool = True) -> ShapeTextStyle:
        name, _ = _get_name_and_widthtimes(name)
        if self.has(name):
            return self._styles[name].copy()
        if not use_shapetextstyles_if_not_exist:
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        return self._shapetextstyles.get(name)

    @error_handler
    def list(self) -> List[str]:
        return list_(self._styles.keys())

    @error_handler
    def set(self, style: ShapeTextStyle, name: str = "") -> None:
        style_validator.validate_shapetextstyle("style", style)
        type_validator.validate_str("name", name)
        if "." in name:
            raise ValueError('Theme style name must not have ".".')

        self._styles[name] = style.copy()
        self._callback_set(name)

    @error_handler
    def delete(self, name: str) -> None:
        name, _ = _get_name_and_widthtimes(name)
        if not self.has(name):
            raise ValueError(f'Theme style name "' + name + '" does not exist.')
        del self._styles[name]
        self._callback_delete(name)

    @error_handler
    def merge(self, style: ShapeTextStyle, targets: Optional[List[str]] = None) -> None:
        style_validator.validate_shapetextstyle("style", style)
        if targets is None:
            targets = self.list()
        for target in targets:
            if not self.has(target):
                continue
            original_style = self.get(target)
            merged_style = ShapeUtil.merge_shapetext_style(style, original_style)
            self.set(merged_style, target)
