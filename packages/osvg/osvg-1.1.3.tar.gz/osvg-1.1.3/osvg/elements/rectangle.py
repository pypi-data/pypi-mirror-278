"""
Module to define a Rectangle in SVG.
"""

import xml.etree.ElementTree as ET
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.elements.rectanglebase
import osvg.style


class RectangleParams(osvg.elements.rectanglebase.RectangleBaseParams):
    """
    Keyword argument definition for RectangleBase class.
    """

    rx: float | int | osvg.float.Const = None
    ry: float | int | osvg.float.Const = None


class Rectangle(osvg.elements.rectanglebase.RectangleBase):
    """
    A rectangle in SVG - See: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/rect
    """

    xml_tag = "rect"
    rx = osvg.float.FloatProperty()
    ry = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[RectangleParams]) -> None:
        self.rx = kwargs.get("rx", None)
        self.ry = kwargs.get("ry", None)
        super().__init__(**kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        # pylint: disable=f-string-without-interpolation
        element = super()._plain_etree_element
        element.set(
            "x", f"{round(self.position.x.value - (self.width.value / 2), 3):g}"
        )
        element.set(
            "y", f"{round(self.position.y.value - (self.height.value / 2), 3):g}"
        )
        element.set("width", str(self.width))
        element.set("height", str(self.height))
        if self.rx.value is not None:
            element.set("rx", str(self.rx))
        if self.ry.value is not None:
            element.set("ry", str(self.ry))
        self.add_element_rotation(element=element)
        return element


class SCRectangleParams(osvg.elements.rectanglebase.RectangleBaseParams):
    """
    Keyword argument definition for RectangleBase class.
    """

    percentage: float | int | osvg.float.Const = 5


class SCRectangle(Rectangle):
    """
    A Smooth Cornered Rectangle

    Parameter:
      percentage: Percent of the lower value of width or height.
    """

    percentage = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[SCRectangleParams]) -> None:
        super().__init__(**kwargs)
        self.percentage = kwargs.get("percentage", 5)
        self.rx = osvg.float_math.PercentOf(
            osvg.float_math.Min(self.width, self.height), self.percentage
        )
