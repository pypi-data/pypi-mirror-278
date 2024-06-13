"""
Module to define class for SVG ellipse elements.
"""

import xml.etree.ElementTree as ET
from typing import TypedDict
from collections.abc import Iterable
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.positions
import osvg.float
import osvg.float_math


class GlyphRotation(osvg.float.FloatList):
    """
    Text rotate
    """

    name = "glyph_rotation"
    svg_attribute = "rotate"


class TextOrientationParams(TypedDict):
    """
    Additional Keyword argument definitions for Text classes.
    """

    width: float | int | osvg.float.Float
    width_adjust: str
    alignment_baseline: str
    text_anchor: str
    word_spacing: str
    writing_mode: str
    glyph_rotation: Iterable[float | int | osvg.float.Float]


TextOrientationParamsInfo = {
    "width_adjust": {
        "default": "spacing",
        "svg_attribute": "textAdjust",
    },
    "alignment_baseline": {
        "default": "auto",
        "svg_attribute": "alignment-baseline",
    },
    "text_anchor": {
        "default": "start",
        "svg_attribute": "text-anchor",
    },
    "word_spacing": {
        "default": "normal",
        "svg_attribute": "word-spacing",
    },
    "writing_mode": {
        "default": "horizontal-tb",
        "svg_attribute": "writing-mode",
    },
}


class _TextBase(osvg.elements.elementbase.SVGElement):
    """
    Base class for Text and TextSpan classes.
    """

    width = osvg.float.FloatProperty()

    def __init__(self, text: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.text = text
        self.text_anchor = None
        self.width = kwargs.get("width", 0)
        for attr, info in TextOrientationParamsInfo.items():
            self.__dict__[attr] = kwargs.get(attr, info["default"])
        self.glyph_rotation = GlyphRotation(values=kwargs.get("glyph_rotation", None))
        self.create_default_connectors()

    def create_default_connectors(self):
        """
        Create Positions as connectors and add them.
        """
        x_shift_left = osvg.float.Const(0)
        x_shift_right = osvg.float.Const(0)
        if self.text_anchor == "start":
            x_shift_right = self.width
        elif self.text_anchor == "middle":
            x_shift_left = osvg.float_math.Prod(self.width, -0.5)
            x_shift_right = osvg.float_math.Prod(self.width, 0.5)
        elif self.text_anchor == "end":
            x_shift_left = osvg.float_math.Prod(self.width, -1)
        self.add_connector(
            position=osvg.positions.ShiftedPosition(
                origin=self.position, x_shift=x_shift_left
            ),
            name="left",
            respect_rotation=True,
        )
        self.add_connector(
            position=osvg.positions.ShiftedPosition(
                origin=self.position, x_shift=x_shift_right
            ),
            name="right",
            respect_rotation=True,
        )

    @property
    def _plain_etree_element(self) -> ET.Element:
        element = super()._plain_etree_element
        element.text = self.text
        return element

    def _add_orientation_attributes(self, element: ET.Element) -> None:
        """
        Add "orientation" SVG attributes to element
        """
        if str(self.width) != "0":
            element.set("textLenght", str(self.width))
        for attr, info in TextOrientationParamsInfo.items():
            if self.__dict__[attr] != info["default"]:
                element.set(info["svg_attribute"], str(self.__dict__[attr]))
        if not self.glyph_rotation.isdefault:
            element.set(self.glyph_rotation.svg_attribute, str(self.glyph_rotation))


class TextSpanParams(TextOrientationParams):
    """
    Keyword argument definition for TextSpan class.
    """

    dx: float | int | osvg.float.Float | str = None
    dy: float | int | osvg.float.Float | str = None
    align_with_parent: bool = False
    style: osvg.style.Style = None
    hyperlink: str = None


class TextSpan(_TextBase):
    """
    SVGP Tspan class. See: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/tspan
    """

    xml_tag = "tspan"
    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()

    def __init__(
        self, parent: "TextSpan | Text", text: str, **kwargs: Unpack[TextSpanParams]
    ) -> None:
        if not issubclass(type(parent), _TextBase):
            raise TypeError("Parent must be a subclass of Text or TextSpan")
        kwargs["parent"] = parent
        self.align_with_parent = kwargs.get("align_with_parent", False)
        kwargs["width"] = kwargs.get(
            "width", parent.width if self.align_with_parent else 0
        )
        super().__init__(text=text, **kwargs)
        self._dx = None
        self.dx = kwargs.get("dx", None)
        self._dy = None
        self.dy = kwargs.get("dy", None)

    @property
    def dx(self):
        """
        Get dx
        """
        return self._dx

    @dx.setter
    def dx(self, dx: float | int | osvg.float.Float | str):
        """
        Set dx
        """
        if dx is None:
            self.x = self.parent.position.x if self.align_with_parent else None
            self._dx = None
            return
        self.x = None
        if isinstance(dx, str):
            self._dx = dx
            return
        if not issubclass(type(dx), osvg.float.Float):
            dx = osvg.float.Const(dx)
        self._dx = osvg.float.RefFloat(float_ref=dx)

    @property
    def dy(self):
        """
        Get dy
        """
        return self._dy

    @dy.setter
    def dy(self, dy: float | int | osvg.float.Float | str):
        """
        Set dy
        """
        if dy is None:
            self.y = self.parent.position.y if self.align_with_parent else None
            self._dy = None
            return
        self.y = None
        if isinstance(dy, str):
            self._dy = dy
            return
        if not issubclass(type(dy), osvg.float.Float):
            dy = osvg.float.Const(dy)
        self._dy = osvg.float.RefFloat(float_ref=dy)

    @property
    def _plain_etree_element(self) -> ET.Element:
        element = super()._plain_etree_element
        if self.dx is None:
            if self.x.value is not None:
                element.set("x", str(self.x))
        else:
            element.set("dx", str(self.dx))
        if self.dy is None:
            if self.y.value is not None:
                element.set("y", str(self.y))
        else:
            element.set("dy", str(self.dy))
        self._add_orientation_attributes(element=element)
        self.add_element_rotation(element=element)
        return element


class TextParams(TextOrientationParams, osvg.elements.elementbase.SVGElementParams):
    """
    Keyword argument definitions for Text classes.
    """


class Text(_TextBase):
    """
    SVG Text class. See: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/text

    Parameters:
        - text: str
        - width ==> "textLength"
        - width_adjust ==> "lengthAdjust"
        - glyph_rotation ==> "rotate"
        - alignment_baseline ==> "alignment-baseline":
                https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/alignment-baseline
        - text_anchor ==> "text-anchor":
                https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-anchor
        - word_spacing ==> "word-spacing":
                https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/word-spacing
        - writing_mode ==> "writing-mode":
                https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/writing-mode
    """

    xml_tag = "text"

    def __init__(self, text: str, **kwargs: Unpack[TextParams]) -> None:
        super().__init__(text=text, **kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        element = super()._plain_etree_element
        element.set("x", str(self.position.x))
        element.set("y", str(self.position.y))
        self._add_orientation_attributes(element=element)
        self.add_element_rotation(element=element)
        return element

    def add_text_span(self, text: str, **kwargs: Unpack[TextSpanParams]) -> None:
        """
        Add a TextSpan object to this Text object
        """
        TextSpan(parent=self, text=text, **kwargs)
