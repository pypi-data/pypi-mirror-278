"""
Module to define Line in SVG.
"""

import xml.etree.ElementTree as ET
from collections.abc import Iterable
from typing import TypedDict
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.elements.group
import osvg.style
import osvg.elements.line_marker


class PolylineParams(TypedDict):
    """
    Keyword argument definition for Line class.
    """

    parent: osvg.elements.group.Group
    positions: Iterable[osvg.positions.Position]
    name: str = None
    style: osvg.style.Style = None
    layer: int = 0


class Polyline(osvg.elements.elementbase.SVGElement):
    """
    A Line in SVG over at least two prositions.
    """

    xml_tag = "polyline"

    def __init__(self, **kwargs: Unpack[PolylineParams]) -> None:
        super().__init__(**kwargs)
        self.positions = kwargs["positions"]
        if len(self.positions) < 2:
            raise ValueError(f"{self.__class__} needs at least two positions")
        self.start_marker = None
        self.end_marker = None

    @property
    def etree_element(self) -> ET.Element:
        # pylint: disable=f-string-without-interpolation
        element = super().etree_element
        # Adjust positions according to start/end marker lenghts
        positions = self.positions[:]
        pop_first = False
        if self.start_marker and self.start_marker.length.value > 0:
            distance = osvg.positions.Distance(a=self.start, b=self.positions[1])
            if distance.value > self.start_marker.length.value:
                positions[0] = osvg.positions.PolarShiftedPosition(
                    origin=self.start,
                    angle=osvg.positions.AngleDegree(a=self.start, b=self.positions[1]),
                    distance=self.start_marker.length,
                )
            else:
                pop_first = True
        pop_last = False
        if self.end_marker and self.end_marker.length.value > 0:
            distance = osvg.positions.Distance(a=self.positions[-2], b=self.end)
            if distance.value > self.end_marker.length.value:
                positions[-1] = osvg.positions.PolarShiftedPosition(
                    origin=self.end,
                    angle=osvg.positions.AngleDegree(a=self.end, b=self.positions[-2]),
                    distance=self.end_marker.length,
                )
            else:
                pop_last = True
        if pop_first:
            positions = positions[1:]
        if pop_last:
            positions = positions[:-1]

        # Add OSVG element infos
        element.set("points", " ".join([str(p) for p in positions]))
        if self.start_marker or self.end_marker:
            element = [element]
            if self.start_marker:
                element.append(self.start_marker.etree_element)
            if self.end_marker:
                element.append(self.end_marker.etree_element)
        return element

    @property
    def start(self) -> osvg.positions.Position:
        """
        Return first position
        """
        return self.positions[0]

    @property
    def end(self) -> osvg.positions.Position:
        """
        Return last position
        """
        return self.positions[-1]

    def add_start_marker(
        self, marker_class: osvg.elements.line_marker.Marker, **kwargs
    ) -> None:
        """
        Add a start marker to the line
        """
        angle = osvg.positions.AngleDegree(a=self.positions[1], b=self.start)
        self.start_marker = marker_class(
            parent=self, position=self.start, angle=angle, **kwargs
        )

    def add_end_marker(
        self, marker_class: osvg.elements.line_marker.Marker, **kwargs
    ) -> None:
        """
        Add a end marker to the line
        """
        angle = osvg.positions.AngleDegree(a=self.positions[-2], b=self.end)
        self.end_marker = marker_class(
            parent=self, position=self.end, angle=angle, **kwargs
        )
