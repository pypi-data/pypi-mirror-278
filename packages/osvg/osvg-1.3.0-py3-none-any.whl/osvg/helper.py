"""
Module to provide helper classes
"""

import math


class WeightedList:
    """
    A weighted list is list of elements with integer based weights.
    The default weight is 0. On iteration elements with higher weight
    will be processed first.
    Elements with same weight will be processed as they were
    appended, prepended or inserted.
    """

    def __init__(self) -> None:
        self._weighted_elements = {}
        self._index = 0
        self._list = []

    def _add_weight(self, weight: int) -> None:
        """
        Add a weight to the list.
        """
        if weight not in self._weighted_elements:
            self._weighted_elements[weight] = []

    @property
    def weights(self) -> list[int]:
        """
        Returns a sorted list of weights.
        """
        return sorted(list(self._weighted_elements), reverse=True)

    def append(self, new_element: any, weight: int = 0) -> None:
        """
        Add a new element to the end of the list.
        Optional the weight can be specified.
        """
        self._add_weight(weight)
        self._weighted_elements[weight].append(new_element)

    def insert(self, index: int, new_element: any, weight: int = 0) -> None:
        """
        Insert a new element at a specific position (index) of the list.
        Optional the weight can be specified.
        """
        self._add_weight(weight)
        self._weighted_elements[weight].insert(index, new_element)

    def prepend(self, new_element: any, weight: int = 0) -> None:
        """
        Add a new element to the beginning of the list.
        Optional the weight can be specified.
        """
        self.insert(0, new_element, weight)

    def __len__(self) -> int:
        """
        Returns the length of the list.
        """
        length = 0
        for l in self._weighted_elements.values():
            length += len(l)
        return length

    @property
    def length(self) -> int:
        """
        Length of the list.
        """
        return len(self)

    def length_w(self, weight: int) -> int:
        """
        Return the amount of elements for a given weight.
        """
        if weight not in self._weighted_elements:
            return 0
        return len(self._weighted_elements[weight])

    def list_w(self, weight: int) -> list:
        """
        Returns the list for a given weight.
        """
        if weight not in self._weighted_elements:
            raise IndexError(f"Weight {weight} not in this list")
        return self._weighted_elements[weight]

    @property
    def list(self) -> list:
        """
        Returns all elements according to the weight.
        """
        l = []
        for w in self.weights:
            l += self._weighted_elements[w]
        return l

    def __iter__(self):
        self._index = 0
        self._list = self.list
        return self

    def __next__(self):
        if self._index == len(self):
            raise StopIteration
        self._index += 1
        return self._list[self._index - 1]

    def extend(self, other: "WeightedList"):
        """
        Add all other's weighted element to self
        """
        # pylint: disable=protected-access
        if not isinstance(other, WeightedList):
            raise TypeError("Can only extend with another WeightedList")
        for w, elements in other._weighted_elements.items():
            if w in self._weighted_elements:
                self._weighted_elements[w].extend(elements)
            else:
                self._weighted_elements[w] = elements


def radians(angle: float) -> float:
    """
    Return the radiant of an angle in degree.
    Note: angle=0 ist 3 o'clock and it goes clockwise.
    """
    return -math.radians(angle)


def degrees(radiant: float) -> float:
    """
    Return the angle of a radiant float value.
    Note: angle=0 ist 3 o'clock and it goes clockwise.
    """
    return -math.degrees(radiant)


def x_position_on_circle(angle: float = 0, radius: float = 1) -> float:
    """
    Calculate the delta for x of a point on a circle with radius 'radius'
    and the angle 'anlge' in degrees.
    Note: angle=0 ist 3 o'clock and it goes clockwise.
    """
    # 1. Get the cosine of the radiant
    # 2. multiply by the radius of the circle
    # 3. Return float rounded to 3 decimals
    return round(math.cos(radians(angle)) * radius, 3)


def y_position_on_circle(angle: float = 0, radius: float = 1) -> float:
    """
    Calculate the delta for y of a point on a circle with radius 'radius'
    and the angle 'anlge' in degrees.
    Note: angle=0 ist twelve o'clock and it goes clockwise.
    """
    # 1. Get the sine of the radiant
    # 2. Invert (multiple by -1) to get the delta in a SVG oriented coordinational system
    # 3. multiply by the radius of the circle
    # 4. Return float rounded to 3 decimals
    return round(math.sin(radians(angle)) * -1 * radius, 3)


def angle_a_b(b: tuple[float, float], a: tuple[float, float] = None) -> float:
    """
    Angle from position 'a' (x, y) to position 'b' (x, y) in degrees.
    Rotation is clockwise with 0 == "12 o'clock"
    """
    if a is None:
        a = (0, 0)
    dx = b[0] - a[0]
    dy = a[1] - b[1]  # due to the inverted y-axis
    return degrees(math.atan2(dy, dx))


def radian_a_b(b: tuple[float, float], a: tuple[float, float] = None) -> float:
    """
    Angle from position 'a' (x, y) to position 'b' (x, y) in radians.
    """
    if a is None:
        a = (0, 0)
    dx = b[0] - a[0]
    dy = a[1] - b[1]  # due to the inverted y-axis
    return math.atan2(dy, dx) % (2 * math.pi)
