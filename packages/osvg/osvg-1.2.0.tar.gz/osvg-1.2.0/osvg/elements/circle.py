"""
Module to define class for SVG ellipse elements.
"""

import xml.etree.ElementTree as ET
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.elements.circlebase
import osvg.elements.ellipse
import osvg.positions
import osvg.float
import osvg.float_math


class CircleParams(osvg.elements.elementbase.SVGElementParams):
    """
    Keyword argument definition for Ellipse class.
    """

    radius: float | int | osvg.float.Const


class Circle(osvg.elements.circlebase.CircleBase):
    """
    Base class for ellipse elements.
    """

    xml_tag = "circle"
    radius = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[CircleParams]) -> None:
        super().__init__(**kwargs)
        self.radius = kwargs["radius"]
        self.create_default_connectors()

    @property
    def _plain_etree_element(self) -> ET.Element:
        # pylint: disable=f-string-without-interpolation
        element = super()._plain_etree_element
        element.set("cx", str(self.position.x))
        element.set("cy", str(self.position.y))
        element.set("r", str(self.radius))
        return element

    def angled_position(self, angle: osvg.float.Float) -> osvg.positions.Position:
        return osvg.positions.Position(
            x=osvg.positions.XonCircle(
                angle=angle,
                radius=self.radius,
            ),
            y=osvg.positions.YonCircle(
                angle=angle,
                radius=self.radius,
            ),
        )
