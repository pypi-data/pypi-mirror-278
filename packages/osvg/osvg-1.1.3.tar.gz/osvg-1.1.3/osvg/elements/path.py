"""
Module to define class for SVG ellipse elements.
"""

# pylint: disable=too-few-public-methods

from xml.etree import ElementTree as ET
from typing import TypedDict
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg.positions
import osvg.float
import osvg.float_math


class _PathElement:
    """
    Base class for all Path elements
    """

    tag = ""
    needs_previous_path_element = False
    previous_path_element_sub_classes = []

    def verify_previous_path_element(self, element: "_PathElement") -> None:
        """
        Checks if given (previous) path element if the one which is needed
        """
        if not issubclass(type(element), tuple(self.previous_path_element_sub_classes)):
            class_names = " or ".join(
                [x.__name__ for x in self.previous_path_element_sub_classes]
            )
            raise RuntimeError(
                f"{self.__class__.__name__} need sub-class of "
                + f"{class_names} as previous path element"
            )


class _SingleFloatElement(_PathElement):
    """
    Base class for Path elements which uses a position
    """

    ref = osvg.float.FloatProperty()

    def __init__(self, ref: int | float | osvg.float.Float) -> None:
        self.ref = ref

    def __str__(self) -> str:
        return f"{self.tag} {str(self.ref)}"


class _AbsolutePositionElement(_PathElement):
    """
    Base class for Path elements which uses a position object
    """

    def __init__(self, position: osvg.positions.Position) -> None:
        self.position = position

    def __str__(self) -> str:
        return f"{self.tag} {str(self.position)}"


class _TwoAbsolutePositionElement(_AbsolutePositionElement):
    """
    Base class for Path elements which uses two position objects
    """

    def __init__(
        self, position1: osvg.positions.Position, position2: osvg.positions.Position
    ) -> None:
        super().__init__(position=position1)
        self.position2 = position2

    def __str__(self) -> str:
        return f"{super().__str__()} {str(self.position2)}"


class _ThreeAbsolutePositionElement(_TwoAbsolutePositionElement):
    """
    Base class for Path elements which uses three position objects
    """

    def __init__(
        self,
        position1: osvg.positions.Position,
        position2: osvg.positions.Position,
        position3: osvg.positions.Position,
    ) -> None:
        super().__init__(position1=position1, position2=position2)
        self.position3 = position3

    def __str__(self) -> str:
        return f"{super().__str__()} {str(self.position3)}"


class _RelativePositionElement(_PathElement):
    """
    Base class for Path elements which uses a position shifted by
    float values x1 and y1.
    """

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()

    def __init__(
        self, x: int | float | osvg.float.Float, y: int | float | osvg.float.Float
    ) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.tag} {str(self.x)},{str(self.y)}"


class _TwoRelativePositionElement(_RelativePositionElement):
    """
    Base class for Path elements which uses two positions shifted by
    float values x1, y1, x2, and y2.
    """

    x2 = osvg.float.FloatProperty()
    y2 = osvg.float.FloatProperty()

    def __init__(
        self,
        x1: int | float | osvg.float.Float,
        y1: int | float | osvg.float.Float,
        x2: int | float | osvg.float.Float,
        y2: int | float | osvg.float.Float,
    ) -> None:
        super().__init__(x=x1, y=y1)
        self.x2 = x2
        self.y2 = y2

    def __str__(self) -> str:
        return f"{super().__str__()} {str(self.x2)},{str(self.y2)}"


class _ThreeRelativePositionElement(_TwoRelativePositionElement):
    """
    Base class for Path elements which uses three positions shifted by
    float values x1, y1, x2, y2, x3 and y3.
    """

    x3 = osvg.float.FloatProperty()
    y3 = osvg.float.FloatProperty()

    def __init__(
        self,
        x1: int | float | osvg.float.Float,
        y1: int | float | osvg.float.Float,
        x2: int | float | osvg.float.Float,
        y2: int | float | osvg.float.Float,
        x3: int | float | osvg.float.Float,
        y3: int | float | osvg.float.Float,
    ) -> None:
        # pylint: disable=too-many-arguments
        super().__init__(x1=x1, y1=y1, x2=x2, y2=y2)
        self.x3 = x3
        self.y3 = y3

    def __str__(self) -> str:
        return f"{super().__str__()} {str(self.x3)},{str(self.y3)}"


class PathM(_AbsolutePositionElement):
    """
    Class for a Path element which moves the path to a position object
    """

    tag = "M"


class Pathm(_RelativePositionElement):
    """
    Class for a Path element which moves the path to
    a position shifted by x and y float values
    """

    tag = "m"


class PathL(_AbsolutePositionElement):
    """
    Class for a Path element which draws a line to a position object
    """

    tag = "L"


class Pathl(_RelativePositionElement):
    """
    Class for a Path element which draws a line to
    aa position shifted by x and y float values
    """

    tag = "l"


class PathH(_SingleFloatElement):
    """
    Class for a Path element which draws a horizontal line to
    a position (x, current_y)
    """

    tag = "H"

    def __init__(self, x: int | float | osvg.float.Float) -> None:
        super().__init__(ref=x)


class Pathh(_SingleFloatElement):
    """
    Class for a Path element which draws a horizontal line to
    a position shifted by x float value
    """

    tag = "h"

    def __init__(self, x: int | float | osvg.float.Float) -> None:
        super().__init__(ref=x)


class PathV(_SingleFloatElement):
    """
    Class for a Path element which draws a vertical line to
    a position (current_x, y)
    """

    tag = "V"

    def __init__(self, y: int | float | osvg.float.Float) -> None:
        super().__init__(ref=y)


class Pathv(_SingleFloatElement):
    """
    Class for a Path element which draws a horizontal line to
    a position shifted by y float value
    """

    tag = "v"

    def __init__(self, y: int | float | osvg.float.Float) -> None:
        super().__init__(ref=y)


class PathZ(_PathElement):
    """
    Class for the final 'Z' element which closes the path to
    the starting position
    """

    def __str__(self):
        return "Z"


class CubicBezierCurveElement:
    """
    Meta class to to verify previous path element
    """


class PathC(_ThreeAbsolutePositionElement, CubicBezierCurveElement):
    """
    Class to draw a cubic Bézier curve by using three position objects:
    - postion1: Bézier Point 1
    - postion2: Bézier Point 2
    - postion3: Final Point
    """

    tag = "C"


class Pathc(_ThreeRelativePositionElement, CubicBezierCurveElement):
    """
    Class to draw a cubic Bézier curve by using three relative positions:
    - x1: x Float value of Bézier Point 1
    - y1: y Float value of Bézier Point 1
    - x2: x Float value of Bézier Point 2
    - y2: y Float value of Bézier Point 2
    - x3: x Float value of Final Point
    - y3: y Float value of Final Point
    """

    tag = "c"


class PathS(_TwoAbsolutePositionElement, CubicBezierCurveElement):
    """
    Class to draw a follow-up cubic Bézier curve by using two position objects:
    - postion1: Bézier Point 2
    - postion2: Final Point
    Note: Bézier Point 1 is a reflection of Bézier Point 2 of previous
    cubic Bézier Curve.
    """

    tag = "S"
    needs_previous_path_element = True
    previous_path_element_sub_classes = [CubicBezierCurveElement]


class Paths(_TwoRelativePositionElement, CubicBezierCurveElement):
    """
    Class to draw a follow-up cubic Bézier curve by using two relative positions:
    - x1: x Float value of Bézier Point 2
    - y1: y Float value of Bézier Point 2
    - x2: x Float value of Final Point
    - y2: y Float value of Final Point
    Note: Bézier Point 1 is a reflection of Bézier Point 2 of previous
    cubic Bézier Curve.
    """

    tag = "s"
    needs_previous_path_element = True
    previous_path_element_sub_classes = [CubicBezierCurveElement]


class QuadraticBezierCurveElement:
    """
    Meta class to to verify previous path element
    """


class PathQ(_TwoAbsolutePositionElement, QuadraticBezierCurveElement):
    """
    Class to draw a quadratic Bézier curve by using two position objects:
    - postion1: Bézier Point
    - postion2: Final Point
    """

    tag = "Q"


class Pathq(_TwoRelativePositionElement, QuadraticBezierCurveElement):
    """
    Class to draw a quadratic Bézier curve by using two relative positions:
    - x1: x Float value of Bézier Point
    - y1: y Float value of Bézier Point
    - x2: x Float value of Final Point
    - y2: y Float value of Final Point
    """

    tag = "q"


class PathT(_AbsolutePositionElement, QuadraticBezierCurveElement):
    """
    Class to draw a follow-up quadratic Bézier curve by using a position object:
    - postion: Final Point
    Note: Bézier Point is a reflection of Bezier Point of previous
    quadratic Bézier Curve.
    """

    tag = "T"
    needs_previous_path_element = True
    previous_path_element_sub_classes = [QuadraticBezierCurveElement]


class Patht(_RelativePositionElement, QuadraticBezierCurveElement):
    """
    Class to draw a follow-up quadratic Bézier curve by using a relative position:
    - x: x Float value of Final Point
    - y: y Float value of Final Point
    Note: Bézier Point is a reflection of Bezier Point of previous
    quadratic Bézier Curve.
    """

    tag = "t"
    needs_previous_path_element = True
    previous_path_element_sub_classes = [QuadraticBezierCurveElement]


class PathAParams(TypedDict):
    """
    Optional parameter definition for class PathA
    """

    angle: int | float | osvg.float.Float = (0,)
    long_bow: bool = (True,)
    right_bend: bool = (True,)


class PathA(_PathElement):
    """
    Class to draw a elliptic arc bow:
    - position: Final position of the arc curve
    - width: Width of the ellipse
    - height: Height of the ellipse
    - angle: Angled orientation of the ellipse
    - long_bow: Indicator if long bow should be drawn
    - right_bend:  Inficator if bow is right or left bend
    """

    width = osvg.float.FloatProperty()
    height = osvg.float.FloatProperty()
    angle = osvg.float.FloatProperty()

    def __init__(
        self,
        position: osvg.positions.Position,
        width: int | float | osvg.float.Float,
        height: int | float | osvg.float.Float,
        **kwargs: Unpack[PathAParams],
    ) -> None:
        self.position = position
        self.width = width
        self.height = height
        self.angle = kwargs.get("angle", 0)
        self.long_bow = kwargs.get("long_bow", True)
        self.right_bend = kwargs.get("right_bend", True)

    def __str__(self) -> str:
        return (
            f"A {self.width},{str(self.height)} "
            + f"{str(self.angle)},{int(self.long_bow)},{int(self.right_bend)} {str(self.position)}"
        )


class Path(osvg.elements.elementbase.SVGElement):
    """
    Class representing a SVG path element
    """

    xml_tag = "path"

    def __init__(
        self, **kwargs: Unpack[osvg.elements.elementbase.SVGElementParams]
    ) -> None:
        super().__init__(**kwargs)
        self.path_elements = [PathM(position=self.position)]

    def add_path_element(self, element: _PathElement) -> None:
        """
        Add a path element to the SVG path element
        """
        if element.needs_previous_path_element:
            element.verify_previous_path_element(self.path_elements[-1])
        self.path_elements.append(element)

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this object without wrappers
        """
        # Create the ET Element
        element = super()._plain_etree_element
        element.set("d", " ".join([str(x) for x in self.path_elements]))
        return element
