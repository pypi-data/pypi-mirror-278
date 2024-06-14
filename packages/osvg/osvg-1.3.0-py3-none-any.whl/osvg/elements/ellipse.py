"""
Module to define class for SVG ellipse elements.
"""

import xml.etree.ElementTree as ET
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.elements.circlebase
import osvg.positions
import osvg.float
import osvg.float_math


class EllipseParams(osvg.elements.elementbase.SVGElementParams):
    """
    Keyword argument definition for Ellipse class.
    """

    radius_x: float | int | osvg.float.Const
    radius_y: float | int | osvg.float.Const


class Ellipse(osvg.elements.circlebase.CircleBase):
    """
    Base class for ellipse elements.
    """

    xml_tag = "ellipse"
    radius_x = osvg.float.FloatProperty()
    radius_y = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[EllipseParams]) -> None:
        super().__init__(**kwargs)
        self.radius_x = kwargs["radius_x"]
        self.radius_y = kwargs["radius_y"]
        self.create_default_connectors()

    @property
    def _plain_etree_element(self) -> ET.Element:
        element = super()._plain_etree_element
        element.set("cx", str(self.position.x))
        element.set("cy", str(self.position.y))
        element.set("rx", str(self.radius_x))
        element.set("ry", str(self.radius_y))
        self.add_element_rotation(element=element)
        return element

    def angled_position(self, angle: osvg.float.Float) -> osvg.positions.Position:
        return osvg.positions.Position(
            x=osvg.positions.XonEllipse(
                angle=angle, radius_x=self.radius_x, radius_y=self.radius_y
            ),
            y=osvg.positions.YonEllipse(
                angle=angle, radius_x=self.radius_x, radius_y=self.radius_y
            ),
        )
