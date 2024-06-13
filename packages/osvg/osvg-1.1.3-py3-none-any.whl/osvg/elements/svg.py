"""
Module to define PositionalElement classes.
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import osvg.elements.group
import osvg.elements.rectanglebase
import osvg.style
import osvg.float


class ViewBox:
    """
    Representation of a viewBox value tuple
    """

    # pylint: disable=too-few-public-methods
    min_x = osvg.float.FloatProperty()
    min_y = osvg.float.FloatProperty()
    width = osvg.float.FloatProperty()
    height = osvg.float.FloatProperty()

    def __init__(
        self,
        width: int | float,
        height: int | float,
        min_x: int | float = 0,
        min_y: int | float = 0,
    ) -> None:
        self.min_x = min_x
        self.min_y = min_y
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"{self.min_x} {self.min_y} {self.width} {self.height}"


class SVG(osvg.elements.rectanglebase.RectangleBase, osvg.elements.group.Group):
    """
    This is the starting point to place elements within.
    """

    xml_tag = "svg"

    def __init__(
        self,
        width: int | float | osvg.float.Float,
        height: int | float | osvg.float.Float,
        viewbox: (
            ViewBox | tuple[int | float, int | float, int | float, int | float]
        ) = None,
        style: osvg.style.Style = None,
    ) -> None:
        super().__init__(
            width=width,
            height=height,
            style=style,
        )
        self.viewbox = None
        if viewbox is not None:
            self.set_viewbox(viewbox=viewbox)

    @property
    def etree_element(self) -> ET.Element:
        """
        Create ET element for this object
        """
        element = super().etree_element
        element.set("width", str(self.width))
        element.set("height", str(self.height))
        if self.viewbox:
            element.set("viewBox", str(self.viewbox))
        element.set("xmlns", "http://www.w3.org/2000/svg")
        return element

    @property
    def xml_string(self):
        """
        Return a pretty string with the XML code
        """
        return xml.dom.minidom.parseString(
            ET.tostring(self.etree_element)
        ).toprettyxml()

    def set_viewbox(
        self, viewbox: tuple[int | float, int | float, int | float, int | float]
    ) -> None:
        """
        Verify and set viewbox parameters.
        """
        if isinstance(viewbox, ViewBox):
            self.viewbox = viewbox
        elif not isinstance(viewbox, tuple) or len(viewbox) != 4:
            raise TypeError("viewbox must be an tuple of four values")
        else:
            self.viewbox = ViewBox(
                min_x=viewbox[0],
                min_y=viewbox[1],
                width=viewbox[2],
                height=viewbox[3],
            )
