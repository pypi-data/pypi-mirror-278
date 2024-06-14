"""
Module to define base Element classes.
"""

import xml.etree.ElementTree as ET
from typing import TypedDict
from typing_extensions import Unpack
import osvg.float
import osvg.float_math
import osvg.helper
import osvg.positions
import osvg.style


SVG_STROKE_WIDTH_DEFAULT = 1


class SVGElementParams(TypedDict):
    """
    Keyword argument definition for SVGElement class.
    """

    name: str = None
    parent: "SVGElement" = None
    position: osvg.positions.Position = None
    style: osvg.style.Style = None
    layer: int = 0
    rotation: "float | osvg.float.Const" = 0
    hyperlink: str = None


class SVGElement:
    """
    Parent class for Element and Group/SVG classes.
    """

    # pylint: disable=too-many-instance-attributes

    xml_tag = ""
    layer = 0
    position = osvg.positions.PositionProperty()
    element_rotation = osvg.float.FloatProperty()
    parent_rotation = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[SVGElementParams]) -> None:
        self.name = kwargs.get("name", None)
        self.parent_obj = None
        self.childs = []
        parent = kwargs.get("parent", None)
        self.parent = parent
        self.element_rotation = kwargs.get("rotation", 0)
        self.rotation = osvg.float_math.Sum(self.element_rotation, self.parent_rotation)
        position = kwargs.get("position", None)
        if position is None and parent is not None:
            self.position = parent.position
        else:
            self.position = position
        self.style_obj = None
        self.style = kwargs.get("style", None)
        self.layer = kwargs.get("layer", 0)
        self.connectors = {}
        self.hyperlink = kwargs.get("hyperlink", None)

    @property
    def parent(self):
        """
        Get parent object
        """
        return self.parent_obj

    @parent.setter
    def parent(self, parent: "SVGElement"):
        """
        Set and validate parent
        """
        # Check parent type
        if parent is not None and not issubclass(type(parent), SVGElement):
            raise TypeError("Parent type not allowed")
        # Check ancestor loop
        if parent is not None and (self == parent or self in parent.ancestors):
            raise RuntimeError("Parent loop detected")
        # Derefer/Refer parent
        if self.parent_obj:
            self.parent_obj.remove_child(self)
        if parent is None:
            self.parent_rotation = 0
        else:
            parent.add_child(self)
            self.parent_obj = parent
            self.parent_rotation = parent.rotation

    @property
    def ancestors(self) -> list["SVGElement"]:
        """
        Get all ancestors recursively
        """
        if self.parent_obj is None:
            return []
        return self.parent_obj.ancestors + [self.parent_obj]

    @staticmethod
    def verify_other(other: "SVGElement", class_check: bool = True):
        """
        Verify if other's class is a subclass to IOR
        """
        if class_check and not issubclass(type(other), SVGElement):
            raise TypeError("Other's class is not a subclass to ElementBase")

    def add_child(self, other: "SVGElement") -> None:
        """
        Add other IOR object as a child
        """
        self.verify_other(other)
        self.childs.append(other)

    def remove_child(self, other: "SVGElement") -> None:
        """
        Remove other IOR object from childs
        """
        self.childs.remove(other)

    @property
    def descendants(self) -> dict:
        """
        Return a dictionary with all childs recursively
        if child has a name
        """
        descendants = {}
        for o in self.childs:
            if o.name is not None:
                descendants[o.name] = o
            descendants.update(o.descendants)
        return descendants

    @property
    def style(self) -> osvg.style.Style:
        """
        Get style of this element.
        """
        return self.style_obj

    @style.setter
    def style(self, style: osvg.style.Style):
        """
        Set style for this element.
        """
        if style is None:
            style = osvg.style.Style()
        elif not isinstance(style, osvg.style.Style):
            raise TypeError("Style must be a style object")
        self.style_obj = style

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this object without wrappers
        """
        # Create the ET Element
        element = ET.Element(self.xml_tag)
        if self.name is not None:
            element.set("id", self.name)
        if self.parent:
            style_str = str(self.parent.style.diff(self.style))
        else:
            style_str = str(self.style)
        if style_str:
            element.set("style", style_str)
        # Get the child ET Element list
        sub_elements = osvg.helper.WeightedList()
        for obj in self.childs:
            sub_ets = obj.etree_element
            if isinstance(sub_ets, list):
                for et in sub_ets:
                    sub_elements.append(et, obj.layer)
            else:
                sub_elements.append(sub_ets, obj.layer)
        for e in sub_elements:
            element.append(e)
        return element

    @property
    def etree_element(self) -> ET.Element:
        """
        Create ET element for this object
        """
        # If element has a hyperlink, this needs to be wrapped.
        if self.hyperlink is not None:
            element = ET.Element("a")
            element.set("href", self.hyperlink)
            element.append(self._plain_etree_element)
            return element
        return self._plain_etree_element

    def add_connector(
        self, position, name: str, respect_rotation=False
    ) -> osvg.positions.Position:
        """
        Add a position to the connector dictionary.
        Self must be within position's reference path.
        Return the added connector position
        """
        if name in self.connectors:
            raise ValueError(f"Connector with name {name} already exists")
        if not issubclass(type(position), osvg.positions.Position):
            raise TypeError("position must be a Position object")
        if respect_rotation:
            position = osvg.positions.RotatedPosition(
                origin=position,
                center=self.position,
                angle=self.rotation,
            )
        self.connectors[name] = position
        return position

    def add_hyperlink(self, hyperlink: str) -> None:
        """
        Add an hyperlink to this element
        """
        self.hyperlink = hyperlink

    @property
    def stroke_width(self) -> float:
        """
        Get stroke width style attribute of Element or upstream value
        """
        if self.style.stroke_width is not None:
            return self.style.stroke_width
        if not self.parent:
            return SVG_STROKE_WIDTH_DEFAULT
        return self.parent.stroke_width

    def _inherited_style(self, style: osvg.style.Style):
        """
        Adjust given style object with inherited style attributes
        """
        if self.parent:
            style = self.parent._inherited_style(style=style)
        style.merge(self.style)
        return style

    @property
    def inherited_style(self) -> osvg.style.Style:
        """
        Return style object with inherited merged with element's style attributes
        """
        return self._inherited_style(style=osvg.style.Style())

    def add_element_rotation(self, element: ET.ElementTree) -> None:
        """
        Add transform tag with rotation if required
        """
        if self.rotation.value != 0:
            element.set(
                "transform",
                f"rotate({str(self.rotation)} {str(self.position.x)} {str(self.position.y)})",
            )


class Height(osvg.float_math.Prod):
    """
    Relative value to the heigth of an element.
    """

    def __init__(
        self,
        element: SVGElement,
        factor: osvg.float.Float | float | int = 1,
    ) -> None:
        if not hasattr(element, "height_reference"):
            raise TypeError(
                "Can only reference to an element with a height_reference attribute"
            )
        super().__init__(element.height_reference, factor)


class Width(osvg.float_math.Prod):
    """
    Relative value to the width of an area.
    """

    def __init__(
        self,
        element: SVGElement,
        factor: float | int | osvg.float.Float = 1,
    ) -> None:
        if not hasattr(element, "width_reference"):
            raise TypeError(
                "Can only reference to an element with a width_reference attribute"
            )
        super().__init__(element.width_reference, factor)
