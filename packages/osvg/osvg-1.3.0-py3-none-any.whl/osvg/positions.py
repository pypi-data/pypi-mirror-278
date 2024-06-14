"""
Module to define position objects.
"""

# pylint: disable=missing-function-docstring

import math
from collections.abc import Iterable
import osvg.float
import osvg.float_math
import osvg.helper


class Position:
    """
    Class to define a point within in the two-dimensional drawing.
    'x' is the floating point value on the x axis with
    x=0 as the most left point and x>0 is moving to the right.
    'y' is the floating point value on the y axis with
    y=0 as the most upper point and y>0 is moving down.

    A PositionObject is a linkable object.
    """

    # pylint: disable=too-few-public-methods

    str_round = 3
    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()

    def __init__(
        self,
        x: osvg.float.Float | float = 0.0,
        y: osvg.float.Float | float = 0.0,
    ) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        """
        Get the SVG string
        """
        return f"{self.x},{self.y}"


class PositionProperty:
    """
    Property descriptor for Position objects
    """

    def __init__(self):
        self.instances = {}

    def __get__(self, instance, owner):
        return self.instances[instance]

    def __set__(
        self, instance, p: Position | Iterable[int | float | osvg.float.Float] = None
    ):
        if p is None:
            x = 0
            y = 0
        elif issubclass(type(p), Position):
            x = p.x
            y = p.y
        elif isinstance(p, Iterable):
            x = p[0]
            y = p[1]
        else:
            raise TypeError("Position object required")
        if instance not in self.instances:
            self.instances[instance] = Position()
        self.instances[instance].x = x
        self.instances[instance].y = y


class ShiftedPosition(Position):
    # pylint: disable=too-few-public-methods
    """
    A relative position object where the coordinates are shifted
    to the reference by values.
    """
    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    origin = PositionProperty()
    x_shift = osvg.float.FloatProperty()
    y_shift = osvg.float.FloatProperty()

    def __init__(
        self,
        origin: Position,
        x_shift: osvg.float.Float | float = 0,
        y_shift: osvg.float.Float | float = 0,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.x = osvg.float_math.Sum(self.origin.x, self.x_shift)
        self.y = osvg.float_math.Sum(self.origin.y, self.y_shift)


class Distance(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    distance between two Positions
    """

    def __init__(self, a: Position, b: Position) -> None:
        super().__init__(ax=a.x, ay=a.y, bx=b.x, by=b.y)

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        self._value = math.dist(
            [self.ax.value, -self.ay.value],
            [self.bx.value, -self.by.value],
        )


class AngleDegree(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    angle from "a" to another position "b" in radians
    """

    def __init__(self, a: Position, b: Position) -> None:
        super().__init__(ax=a.x, ay=a.y, bx=b.x, by=b.y)

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        dx = self.bx.value - self.ax.value
        dy = self.ay.value - self.by.value  # due to the inverted y-axis
        self._value = osvg.helper.degrees(math.atan2(dy, dx))


class XonCircle(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    x value of a position on a circle.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(self, angle: osvg.float.Float, radius: osvg.float.Float) -> None:
        super().__init__(angle=angle, radius=radius)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value = (
            math.cos(osvg.helper.radians(self.angle.value)) * self.radius.value
        )


class YonCircle(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated osvg.float.Float object representing the
    y value of a position on a circle.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, angle: osvg.float.Float, radius: osvg.float.Float) -> None:
        super().__init__(angle=angle, radius=radius)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value = (
            math.sin(osvg.helper.radians(self.angle.value)) * -1 * self.radius.value
        )


class XonEllipse(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    x value of a position on a ellipse.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(
        self,
        angle: osvg.float.Float,
        radius_x: osvg.float.Float,
        radius_y: osvg.float.Float,
    ) -> None:
        super().__init__(angle=angle, radius_x=radius_x, radius_y=radius_y)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        self._value = abs(
            self.radius_x.value
            * self.radius_y.value
            / math.sqrt(
                self.radius_y.value**2
                + self.radius_x.value**2
                * math.tan(osvg.helper.radians(self.angle.value)) ** 2
            )
        )
        if 90 < self.angle.value % 360 < 270:
            self._value = -1 * self._value


class YonEllipse(osvg.float_math.CalculatedKwargs):
    """
    Class to provide a calculated Float object representing the
    y value of a position on a ellipse.
    Note: angle=0 is twelve o'clock and it goes clockwise.
    """

    def __init__(
        self,
        angle: osvg.float.Float,
        radius_x: osvg.float.Float,
        radius_y: osvg.float.Float,
    ) -> None:
        super().__init__(angle=angle, radius_x=radius_x, radius_y=radius_y)

    def fill_cache(self) -> float:
        # pylint: disable=no-member
        tan = math.tan(osvg.helper.radians(self.angle.value))
        if tan == 0:
            self._value = 0
        else:
            self._value = abs(
                self.radius_x.value
                * self.radius_y.value
                / math.sqrt(
                    self.radius_x.value**2
                    + self.radius_y.value**2
                    / math.tan(osvg.helper.radians(self.angle.value)) ** 2
                )
            )
            if self.angle.value % 360 > 180:
                self._value = -1 * self._value


class RotatedPosition(Position):
    """
    Class to define a point rotated around another point by an angle.
    'reference' is the Position which should be shifted.
    'center' is the center of the circle with 'parent' on the cirle track.

    Note:
    - angle goes clockwise
    - angle is delta to current angle 'reference' -> 'parent'
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    origin = PositionProperty()
    center = PositionProperty()
    angle = osvg.float.FloatProperty()

    def __init__(
        self,
        origin: Position,
        center: Position,
        angle: osvg.float.Float | float = 0,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.center = center
        self.angle = angle

        distance = Distance(self.center, self.origin)
        origin_angle = AngleDegree(self.center, self.origin)
        new_angle = osvg.float_math.Sum(self.angle, origin_angle)

        # Calc x
        origin_shift_x = XonCircle(angle=origin_angle, radius=distance)
        new_shift_x = XonCircle(angle=new_angle, radius=distance)
        self.x = osvg.float_math.Sum(
            self.origin.x, osvg.float_math.InvertedSign(origin_shift_x), new_shift_x
        )

        # Calc y
        origin_shift_y = YonCircle(angle=origin_angle, radius=distance)
        new_shift_y = YonCircle(angle=new_angle, radius=distance)
        self.y = osvg.float_math.Sum(
            self.origin.y, osvg.float_math.InvertedSign(origin_shift_y), new_shift_y
        )


class PolarShiftedPosition(Position):
    """
    Class to define a position which is described by a polar coordinate
    with the reference position as center.
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    origin = PositionProperty()
    angle = osvg.float.FloatProperty()
    distance = osvg.float.FloatProperty()
    x_shift = osvg.float.FloatProperty()
    y_shift = osvg.float.FloatProperty()

    def __init__(
        self,
        origin: Position,
        angle: osvg.float.Float | float = 0,
        distance: osvg.float.Float | float = 0,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.angle = angle
        self.distance = distance

        x_shift = osvg.float_math.Prod(
            osvg.float_math.Cos(self.angle),
            self.distance,
        )
        self.x = osvg.float_math.Sum(origin.x, x_shift)
        y_shift = osvg.float_math.Prod(
            osvg.float_math.InvertedSign(osvg.float_math.Sin(self.angle)),
            self.distance,
        )
        self.y = osvg.float_math.Sum(origin.y, y_shift)


class RayCrossCirclePosition(Position):
    """
    Class to define a point at which a ray from
    circle center to a position crosses the circle.
    """

    # pylint: disable=too-few-public-methods

    x = osvg.float.FloatProperty()
    y = osvg.float.FloatProperty()
    center = PositionProperty()
    position = PositionProperty()
    radius = osvg.float.FloatProperty()
    x_shift = osvg.float.FloatProperty()
    y_shift = osvg.float.FloatProperty()

    def __init__(
        self,
        center: Position,
        position: Position,
        radius: osvg.float.Float | float,
    ) -> None:
        super().__init__()
        self.center = center
        self.position = position
        self.radius = radius

        angle = AngleDegree(a=self.center, b=self.position)
        self.x = osvg.float_math.Sum(
            center.x,
            XonCircle(angle=angle, radius=self.radius),
        )
        self.y = osvg.float_math.Sum(
            center.y,
            YonCircle(angle=angle, radius=self.radius),
        )
