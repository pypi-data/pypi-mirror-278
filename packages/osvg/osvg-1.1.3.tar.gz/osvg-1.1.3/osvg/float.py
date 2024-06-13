"""
Module to define the basic Float classes.
"""

from collections.abc import Iterable


class Float:
    """
    An Float is an object that has other Float objects as
    inputs and output.
    With Float you can build a loop-free directed graph for calculating
    dynamically float numbers.
    """

    str_round = 3

    def __init__(
        self, inputs: list["Float"] | None = None, outputs: list["Float"] | None = None
    ) -> None:
        self.inputs = []
        self.outputs = []
        if inputs is not None:
            for i in inputs:
                self.add_input(i)
        if outputs is not None:
            for o in outputs:
                self.add_output(o)

    @staticmethod
    def verify_other(other: any, class_check: bool = True):
        """
        Verify if other's class is a subclass to IOR
        """
        if class_check and not issubclass(type(other), Float):
            raise TypeError("Other's class is not a subclass to Float")

    @property
    def input_history(self) -> set["Float"]:
        """
        Get all inputs of all inputs recursively
        """
        input_history = set(self.inputs)
        for i in input_history:
            input_history.union(i.input_history)
        return input_history

    def add_input(self, other: "Float") -> None:
        """
        Add other Float object as a input
        """
        self.verify_other(other)
        if self in other.input_history:
            raise RuntimeError("Input loop detected")
        self.inputs.append(other)
        other.outputs.append(self)
        self.input_changed()

    def remove_input(self, other: "Float") -> None:
        """
        Remove other Float object from inputs
        """
        self.inputs.remove(other)
        other.outputs.remove(self)
        self.input_changed()

    def add_output(self, other: "Float") -> None:
        """
        Add other Float object as a output
        """
        self.verify_other(other)
        other.add_input(self)

    def remove_output(self, other: "Float") -> None:
        """
        Remove other Float object from outputs
        """
        other.remove_input(self)

    def replace_by(self, other: "Float") -> "Float":
        """
        - Remove all my inputs
        - Move all my outputs to other's outputs
        - Return other
        """
        if self == other:
            raise RuntimeError("Cannot replace myself")
        for i in self.inputs:
            self.remove_input(i)
        for o in self.outputs:
            other.add_output(o)
            self.remove_output(o)
        return other

    def my_input_changed(self):
        """
        Perform actions on input change
        """

    def input_changed(self):
        """
        Inform myself and all outputs about an input change
        """
        self.my_input_changed()
        for o in self.outputs:
            o.input_changed()

    @property
    def value(self) -> None:
        """
        Get the value of the reference Float object
        """
        raise NotImplementedError

    def __str__(self) -> str:
        v = round(self.value, self.str_round)
        if v == 0:
            v = 0
        return f"{v:g}"


class Const(Float):
    """
    Float with an attribute 'value' as a floating number
    """

    def __init__(self, value: float) -> None:
        super().__init__()
        self._value = float(value)

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float | int) -> None:
        self._value = value
        self.input_changed()


class RefFloat(Float):
    """
    Is always an intermediate "input" to another Float object
    """

    def __init__(self, float_ref: Float = None):
        super().__init__()
        self._float_ref = None
        if float_ref is not None:
            self.float_ref = float_ref

    @property
    def float_ref(self) -> Float:
        """
        Get the reference Float object
        """
        return self._float_ref

    @float_ref.setter
    def float_ref(self, float_ref: Float):
        if float_ref is None:
            if self._float_ref is not None:
                self.remove_input(self._float_ref)
            self._float_ref = None
            return
        if not issubclass(type(float_ref), Float):
            raise TypeError("Float reference must be a Float object")
        if self._float_ref is not None:
            self._float_ref = self._float_ref.replace_by(float_ref)
        else:
            self._float_ref = float_ref
        self.add_input(self._float_ref)

    @property
    def value(self) -> float:
        if self.float_ref is None:
            return None
        return self.float_ref.value


class FloatProperty:
    """
    Property descriptor for Float objects.
    It automatically creates an intermediate Float object,
    which uses the given Float object as input.
    Or, if input is a python native float or int, it creates
    a Float object with that value and use it as the input.
    """

    def __init__(self):
        self.instances = {}

    def __get__(self, instance, owner):
        return self.instances[instance]

    def __set__(self, instance, f):
        if f is not None and not issubclass(type(f), Float):
            f = Const(f)
        if instance not in self.instances:
            self.instances[instance] = RefFloat(f)
        else:
            self.instances[instance].float_ref = f


class FloatList:
    """
    List of Float values
    """

    name = "values"

    def __init__(self, values: Iterable[int | float | Float] = None) -> None:
        self._values = []
        if values is not None:
            self.values = values

    @property
    def values(self) -> list[Float]:
        """
        Get value list
        """
        return self._values

    @values.setter
    def values(self, values: Iterable[int | float | Float]) -> None:
        """
        Verify and set values
        """
        if not isinstance(values, list):
            raise TypeError(f"{self.name} must be a list of float values")
        for value in values:
            if not issubclass(type(value), Float):
                value = Const(value)
            self._values.append(RefFloat(float_ref=value))

    def __str__(self) -> str:
        if not self.values:
            return ""
        return ",".join([str(value) for value in self.values])

    def copy(self):
        """
        Return an object with the same float values as values
        """
        return self.__class__(values=[v.float_ref for v in self.values])

    @property
    def isdefault(self) -> bool:
        """
        Check, if object's value is not set.
        """
        return self.values == []

    def equals(self, other) -> bool:
        """
        Check, if other's float value is equal to self's float value
        """
        for i, v in enumerate(self.values):
            if v.float_ref.value != other.values[i].float_ref.value:
                return False
        return True
