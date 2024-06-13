"""
Module to define Float classes to calculate float numbers.
"""

from collections.abc import Iterable
import math
import osvg.float
import osvg.helper


class MathFloat(osvg.float.RefFloat):
    """
    Base class for all "calculated" Float classes
    """

    def __init__(
        self,
        float_ref: osvg.float.Float,
    ) -> None:
        super().__init__(float_ref=float_ref)
        self._value = None

    def fill_cache(self) -> None:
        """
        Calculate the value for the cache
        """
        raise NotImplementedError

    @property
    def value(self) -> float:
        if self._value is None:
            self.fill_cache()
        return self._value

    def my_input_changed(self):
        self._value = None
        return super().my_input_changed()


class InvertedSign(MathFloat):
    """
    Invert the sign of the referenced Float
    """

    def fill_cache(self) -> None:
        self._value = -self.float_ref.value


class Cos(MathFloat):
    """
    Cosinus value of an angle in degree
    """

    def fill_cache(self):
        self._value = math.cos(osvg.helper.radians(self.float_ref.value))


class Sin(MathFloat):
    """
    Sinus value of an angle in degree
    """

    def fill_cache(self):
        self._value = math.sin(osvg.helper.radians(self.float_ref.value))


class Cot(MathFloat):
    """
    Cotangent value of an angle in degree
    """

    def fill_cache(self):
        v = osvg.helper.radians(self.float_ref.value)
        self._value = math.cos(v) / math.sin(v)


class Tan(MathFloat):
    """
    Tangent value of an angle in degree
    """

    def fill_cache(self):
        v = osvg.helper.radians(self.float_ref.value)
        self._value = math.sin(v) / math.cos(v)


class CalculatedList(MathFloat):
    """
    Base class for all calculated Floats with a list of Float objects
    """

    def __init__(
        self,
        *args: Iterable[osvg.float.Float | float | int],
    ) -> None:
        super().__init__(float_ref=None)
        if not args:
            raise ValueError(f"{self.__class__} needs at least on argument")
        for v in args:
            if not issubclass(type(v), osvg.float.Float):
                v = osvg.float.Const(v)
            self.add_input(v)

    @property
    def floats(self) -> list[float]:
        """
        Get tuple of all float input object values
        """
        return tuple(x.value for x in self.inputs)

    def fill_cache(self) -> None:
        raise NotImplementedError


class CalculatedKwargs(MathFloat):
    """
    Base class for all calculated Floats with keyword Float objects arguments
    """

    def __init__(
        self,
        **kwargs: osvg.float.Float | float | int,
    ) -> None:
        super().__init__(float_ref=None)
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if not issubclass(type(v), osvg.float.Float):
                v = osvg.float.Const(v)
                kwargs[k] = v
            self.add_input(v)
        self.__dict__.update(kwargs)

    def fill_cache(self) -> None:
        raise NotImplementedError


class FunctFloat(CalculatedList):
    """
    Class for customized calculation of Floats by passing a external function
    """

    def __init__(
        self,
        args: Iterable[osvg.float.Float | float | int],
        funct: "function",
    ) -> None:
        super().__init__(*args)
        self.funct = funct

    def fill_cache(self) -> None:
        args = self.floats
        self._value = self.funct(*args)


class Prod(CalculatedList):
    """
    Multiply all given Floats.
    """

    def fill_cache(self) -> None:
        """
        Product of all given values
        """
        result = 1
        for v in self.floats:
            result = result * v
        self._value = result


class Sum(CalculatedList):
    """
    Sum up reference value and one or more other numbers or values.
    """

    def fill_cache(self) -> None:
        """
        Sum of all given values
        """
        self._value = sum(self.floats)


class Min(CalculatedList):
    """
    Get the lowest value of all given Floats.
    """

    def fill_cache(self) -> None:
        """
        Lowest values of all given values
        """
        self._value = min(self.floats)


class LowestAbs(CalculatedList):
    """
    Return the floating number with the lowest absolute value.
    """

    def fill_cache(self) -> None:
        """
        Lowest absolute value of all given values
        """
        floats = self.floats
        if not floats:
            raise RuntimeError("At least one input required")
        lowest_value = floats[0]
        for v in floats[1:]:
            if abs(v) < abs(lowest_value):
                lowest_value = v
        self._value = lowest_value


class Max(CalculatedList):
    """
    Get the highest value of all given Floats.
    """

    def fill_cache(self) -> None:
        """
        Highest values of all given values
        """
        self._value = max(self.floats)


class PercentOf(CalculatedKwargs):
    """
    Calculate percentage of a value
    """

    def __init__(
        self,
        reference: osvg.float.Float,
        percentage: int | float | osvg.float.Float,
        modulo: bool = False,
    ) -> None:
        super().__init__(reference=reference, percentage=percentage)
        self._modulo = False
        self.modulo = modulo

    @property
    def modulo(self) -> bool:
        """
        Get modulo value
        """
        return self._modulo

    @modulo.setter
    def modulo(self, _bool: bool) -> None:
        self._modulo = _bool
        self.input_changed()

    def fill_cache(self) -> None:
        # pylint: disable=no-member
        if self.modulo:
            self._value = self.reference.value / 100 * (self.percentage.value % 100)
        else:
            self._value = self.reference.value / 100 * self.percentage.value
