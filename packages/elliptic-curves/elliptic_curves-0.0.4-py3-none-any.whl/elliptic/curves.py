# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

# Curve definitions republished courtesy of the National Institute of Standards and Technology
# Chen et al. (2023), Recommendations for Discrete Logarithm-based Cryptography, NIST SP 800-186
# See https://csrc.nist.gov/pubs/sp/800/186/final or https://doi.org/10.6028/NIST.SP.800-186

"""
This module provides a geometric group structure on elliptic curves.

## Introduction

Elliptic curves are defined in a projective plane. They contain a point at infinity, located on the horizon.

If a line has at least two intersection points with an elliptic curve, then it has exactly three. That
property can be used to define a group structure on the curve.

Given a point `p` on the curve and the result `n * p` of summing `p` with itself many times, it can be
difficult to compute the integer `n`. That problem is called the discrete logarithm.

## Construction

A curve is constructed over a field:

>>> from elliptic.mod import Modular
>>> M = Modular[3]  # The finite field with three elements
>>> c = Curve[M](a=M(2), b=M(1))
>>> print(c.infinity)
(0, 1, 0)

Curve points can be conveniently found by fixing the abscissa value `x`. Simply compute `x**3 + a*x + b` and
take the square root if it exists.

That works reasonably well for modular integers:

>>> M = Modular[31]
>>> a, b = M(1), M(2)
>>> c = Curve(a, b)
>>> x = M(10)
>>> y = (x**3 + a*x + b).sqrt()
>>> p = BasePoint(x, y)
>>> c.contains(p)
True
>>> print(p)
(10, 19)

And it is trivial for real numbers:

>>> from elliptic.inf import Real
>>> a, b = Real(1), Real(2)
>>> c = Curve(a, b)
>>> x = Real(10)
>>> y = (x**3 + a*x + b).sqrt()
>>> p = BasePoint(x, y)
>>> c.contains(p)
True
>>> print(p)
(10, 31.81194744117373270749095566)

The same goes for Galois fields but the algorithms are more complex. This quickly gets slow for large fields:

>>> from elliptic.fin import Galois
>>> G = Galois[3, 3]
>>> a, b = G.one(), G.from_string("X + 2")
>>> c = Curve(a, b)
>>> x = G.from_string("2*X")
>>> y = (x**3 + a*x + b).sqrt()
>>> p = BasePoint(x, y)
>>> c.contains(p)
True
>>> print(p)
(2*X, 2*X**2 + X + 1)

## Interface

As long as the elements of a field are hashable, so are curves and points defined over it. All classes
defined in this module are meant to be immutable.

### Unary and binary operations

Consider two points `p1` and `p2` on an elliptic curve. The third-intersection `p1 @ p2` is the third point
where the line joining `p1` and `p2` intersects with the curve.

>>> M = Modular[5]
>>> c = Curve(a=M(1), b=M(2))
>>> p = Point(M(1), M(2), curve=c)
>>> print(p @ p)
(4, 0)

>>> c.infinity @ (p @ p) != (c.infinity @ p) @ p  # The operation is not associative
True

Unary negation is implemented by taking the third-intersection with the point at infinity. The binary
addition of two points `p1` and `p2` is implemented as `-(p1 @ p2)`.

>>> print(+p)
(1, 2)
>>> print(-p)
(1, 3)
>>> print(p + p)
(4, 0)
>>> print(p - p)
(0, 1, 0)
>>> p == p + c.infinity
True

### Integer multiplication

Since points can be added together, it makes sense that they can be multiplied by an integer. Multiplying by
zero returns the point at infinity. For a positive integer `n` and a point `p`, the operation can be defined
as `(n + 1)*p = n*p + p` by recursion. It is trivially extended by `-n * p = n * -p` for negative integers.

>>> print(3 * p)
(1, 3)
>>> print(4 * p)
(0, 1, 0)

By mathematical convention, integer multiplication is only supported on the left side.

### Comparison

Points support equality comparison:

>>> p = Point(M(1), M(2), curve=c)
>>> p == BasePoint(M(1), M(2))
True
>>> p == BasePoint(M(1), M(1))
False

The point at infinity is equal to zero:

>>> c.infinity == 0
True
"""

from dataclasses import dataclass, field
from elliptic.abc import Field, FiniteField
from elliptic.mod import ModularP
from math import sqrt
from typing import Generic, Self, TypeVar, cast

F = TypeVar("F", bound=Field)
"""A type representing any implementation of `elliptic.abc.Field`."""

FF = TypeVar("FF", bound=FiniteField)
"""A type representing any implementation of `elliptic.abc.FiniteField`."""


@dataclass(frozen=True)
class BasePoint(Generic[F]):
    """
    Construct a point in the projective plane *Z*=1 of a vector space over a field `F`.
    """

    X: F
    """The abscissa of the point."""
    Y: F
    """The ordinate of the point."""
    Z: F = cast(F, None)
    """The applicate of the point. Set to 1 if omitted."""

    def __post_init__(self) -> None:
        if self.Z is None:
            # Set Z to the one element of F
            object.__setattr__(self, "Z", (self.X - self.X) ** 0)
        if all(c == 0 for c in (self.X, self.Y, self.Z)):
            raise ValueError(f"origin point ({self.X}, {self.Y}, {self.Z}) is not projective")

    def is_inf(self) -> bool:
        """
        Return `True` if the point is at infinity, `False` otherwise.
        """
        return self.Z == 0

    @property
    def x(self) -> F:
        """
        The homogeneous abscissa of the point. If it is at infinity, then `ZeroDivisionError` is raised.
        """
        if self.is_inf():
            raise ZeroDivisionError(f"infinity point {self} is not homogeneous")
        assert isinstance(h := self.X / self.Z, type(self.Z))
        return h

    @property
    def y(self) -> F:
        """
        The homogeneous ordinate of the point. If it is at infinity, then `ZeroDivisionError` is raised.
        """
        if self.is_inf():
            raise ZeroDivisionError(f"infinity point {self} is not homogeneous")
        assert isinstance(h := self.Y / self.Z, type(self.Z))
        return h

    def __str__(self) -> str:
        return f"({self.X}, {self.Y}, {self.Z})" if self.is_inf() else f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BasePoint):
            return False
        if self.is_inf():
            return other.is_inf() and other.X * self.Y == self.X * other.Y
        if other.is_inf():
            return False
        return bool(self.x == other.x and self.y == other.y)


@dataclass(frozen=True)
class Curve(Generic[F]):
    """
    Construct a non-singular elliptic curve over a field `F`.

    The curve is defined by two coefficients `a` and `b` as:
    ```python
    x**3 + a * x + b == y ** 2
    ```

    The curve equation cannot be singular, so `a` and `b` cannot be such that:
    ```python
    4 * a**3 + 27 * b**2 == 0
    ```

    If the provided coefficients define a singular equation, then `ValueError` is raised.
    """

    _zero: F = field(init=False)
    _one: F = field(init=False)

    a: F
    """The coefficient of degree 1."""
    b: F
    """The coefficient of degree 0."""

    def __str__(self) -> str:
        return f"(a={self.a}, b={self.b})"

    @property
    def infinity(self) -> "Point[F]":
        """
        The point at infinity on the curve.
        """
        return Point(self._zero, self._one, self._zero, curve=self)

    def is_singular(self) -> bool:
        """
        Return `True` if the curve is singular, `False` otherwise.
        """
        return 4 * self.a**3 + 27 * self.b**2 == 0

    def __post_init__(self) -> None:
        if self.is_singular():
            raise ValueError(f"curve {self} is singular")
        object.__setattr__(self, "_zero", self.a - self.a)
        object.__setattr__(self, "_one", self._zero**0)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Curve)
            and isinstance(self.a, type(other.a))
            and self.a == other.a
            and isinstance(self.b, type(other.b))
            and self.b == other.b
        )

    def contains(self, point: BasePoint[F]) -> bool:
        """
        Return `True` if the curve contains *point*, `False` otherwise.
        """
        if point.is_inf():
            return point.X == 0 and point.Y == 1
        return point.X**3 + self.a * point.X * point.Z**2 + self.b * point.Z**3 - point.Y**2 * point.Z == 0


@dataclass(frozen=True, kw_only=True)
class Point(BasePoint[F]):
    """
    Construct a point on a `Curve` instance over a field `F`.

    If the coordinates do not verify the curve equation, then `ValueError` is raised.
    """

    curve: Curve[F]
    """The `Curve` to which the point belongs."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.curve.contains(self):
            raise ValueError(f"{self} does not belong to {self.curve}")

    @property
    def infinity(self) -> Self:
        """
        The point at infinity on the same curve.
        """
        p = self.curve.infinity
        return type(self)(p.X, p.Y, p.Z, curve=self.curve)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int) and other == 0:
            return self.is_inf()
        if isinstance(other, Point) and self.curve != other.curve:
            return False
        return super().__eq__(other)

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        if self.is_inf():
            return self
        return type(self)(self.x, -self.y, curve=self.curve)

    def third(self, other: Self) -> Self:
        """
        Return the third point where the curve intersects the line joining the point and *other*.

        Intersections include multiplicity, so `self.third(self)` is the intersection with the tangent to
        the curve at the point.
        """
        if other.curve != self.curve:
            raise ValueError(f"{other} is not on {self.curve}")
        if self.is_inf():
            return -other
        if other.is_inf():
            return -self
        if self == other:
            if self.y == 0:  # Vertical tangent at the middle of the curve
                return self.infinity
            slope = (3 * self.x**2 + self.curve.a) / (2 * self.y)
            return type(self)(x := slope**2 - 2 * self.x, slope * (x - self.x) + self.y, curve=self.curve)
        if self.x == other.x:  # Vertical line
            return self.infinity
        slope = (other.y - self.y) / (other.x - self.x)
        return type(self)(x := slope**2 - self.x - other.x, slope * (x - self.x) + self.y, curve=self.curve)

    def _operand(self, other: Self) -> Self:
        if self.curve != other.curve:
            raise ValueError(f"curves {self.curve} and {other.curve} do not match")
        return other

    def __matmul__(self, other: object) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        op = self._operand(other)
        return self.third(op)

    def __rmatmul__(self, other: object) -> Self:
        return self @ other

    def __add__(self, other: object) -> Self:
        return self.infinity @ (self @ other)

    def __radd__(self, other: object) -> Self:
        return self + other

    def __sub__(self, other: object) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        op = self._operand(other)
        return self + -op

    def __rsub__(self, other: object) -> Self:
        return -self + other

    def __rmul__(self, other: object) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        if other == 0:
            return self.infinity
        if other == 1:
            return self
        if other < 0:
            return -other * -self

        # Fast multiplication
        half, odd = divmod(other, 2)
        if odd:
            return self + (other - 1) * self
        return half * (self + self)


@dataclass(frozen=True)
class FiniteCurve(Curve[FF]):
    """
    Construct an elliptic curve over a finite field.
    """

    a: FF
    b: FF

    def max_order(self) -> int:
        """
        Return an upper bound on the group order of the curve.
        """
        q = self.a.order()
        return q + 2 * int(sqrt(q)) + 2  # Hasse's theorem

    def bsgs(self, gen: Point[FF], p: Point[FF]) -> int | None:
        """
        Return the discrete logarithm of *p* in base *gen* using the Baby Step Giant Step algorithm.

        If *gen* is not a generator of the curve and never adds up to *p*, then `None` is returned.
        """

        # Shanks' algorithm
        guess = self.infinity
        guesses: list[Point[FF]] = []
        max_ = int(sqrt(self.max_order())) + 1  # max_ is higher than the square root of the curve's order
        for j in range(max_):  # Precompute the first max_ discrete powers of the generator
            guess = guess if j == 0 else guess + gen
            if guess == p:
                return j
            guesses += [guess]
        step = -max_ * gen  # Define a giant step backwards
        guess = p + step  # Look for (i, j) such that j * gen == self + -max_ * i * gen
        for i in range(1, max_):
            try:
                return guesses.index(guess) + i * max_
            except ValueError:  # if guess not in guesses
                guess += step
        return None


@dataclass(frozen=True, kw_only=True)
class FinitePoint(Point[FF]):
    """
    Construct a point on an elliptic curve over a finite field.
    """

    curve: FiniteCurve[FF]

    @property
    def ord(self) -> int:
        """
        The order of the point in the curve group.
        """
        order = 1
        value = self
        while value != 0:
            order += 1
            value += self
        return order


@dataclass(frozen=True)
class CurveDef(Generic[F]):
    """
    The complete definition of an elliptic curve.
    """

    base: type[F]
    """The base field over which the curve is defined."""
    curve: Curve[F]
    """The curve itself."""
    point: Point[F]
    """A recommended starting point on the curve."""


curve: Curve[ModularP]  # Dummy variable to suppress pdoc
"""@private"""

P224 = CurveDef[ModularP](
    base := ModularP[2**224 - 2**96 + 1],
    curve := FiniteCurve[ModularP](
        a=base(-3), b=base(18958286285566608000408668544493926415504680968679321075787234672564)
    ),
    point=FinitePoint[ModularP](
        base(19277929113566293071110308034699488026831934219452440156649784352033),
        base(19926808758034470970197974370888749184205991990603949537637343198772),
        curve=curve,
    ),
)  # Republished courtesy of the National Institute of Standards and Technology
"""The elliptic curve P-224 as defined by NIST SP 800-186."""

P256 = CurveDef[ModularP](
    base := ModularP[2**256 - 2**224 + 2**192 + 2**96 - 1],
    curve := FiniteCurve[ModularP](
        a=base(-3), b=base(41058363725152142129326129780047268409114441015993725554835256314039467401291)
    ),
    point=FinitePoint[ModularP](
        base(48439561293906451759052585252797914202762949526041747995844080717082404635286),
        base(36134250956749795798585127919587881956611106672985015071877198253568414405109),
        curve=curve,
    ),
)  # Republished courtesy of the National Institute of Standards and Technology
"""The elliptic curve P-256 as defined by NIST SP 800-186."""
