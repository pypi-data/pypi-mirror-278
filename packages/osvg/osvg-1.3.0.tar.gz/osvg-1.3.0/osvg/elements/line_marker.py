"""
Module to define line start and end markers.
"""

from xml.etree import ElementTree as ET
from typing import TypedDict
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.style


class MarkerParams(TypedDict):
    """
    Keyword argument definition for CircleMarker class.
    """

    color: str = None


class Marker:
    """
    Base class for start and end markers
    """

    # pylint: disable=too-few-public-methods

    stroke_width_factor = 3

    def __init__(
        self,
        parent: "osvg.line.Line | osvg.polyline.Polyline",
        position: osvg.positions.Position,
        angle: int | float | osvg.float.Float,
        **kwargs,
    ) -> None:
        self.parent = parent
        self.position = position
        self.angle = angle
        color = kwargs.get("color", None)
        osvg.style.verify_color_value(color)
        self.color = color

    @property
    def length(self) -> osvg.float.Float:
        """
        Return length of marker. (To appropriately shorten line)
        """
        return osvg.float.Const(0)

    def _add_style(self, element: ET.Element) -> None:
        """
        Add style attributes
        """
        element.set("stroke-width", "0")
        self._add_color_style(element=element)

    def _add_color_style(self, element: ET.Element) -> None:
        """
        Add color style attribute
        """
        if self.color is not None:
            color = self.color
        else:
            color = self.parent.inherited_style.attributes["stroke_color"].value
        if color:
            element.set("fill", f"#{color}")

    @property
    def etree_element(self) -> ET.Element:
        """
        Get SVG element to draw marker
        """
        raise NotImplementedError()


class CircleMarkerParams(MarkerParams):
    """
    Keyword argument definition for CircleMarker class.
    """

    radius: int | float | osvg.float.Float = None


class CircleMarker(Marker):
    """
    Class to define a circle at the start/end of a line
    """

    def __init__(
        self,
        parent: "osvg.line.Line | osvg.polyline.Polyline",
        position: osvg.positions.Position,
        angle: int | float | osvg.float.Float,
        **kwargs: Unpack[CircleMarkerParams],
    ):
        super().__init__(parent=parent, position=position, angle=angle, **kwargs)
        self._radius = osvg.float.RefFloat()
        self.radius = kwargs.get("radius", None)

    @property
    def radius(self) -> osvg.float.RefFloat:
        """
        Get radius
        """
        return self._radius

    @radius.setter
    def radius(self, radius: int | float | osvg.float.Float | type[None]) -> None:
        if radius is None:
            parent_stroke_with = self.parent.style.attributes["stroke_width"]
            self._radius = osvg.float_math.Prod(
                (
                    parent_stroke_with.value
                    if parent_stroke_with.value.value is not None
                    else osvg.elements.elementbase.SVG_STROKE_WIDTH_DEFAULT
                ),
                self.stroke_width_factor * 2 / 3,
            )
        else:
            if not issubclass(type(radius), osvg.float.Float):
                radius = osvg.float.Const(radius)
            self._radius = radius

    @property
    def etree_element(self) -> ET.Element:
        element = ET.Element("circle")
        element.set("cx", str(self.position.x))
        element.set("cy", str(self.position.y))
        element.set("r", str(self.radius))
        element.set("stroke-width", "0")
        self._add_style(element=element)
        return element


class ArrowMarkerParams(MarkerParams):
    """
    Keyword argument definition for ArrowMarker class.
    """

    length: int | float | osvg.float.Float = None
    width: int | float | osvg.float.Float = None


class ArrowMarker(Marker):
    """
    Class for regular Arrow Markers
    """

    angle = osvg.float.FloatProperty()

    def __init__(
        self,
        parent: "osvg.line.Line | osvg.polyline.Polyline",
        position: osvg.positions.Position,
        angle: int | float | osvg.float.Float,
        **kwargs: Unpack[ArrowMarkerParams],
    ):
        super().__init__(parent=parent, position=position, angle=angle, **kwargs)
        self._arrow_length = None
        self.arrow_length = kwargs.get("length", None)
        self._arrow_width = None
        self.arrow_width = kwargs.get("width", None)

    @property
    def length(self) -> osvg.float.RefFloat:
        """
        Get length
        """
        return self.arrow_length

    @property
    def arrow_length(self) -> osvg.float.RefFloat:
        """
        Get length
        """
        return self._arrow_length

    @arrow_length.setter
    def arrow_length(self, length: int | float | osvg.float.Float | type[None]) -> None:
        if length is None:
            parent_stroke_with = self.parent.style.attributes["stroke_width"]
            stroke_width = (
                osvg.elements.elementbase.SVG_STROKE_WIDTH_DEFAULT
                if parent_stroke_with.value.value is None
                else parent_stroke_with.value.value
            )
            self._arrow_length = osvg.float_math.Prod(
                stroke_width, self.stroke_width_factor * 2
            )
        else:
            if not issubclass(type(length), osvg.float.Float):
                length = osvg.float.Const(length)
            self._arrow_length = length

    @property
    def arrow_width(self) -> osvg.float.RefFloat:
        """
        Get width
        """
        return self._arrow_width

    @arrow_width.setter
    def arrow_width(self, width: int | float | osvg.float.Float | type[None]) -> None:
        if width is None:
            self._arrow_width = self.arrow_length
        else:
            if not issubclass(type(width), osvg.float.Float):
                width = osvg.float.Const(width)
            self._arrow_width = width

    @property
    def etree_element(self) -> ET.Element:
        element = ET.Element("polygon")
        root = osvg.positions.PolarShiftedPosition(
            origin=self.position,
            angle=osvg.float_math.Sum(self.angle, 180),
            distance=self.arrow_length,
        )
        upper = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 270),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        lower = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 90),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        element.set("points", " ".join([str(upper), str(self.position), str(lower)]))
        self._add_style(element=element)
        return element


class LightArrowMarkerParams(ArrowMarkerParams):
    """
    Keyword argument definition for LightArrowMarker class.
    """

    inner_length: int | float | osvg.float.Float = None


class LightArrowMarker(ArrowMarker):
    """
    Class for Arrow Markers, which are more light/sharp
    """

    def __init__(
        self,
        parent: "osvg.line.Line | osvg.polyline.Polyline",
        position: osvg.positions.Position,
        angle: int | float | osvg.float.Float,
        **kwargs: Unpack[LightArrowMarkerParams],
    ):
        super().__init__(parent=parent, position=position, angle=angle, **kwargs)
        self._inner_length = None
        self.inner_length = kwargs.get("inner_length", None)

    @property
    def length(self) -> osvg.float.RefFloat:
        """
        Get length
        """
        return self.inner_length

    @property
    def inner_length(self) -> osvg.float.RefFloat:
        """
        Get length
        """
        return self._inner_length

    @inner_length.setter
    def inner_length(
        self, inner_length: int | float | osvg.float.Float | type[None]
    ) -> None:
        if inner_length is None:
            self._inner_length = osvg.float_math.Prod(self.arrow_length, 0.5)
        else:
            if not issubclass(type(inner_length), osvg.float.Float):
                inner_length = osvg.float.Const(inner_length)
            self._inner_length = inner_length

    @property
    def etree_element(self) -> ET.Element:
        element = ET.Element("polygon")
        root = osvg.positions.PolarShiftedPosition(
            origin=self.position,
            angle=osvg.float_math.Sum(self.angle, 180),
            distance=self.arrow_length,
        )
        draw_root = osvg.positions.PolarShiftedPosition(
            origin=self.position,
            angle=osvg.float_math.Sum(self.angle, 180),
            distance=self.inner_length,
        )
        upper = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 270),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        lower = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 90),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        element.set(
            "points",
            " ".join([str(draw_root), str(upper), str(self.position), str(lower)]),
        )
        self._add_style(element=element)
        return element


class SkinnyArrowMarker(ArrowMarker):
    """
    Class for Arrow Markers, which are only two lines.
    """

    @property
    def length(self) -> osvg.float.RefFloat:
        """
        Get length
        """
        return osvg.float.Const(0)

    @property
    def etree_element(self) -> ET.Element:
        element = ET.Element("polyline")
        root = osvg.positions.PolarShiftedPosition(
            origin=self.position,
            angle=osvg.float_math.Sum(self.angle, 180),
            distance=self.arrow_length,
        )
        upper = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 270),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        lower = osvg.positions.PolarShiftedPosition(
            origin=root,
            angle=osvg.float_math.Sum(self.angle, 90),
            distance=osvg.float_math.Prod(self.arrow_width, 0.5),
        )
        element.set("points", " ".join([str(upper), str(self.position), str(lower)]))
        self._add_color_style(element=element)
        return element
