# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

"""
This module defines fields with an infinite number of elements.

## Rational numbers

The `Rational` class represents the field of rational numbers, wrapped around Python's built-in `fractions`
implementation. They can be constructed from integers defining the numerator and denominator (the latter may
be omitted.)

>>> print(Rational(1, 2))
1/2
>>> print(Rational(2))
2
>>> print(Rational(4, 2))
2

For more details, see the Python `fractions` [documentation](https://docs.python.org/3/library/fractions.html).

## Real numbers

The `Real` class represents the field of real numbers, wrapped around Python's built-in `decimal`
implementation. They can be constructed from a string, an integer, a `float` or a `Decimal` object.

>>> Real(2)
Real('2')
>>> Real("1.414")
Real('1.414')

Note that a `float` value is a binary floating-point number. As such, it is not always equal to its printed
form. For example:
>>> Real(1.414)
Real('1.4139999999999999236166559057892300188541412353515625')

Real numbers contain the context for arithmetic from `decimal`, which specifies floating-point
precision and rouding rules, among other things. For more details, see the Python `decimal`
[documentation](https://docs.python.org/3/library/decimal.html).
"""

from dataclasses import dataclass
from decimal import Context, Decimal
from elliptic.abc import Field
from fractions import Fraction
from typing import Any, Generic, Self, TypeVar

N = TypeVar("N", Decimal, Fraction)
"""A type representing any of `decimal.Decimal` or `fractions.Fraction`."""


@dataclass(frozen=True)
class NumberField(Generic[N], Field):
    """
    The abstract class of fields wrapped around a number type.
    """

    value: N
    """The value of the underlying number."""

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value.__eq__(other)

    def __pos__(self) -> Self:
        if (res := self.value.__pos__()) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __neg__(self) -> Self:
        if (res := self.value.__neg__()) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __add__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__add__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __radd__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__radd__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __sub__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__sub__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __rsub__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__rsub__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __mul__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__mul__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __rmul__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__rmul__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    @property
    def inverse(self) -> Self:
        if (res := self.value.__rtruediv__(1)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __truediv__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__truediv__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __rtruediv__(self, other: Any) -> Self:
        if isinstance(other, type(self)):
            other = other.value
        if (res := self.value.__rtruediv__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)

    def __pow__(self, other: int, _: int | None = None) -> Self:
        if other == 0:
            return self.one()
        if (res := self.value.__pow__(other)) is NotImplemented:
            return NotImplemented
        return type(self)(res)


@dataclass(frozen=True, eq=False)
class Rational(NumberField[Fraction]):
    """
    Construct a rational number from a numerator and an optional denominator.

    The numerator may be an instance of `fractions.Fraction` in which case the denominator must be omitted or
    set to 1 or `ValueError` is raised.
    """

    value: Fraction

    def __init__(self, numerator: str | int | Fraction, denominator: str | int = 1) -> None:
        if isinstance(numerator, Fraction):
            if int(denominator) != 1:
                raise ValueError(f"Denominator {denominator} does not make sense with numerator {numerator}")
            object.__setattr__(self, "value", numerator)
        else:
            object.__setattr__(self, "value", Fraction(int(numerator), int(denominator)))

    @classmethod
    def zero(cls) -> Self:
        return cls(0)

    @classmethod
    def one(cls) -> Self:
        return cls(1)

    @property
    def numerator(self) -> int:
        return self.value.numerator

    @property
    def denominator(self) -> int:
        return self.value.denominator

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.numerator}, {self.denominator})"


@dataclass(frozen=True, eq=False)
class Real(NumberField[Decimal]):
    """
    Construct a real number from a value and an optional context.
    """

    value: Decimal

    def __init__(self, value: str | int | float | Decimal, /, context: Context | None = None) -> None:
        object.__setattr__(self, "value", Decimal(value, context))

    @classmethod
    def zero(cls) -> Self:
        return cls(0)

    @classmethod
    def one(cls) -> Self:
        return cls(1)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}('{super().__str__()}')"

    def sqrt(self) -> Self:
        """
        Return the square root of the number to full precision.
        """
        return type(self)(self.value.sqrt())
