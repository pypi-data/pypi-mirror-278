"""
Module to define style classes.
"""

# pylint: disable=too-few-public-methods

from typing import TypedDict
from typing_extensions import Unpack
import osvg.float


def verify_hex_string(hex_value: str) -> bool:
    """
    Verify if given string represents a hexadecimal value
    """
    try:
        int(hex_value, 16)
    except (TypeError, ValueError):
        return False
    return True


def verify_color_value(value):
    """
    Verify if given string is a valid value for a color style attribute
    """
    if (
        value is not None
        and value != "none"
        and (
            not isinstance(value, str)
            or len(value) != 6
            or not verify_hex_string(value)
        )
    ):
        raise TypeError("hex_def must be a string of 6 hex values or 'none'")


class StyleStringAttribute:
    """
    Parent class for all style attributes.
    """

    key = ""

    def __init__(self, value: str = None) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        """
        Get value
        """
        return self._value

    def _verify_value(self, value):
        """
        Verify value
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("Style attribute value must be a string")

    @property
    def isdefault(self) -> bool:
        """
        Check, if object's value is not set.
        """
        return self.value is None

    def equals(self, other) -> bool:
        """
        Check, if other's string value is equal to self's string value
        """
        return self.value == other.value

    @value.setter
    def value(self, value):
        """
        Verify and set value
        """
        self._verify_value(value)
        self._value = value

    def __str__(self) -> str:
        return "" if self.value is None else f"{self.key}:{self.value}"

    def copy(self):
        """
        Return an object with the same string as value
        """
        return self.__class__(value=self.value)


class StyleFloatAttribute:
    """
    Parent class for all style attributes.
    """

    key = ""
    value = osvg.float.FloatProperty()
    str_round = 3

    def __init__(self, value: int | float | osvg.float.Float = None) -> None:
        self.value = value

    def __str__(self) -> str:
        return (
            ""
            if self.value.value is None
            else f"{self.key}:{round(self.value.value, self.str_round):g}"
        )

    def copy(self):
        """
        Return an object with the same float value as value
        """
        return self.__class__(value=self.value.float_ref)

    @property
    def isdefault(self) -> bool:
        """
        Check, if object's value is not set.
        """
        return self.value.value is None

    def equals(self, other) -> bool:
        """
        Check, if other's float value is equal to self's float value
        """
        return self.value.value == other.value.value


class Color(StyleStringAttribute):
    """
    SVG representation of a color in string of hex values or "none".
    "rrggbb" ->:
        - "rr" 256 bit value for red
        - "gg" 256 bit value for green
        - "bb" 256 bit value for blue
    """

    def __init__(self, value: str = None) -> None:
        super().__init__(value=value)

    def _verify_value(self, value):
        verify_color_value(value)

    def __str__(self) -> str:
        if self.value == "none":
            return f"{self.key}:none"
        return "" if self.value is None else f"{self.key}:#{self.value}"


class Opacity(StyleFloatAttribute):
    """
    SVG representation of a opacity in float 0 <= value <= 1
    with 1 is 100% opacity.
    """

    key = "opacity"

    def __init__(self, value: int | float | osvg.float.Float = None) -> None:
        super().__init__(value=value)

    @property
    def opacity(self) -> float:
        """
        Get opacity float value
        """
        return self.value.value

    @opacity.setter
    def opacity(self, value: int | float | osvg.float.Float):
        """
        Set opacity
        """
        self.value = value


class FillColor(Color):
    """
    SVG Style Attribute "fill"
    """

    key = "fill"


class FillOpacity(Opacity):
    """
    SVG Style Attribute "fill-opacity"
    """

    key = "fill-opacity"


class StrokeColor(Color):
    """
    SVG Style Attribute "stroke"
    """

    key = "stroke"


class StrokeOpacity(Opacity):
    """
    SVG Style Attribute "stroke-opacity"
    """

    key = "stroke-opacity"


class StrokeWidth(StyleFloatAttribute):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-width"

    def __init__(self, value: int | float | osvg.float.Float = None) -> None:
        super().__init__(value=value)


class StrokeLineCap(StyleStringAttribute):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-linecap"

    def __init__(self, value: str = None) -> None:
        if value and value not in ["butt", "round", "square"]:
            raise ValueError(f"'{value}' not a valid linecap option")
        super().__init__(value=value)


class StrokeDashArray(osvg.float.FloatList):
    """
    SVG Style Attribute "stroke-width"
    """

    key = "stroke-dasharray"
    name = "values"

    def __str__(self) -> str:
        if not self.values:
            return ""
        return f"{self.key}:{super().__str__()}"


class StrokeLineJoin(StyleStringAttribute):
    """
    SVG Style Attribute "stroke-linejoin"
    """

    key = "stroke-linejoin"

    def __init__(self, value: str = None) -> None:
        if value and value not in [
            "arcs",
            "bevel",
            "miter",
            "miter-clip",
            "round",
        ]:
            raise ValueError(f"'{value}' not a valid linecap option")
        super().__init__(value=value)


class FontFamily(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-family"
    """

    key = "font-family"


class FontSize(StyleFloatAttribute):
    """
    SVG Font Style Attribute "font-size" in pixels
    """

    key = "font-size"

    def __str__(self) -> str:
        return (
            ""
            if self.value.value is None
            else f"{self.key}:{round(self.value.value, self.str_round):g}px"
        )


class FontSizeAdjust(StyleFloatAttribute):
    """
    SVG Font Style Attribute "font-size-adjust" in pixels
    """

    key = "font-size-adjust"


class FontStretch(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-stretch"
    """

    key = "font-stretch"


class FontStyle(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-style"
    """

    key = "font-style"
    allowed_values = [
        "normal",
        "italic",
        "oblique",
    ]

    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        if value is not None and value not in self.allowed_values:
            raise ValueError(
                f"font-style value mus be on of {','.join(self.allowed_values)}"
            )


class FontVariant(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-variant"
    """

    key = "font-variant"


class FontWeigth(StyleStringAttribute):
    """
    SVG Font Style Attribute "font-weigth"
    """

    key = "font-weight"
    allowed_values = [
        "normal",
        "bold",
        "bolder",
        "lighter",
    ]

    def __init__(self, value: str = None) -> None:
        super().__init__(value)
        if value is not None and value not in self.allowed_values:
            raise ValueError(
                f"font-weigth value must be on of {','.join(self.allowed_values)}"
            )


class StyleParamTypes(TypedDict):
    """
    Parameter type hint for class Style
    """

    opacity: Opacity | float | int
    fill_color: FillColor | str
    fill_opacity: FillOpacity | float | int
    stroke_color: StrokeColor | str
    stroke_opacity: StrokeOpacity | float | int
    stroke_width: StrokeWidth | float | int
    stroke_linecap: StrokeLineCap | str
    stroke_linejoin: StrokeLineJoin | str
    stroke_dasharray: StrokeDashArray | str
    font_family: FontFamily | str
    font_size: FontSize | float | int
    font_size_adjust: FontSizeAdjust | float | int
    font_stretch: FontStretch | str
    font_style: FontStyle | str
    font_variant: FontVariant | str
    font_weigth: FontWeigth | str
    reference: "Style"


class Style:
    """
    SVG Style representative.
    """

    param_classes = {
        "opacity": Opacity,
        "fill_color": FillColor,
        "fill_opacity": FillOpacity,
        "stroke_color": StrokeColor,
        "stroke_opacity": StrokeOpacity,
        "stroke_width": StrokeWidth,
        "stroke_linecap": StrokeLineCap,
        "stroke_linejoin": StrokeLineJoin,
        "stroke_dasharray": StrokeDashArray,
        "font_family": FontFamily,
        "font_size": FontSize,
        "font_size_adjust": FontSizeAdjust,
        "font_stretch": FontStretch,
        "font_style": FontStyle,
        "font_variant": FontVariant,
        "weigth": FontWeigth,
    }

    def __init__(self, **kwargs: Unpack[StyleParamTypes]) -> None:
        self.attributes = self.param_classes.copy()
        if "reference" in kwargs:
            ref_obj = kwargs["reference"]
            for attr in self.attributes:
                self.attributes[attr] = ref_obj.attributes[attr]
        for attr, _class in self.param_classes.items():
            if attr in kwargs:
                attr_obj = kwargs[attr]
                if not isinstance(attr_obj, _class):
                    attr_obj = _class(attr_obj)
                self.attributes[attr] = attr_obj
            elif "reference" not in kwargs:
                self.attributes[attr] = _class()

    def __str__(self) -> str:
        """
        SVG font style string
        """
        return_kvs = []
        for attr_v in self.attributes.values():
            if str(attr_v):
                return_kvs.append(str(attr_v))
        return ";".join(return_kvs)

    def copy(self) -> "Style":
        """
        Return an object with same atrributes.
        """
        obj = Style()
        for k, v in self.attributes.items():
            obj.attributes[k] = v.copy()
        return obj

    def merge(self, other: "Style") -> None:
        """
        Overwrite with all not 'None' values
        """
        for k, v in other.attributes.items():
            if isinstance(v, StyleStringAttribute):
                if v.value is not None:
                    self.attributes[k] = v.copy()
            if isinstance(v, StyleFloatAttribute):
                if v.value.value is not None:
                    self.attributes[k] = v.copy()
            elif isinstance(v, StrokeDashArray):
                if v.values != []:
                    self.attributes[k] = v.copy()

    def diff(self, other: "Style") -> "Style":
        """
        Return style object with only attributes which are overwritten in 'other'
        """
        style = Style()
        for k, v in other.attributes.items():
            if isinstance(v, StyleStringAttribute):
                if v.value is not None and v.value != self.attributes[k].value:
                    style.attributes[k] = v.copy()
            if isinstance(v, StyleFloatAttribute):
                if (
                    v.value.value is not None
                    and v.value.value != self.attributes[k].value.value
                ):
                    style.attributes[k] = v.copy()
            elif isinstance(v, StrokeDashArray):
                if v.values not in ([], self.attributes[k].values):
                    style.attributes[k] = v.copy()
        return style

    @property
    def stroke_width(self) -> float | None:
        """
        Get stroke width value
        """
        return self.attributes["stroke_width"].value.value
