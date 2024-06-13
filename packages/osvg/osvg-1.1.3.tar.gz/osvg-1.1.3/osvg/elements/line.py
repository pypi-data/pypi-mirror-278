"""
Module to define Line in SVG.
"""

from typing import TypedDict
from typing_extensions import Unpack
import osvg.elements.polyline
import osvg.elements.group
import osvg.style
import osvg.elements.line_marker


class LineParams(TypedDict):
    """
    Keyword argument definition for Line class.
    """

    parent: osvg.elements.group.Group
    start: osvg.positions.Position
    end: osvg.positions.Position
    name: str = None
    style: osvg.style.Style = None
    layer: int = 0


class Line(osvg.elements.polyline.Polyline):
    """
    A Line in SVG from position "start" to position "end".
    """

    xml_tag = "polyline"

    def __init__(self, **kwargs: Unpack[LineParams]) -> None:
        start = kwargs.pop("start")
        end = kwargs.pop("end")
        kwargs["positions"] = [start, end]
        super().__init__(**kwargs)

    def add_start_marker(
        self, marker_class: osvg.elements.line_marker.Marker, **kwargs
    ) -> None:
        """
        Add a start marker to the line
        """
        angle = osvg.positions.AngleDegree(a=self.end, b=self.start)
        self.start_marker = marker_class(
            parent=self, position=self.start, angle=angle, **kwargs
        )

    def add_end_marker(
        self, marker_class: osvg.elements.line_marker.Marker, **kwargs
    ) -> None:
        """
        Add a end marker to the line
        """
        angle = osvg.positions.AngleDegree(a=self.start, b=self.end)
        self.end_marker = marker_class(
            parent=self, position=self.end, angle=angle, **kwargs
        )
