# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

"""
This module implements extended finite fields as defined by Galois.

## Introduction

Modular integer fields are limited to a prime number of elements. By using such fields to construct
polynomials, it is possible to define a field structure of higher order.

Formally, any finite field contains *p*<sup>*n*</sup> elements, for some prime number *p* and some integer
*n* > 0. When *n* = 1, the field is represented by modular integers. When *n* > 1, the field can be defined
as a Galois extension over the field of modular integers.

Galois arithmetic uses the proper divisors of the degree *n*. These are the integers *m* such that *n*/*m* is
a prime number. This module provides a basic `factors()` function which is used to identify proper divisors.

## Polynomial representation

Galois fields can be constructed as polynomials with modular integer coefficients. This conveniently provides
the additive group structure. Multiplication can be defined by using regular polynomial multiplication: the
product of two elements from Galois field of degree *n* is the remainder after dividing the result by a
monic, irreducible polynomial of degree *n*.

The `Galois` class implements a finite field whose elements are univariate modular polynomials. The field
`Galois[p, n]` is represented by all polynomials of degree *n*-1 or lower with integer coefficients modulo
*p*. It contains *p*<sup>*n*</sup> elements.

## Multiplicative group

A convention is required to choose the polynomial which defines multiplication. This requires an ordering:
the alternating lexicographical ordering defined by Parker and detailed in `elliptic.poly`.

The Conway polynomial of a field `Galois[p, n]` is the smallest monic, irreducible, primitive polynomial of
degree *n*, with coefficients modulo *p*, compatible with all Conway polynomials for proper divisors of *n*.

For a prime modulus *p*, a modular polynomial *C*<sub>*n*</sub> is compatible with the Conway polynomial
*C*<sub>*m*</sub> (whose degree *m* is a proper divisor of *n*) when
*C*<sub>*m*</sub>(*X*<sup>(*p*<sup>*n*</sup>-1)/(*p*<sup>*m*</sup>-1)</sup>) is divisible by
*C*<sub>*n*</sub>(X).

Equivalently:
```python
c_m.of(
    c_m.one() << ((c_n.modulus**c_n.deg - 1) // (c_m.modulus**c_m.deg - 1))
) % c_n == 0
```

The class method `Galois.conway()` returns the Conway polynomial of the Galois field. The multiplication of
two Galois element is based on the regular product of their polynomial representations. If the degree of the
product is lower than the field degree then no more steps are required. Otherwise, the product is divided by
the Conway polynomial and the remainder of the division is used.

>>> P = PolyModular[3]
>>> G = Galois[3,2]
>>> print(P.from_string("X") * P.from_string("X+1"))
X**2 + X
>>> print(G.from_string("X") * G.from_string("X+1"))
2*X + 1
>>> print(P.from_string("X**2 + X") % G.conway())
2*X + 1
"""

from collections.abc import Iterator
from dataclasses import dataclass
from elliptic.abc import FiniteField
from elliptic.mod import Modular
from elliptic.poly import BasePoly, MetaPoly, PolyModular
from functools import cache
from typing import Any, ClassVar, Final, Self


def factors(n: int, /) -> dict[int, int]:
    """
    Return the prime factors of *n* with their exponents.

    The returned dictionary is indexed by the prime factors of *n* and its values are the corresponding
    exponents.

    >>> factors(0), factors(1)
    ({}, {})
    >>> factors(2), factors(-2)
    ({2: 1}, {2: 1})
    >>> factors(2310)
    {2: 1, 3: 1, 5: 1, 7: 1, 11: 1}
    >>> factors(1280)
    {2: 8, 5: 1}

    Implemented by trial division which has O(sqrt(*n*)) complexity (exponential).
    """
    if not isinstance(n, int):
        raise TypeError(f"unsupported for factorization: {type(n).__name__}")
    p = 2
    f: dict[int, int] = {}
    while abs(n) > 1:
        if n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
            continue
        p += 1 if p == 2 else 2
    return f


class MetaGalois(MetaPoly):
    """
    The metaclass of Galois fields, allowing for creation of `Galois[modulus, degree]` subclasses.

    >>> isinstance(Galois[2, 3], MetaGalois)
    True
    """

    attr_names: ClassVar[tuple[str, ...]] = ("modulus", "degree")
    """The name of the attributes passed as subscript: "modulus" and "degree"."""

    def attrs(cls, key: Any) -> tuple[Any, ...]:
        """
        Return the *key* subscript if it is a tuple of a prime number and a positive integer, raise
        `TypeError` or `ValueError` otherwise.
        """
        if not isinstance(key, tuple):
            raise TypeError(f"invalid index type: {type(key).__name__}")
        if len(key) != len(cls.attr_names):
            raise ValueError(f"expected index as {cls.attr_names} but got: {key}")
        attrs = (*_, degree) = key
        if not isinstance(degree, int) or degree < 0:
            raise TypeError(f"invalid degree: {degree}")
        return attrs


class BaseGalois(BasePoly):
    """
    The abstract base class of Galois fields.
    """

    # Hack for final classvars until they are implemented
    # See https://github.com/python/cpython/issues/89547
    degree: Final[int] = 0
    """The degree of the field."""


@dataclass(frozen=True)
class Galois(PolyModular, BaseGalois, FiniteField, metaclass=MetaGalois):
    """
    Galois field elements are constructed from a modulus, a degree and a list of modular coefficients.

    Calling `Galois[m, d]` returns a subclass with the `modulus` and `degree` class variables set. Such a
    subclass takes a single argument `coeffs` to construct a Galois element.

    When the subclass is created, `elliptic.mod.isprime()` is called on the modulus: if it returns `False`,
    then `ValueError` is raised.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        if not all(getattr(self, attr, None) is not None for attr in MetaGalois.attr_names):
            raise TypeError(f"degree and modulus are required, use {self.__class__.__qualname__}[degree, modulus]")
        if not self.deg < self.degree:
            object.__setattr__(self, "coeffs", (PolyModular[self.modulus](self.coeffs) % self.conway()).coeffs)
        if self.nonzero and not len(set(m for c in self.coeffs if (m := getattr(c, "modulus", None)))) == 1:
            raise ValueError(f"moduli of Gallois coefficients do not match: {self.coeffs}")

    def __hash__(self) -> int:
        return hash((self.modulus, self.degree, tuple(self.coeffs), self.format))

    @classmethod
    def zero(cls) -> Self:
        """
        Return the neutral element of addition.
        """
        return cls([cls.M(0)])

    @classmethod
    def one(cls) -> Self:
        """
        Return the neutral element of multiplication.
        """
        return cls([cls.M(1)])

    @classmethod
    def order(cls) -> int:
        return int(cls.modulus**cls.degree)

    @classmethod
    def from_roots(cls, *roots: Modular) -> Self:
        if not roots or len(roots) > cls.degree - 1:
            raise ValueError(f"unsupported number of roots for degree {cls.degree} polynomial: {len(roots)}")
        (root, *others) = roots
        return super().__mul__(cls([-root, cls.M(1)]), cls.from_roots(*others) if others else cls([cls.M(1)]))

    @classmethod
    def monics(cls) -> Iterator[PolyModular]:
        """
        Return an iterator over all monic polynomials of the field's degree.

        The polynomials are sorted according to Parker's lexicographical ordering.
        """

        def ordered_ints(modulus: int, degree: int) -> Iterator[list[int]]:
            if degree == 0:
                yield []
                return
            for i in range(modulus):
                for rec in ordered_ints(modulus, degree - 1):
                    yield [-j for j in rec] + [i]

        if cls.degree == 0:
            yield PolyModular[cls.modulus].one()
            return
        for ints in ordered_ints(cls.modulus, cls.degree):
            yield PolyModular[cls.modulus]([cls.M(-i) for i in ints] + [cls.M.one()])

    @classmethod
    def is_primitive(cls, poly: PolyModular) -> bool:
        """
        Return `True` if *poly* is a primitive polynomial of the Galois field, `False` otherwise.

        A primitive polynomial is the minimal polynomial of a primitive element of the field.
        """
        for factor in factors(m := cls.modulus**cls.degree - 1).keys():
            proper = m // factor
            if ((PolyModular[cls.modulus].one() << proper) - PolyModular[cls.modulus].one()) % poly == 0:
                return False
        return True

    @classmethod
    @cache
    def conway(cls) -> PolyModular:
        """
        Return the Conway polynomial of the Galois field, as defined by Parker: the lexicographically
        smallest, monic, primitive polynomial compatible with all Conway polynomials for proper divisors
        of the field degree.

        The Conway polynomial is necessary to define the multiplicative group of the Galois field. Results
        are cached because computation is expensive and the same polynomial is used for every multiplication.
        """

        if cls.degree == 1:
            for i in range(1, cls.modulus):
                if (mod := cls.M(i)).primitive:
                    return PolyModular[cls.modulus].from_roots(mod)

        def compatible(candidate: PolyModular, divisor: PolyModular) -> bool:
            exp, rem = divmod(cls.modulus**candidate.deg - 1, cls.modulus**divisor.deg - 1)
            assert rem == 0, f"{divisor.deg} must divide {candidate.deg}"
            return bool(divisor.of(divisor.one() << exp) % candidate == 0)

        # Brute-force search
        primes = factors(cls.degree).keys()
        for p in cls.monics():
            if not cls.is_primitive(p):
                continue
            if all(
                compatible(PolyModular[p.modulus](p.coeffs), cls[cls.modulus, cls.degree // factor].conway())
                for factor in primes
            ):
                return p
        assert False, "Conway polynomials must exist"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return super().__eq__(other)
        return isinstance(other, Galois) and (self.modulus, self.degree, self.coeffs) == (
            other.modulus,
            other.degree,
            other.coeffs,
        )

    def __pos__(self) -> Self:
        return super().__pos__()

    def __neg__(self) -> Self:
        return super().__neg__()

    def __add__(self, other: object) -> Self:
        return super().__add__(other)

    def __sub__(self, other: object) -> Self:
        return super().__sub__(other)

    def __mul__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        if isinstance(other, Galois) and self.degree != other.degree:
            raise TypeError(f"invalid operand type: degrees {self.degree} and {other.degree} do not match")
        return super().__mul__(other)

    def __rmul__(self, other: object) -> Self:
        if not isinstance(other, (Modular, int)):
            return NotImplemented
        if other == 0:
            return self.zero()
        if other < 0:
            return -self.__rmul__(-other)
        return self + (other - 1) * self

    def __pow__(self, other: int, _: None = None) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        if other < 0:
            raise ValueError(f"invalid exponent for Galois: {other}")
        if other == 0:
            return self.one()
        return self * self ** (other - 1)

    @property
    def inverse(self) -> Self:
        if not (lead := self.leading):
            raise ZeroDivisionError("division by zero")
        if self.deg == 0:
            return type(self).from_coeffs(lead.inverse)

        # Recursive Euclidian division
        r, new_r = self.conway(), self
        t, new_t = self.zero(), self.one()
        while new_r != 0:
            quotient = r // new_r
            r, new_r = new_r, r - quotient * new_r
            t, new_t = new_t, t - quotient * new_t
        assert r.deg == 0, f"{r} must be a constant"
        return type(self)(r.coeffs).inverse * t

    def __truediv__(self, other: object) -> Any:
        if not isinstance(other, Galois) or (self.modulus, self.degree) != (other.modulus, other.degree):
            return NotImplemented
        return self * other.inverse

    def __rtruediv__(self, _: Any) -> Any:
        return NotImplemented

    def sqrt(self) -> Self | None:
        # Trivial mode
        if self == 0:
            return self

        # Easy mode: everything is a square
        if self.modulus == 2:
            return self ** (self.order() // 2)

        # Hard mode: Adleman-Manders-Miller algorithm
        criterion = (self.order() - 1) // 2
        if self**criterion != 1:  # Euler's criterion
            return None
        seed = self.one()
        while seed == 0 or seed**criterion == 1:  # Find a quadratic nonresidue
            seed = self.random(self.degree)  # Go to Las Vegas
        assert seed != 1, "A quadratic nonresidue must exist"
        evenlog, odd = 0, self.order() - 1
        while odd % 2 != 1:  # Split order-1 into the odd part and the logarithm (base 2) of the even part
            odd //= 2
            evenlog += 1
        b = self**odd
        h = self.one()
        a = seed**odd
        for i in range(1, evenlog):
            k = 0 if b ** (2 ** (evenlog - i - 1)) == 1 else 1
            b *= a ** (2 * k)
            h *= a**k
            a *= a
        return h * self ** ((odd + 1) // 2)
