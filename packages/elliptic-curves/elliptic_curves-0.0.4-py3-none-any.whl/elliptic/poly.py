# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

"""
This module implements univariate polynomials over modular integers.

## Introduction

Formally, a univariate polynomial is a sum of terms, each comprised of a coefficient and a positive integer
power of a variable. Coefficients are scalars and variables can be any vector over the scalar field. For
example, *X*<sup>3</sup> + 2 * *X* + 2 is a polynomial of degree three and its coefficients are 2, 2, 0 and 1
in little endian (lowest exponent term first).

Polynomials form an infinite-dimensional vector space over the scalar field. They can be added or substracted
and they can be multiplied by a scalar. They can also be multiplied together using the distributivity rule.

The `PolyModular` class implements univariate polynomials over the field of modular integers. The class of
polynomials with coefficients modulo *p* can be constructed as `PolyModular[p]` if *p* is a prime number.
Polynomials are instantiated from a list of coefficients in little endian.

>>> P = PolyModular[3]
>>> print(P([P.M(2), P.M(2), P.M(0), P.M(1)]))
X**3 + 2*X + 2

## Parsing

Modular polynomials can be parsed using a predefined format. Terms may be written in any order and will be
aggregated by degree.

>>> p = P.from_string("X**3+2*X+2")
>>> [int(c) for c in p.coeffs]
[2, 2, 0, 1]
>>> print(p)
X**3 + 2*X + 2

All whitespace characters are ignored. Substractions are supported. Multiplication signs may be omitted.

>>> print(P.from_string("1 + 1 * X + X ** 3 + X + 1"))
X**3 + 2*X + 2
>>> print(P.from_string("X**3-X+2"))
X**3 + 2*X + 2
>>> print(P.from_string("X + 2X**2"))
2*X**2 + X

The format can be customized by changing the various class variables (see the `PolyFormat` documentation for
details). The `big_endian` boolean controls the order in which terms are printed.

>>> P.format = PolyFormat(big_endian=False)
>>> print(P.from_string("X**3+2*X+2"))
2 + 2*X + X**3
>>> P.format = DefaultFormat
>>> print(P.from_string("X**3+2*X+2"))
X**3 + 2*X + 2

## Interface

Polynomials support addition, substraction and multiplication. The `divmod()` function implements
Euclidian division, along with the `//` and `%` operators.

The `<<` and `>>` operators can be used to shift a polynomial's degree. Right-shifting will erase all
coefficients of degree lower than the operand.

>>> print(P.from_string("X + 1") << 3)
X**4 + X**3
>>> print(P.from_string("2*X**2 + X + 1") >> 2)
2

`PolyModular` overloads the matrix multiplication operator `@` to implement scalar multiplication:

>>> s = P.M(2)
>>> print(s @ P.from_string("X**2 + 2"))
2*X**2 + 1

Scalar multiplication is also accepted using `*` but only on the left side, as mathematical convention:

>>> print(s * P.from_string("X**2 + 2"))
2*X**2 + 1
>>> print(P.from_string("X**2 + 2") * s)
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for *: 'PolyModular' and 'Modular'

## Ordering

Modular polynomials implement lexicographical ordering in the sense of Parker. Consider two polynomials of
degree *n*:

> *p* = *p*<sub>0</sub> + *p*<sub>1</sub> * *X* + ... + *p*<sub>n</sub> * *X*<sup>*n*</sup>

> *q* = *q*<sub>0</sub> + *q*<sub>1</sub> * *X* + ... + *q*<sub>n</sub> * *X*<sup>*n*</sup>

They are ordered *p* < *q* when there is an integer *k* such that:
- *p*<sub>*i*</sub> = *q*<sub>*i*</sub> for *k* < *i* < *n* + 1
- (-1)<sup>*n*-*k*</sup> * *p*<sub>*k*</sub> > (-1)<sup>*n*-*k*</sup> * *q*<sub>*k*</sub>

This is a counter-intuitive ordering wherein the comparison reverses the sign of every other coefficient:

>>> P.from_string("X + 2") < P.from_string("X + 1")
True
>>> P.from_string("X**2 + 2*X") < P.from_string("X**2 + X")
True

This ordering implies a norm based on the lexicographical distance to zero:

>>> [abs(P.from_string(s)) for s in ("0", "2", "X", "X+2", "X+1", "X**2+1", "X**2+2*X", "X**2+X")]
[0, 2, 3, 4, 5, 10, 12, 15]

## Factorization

Polynomials have a unique composition of irreducible factors, much like integers have prime factors. For
modular polynomials, factorization traditionally takes three stages.

The polynomial is first split into square-free factors by the `PolyModular.sff()` method. Each of those is
decomposed by `PolyModular.ddf()` into products of irreducible factors of equal degree. Each equal-degree
product can then be split into irreducible factors by the `PolyModular.edf()` method.

The full factorization process is implemented by the `PolyModular.factors()` method:

>>> p = P.from_string("X**11 + 2*X**9 + 2*X**8 + X**6 + X**5 + 2*X**3 + 2*X**2 + 1")
>>> " * ".join(f"({f}){'**' + str(e) if e!=1 else ''}" for f,e in p.factors().items())
'(X + 1) * (X + 2)**4 * (X**2 + 1)**3'
"""

from dataclasses import dataclass
from elliptic.abc import ProtoVar
from elliptic.mod import BaseModular, MetaModular, Modular
from itertools import zip_longest
from typing import Any, ClassVar, Final, Self, TypeVar


class MetaPoly(MetaModular):
    """
    The metaclass of modular polynomials, allowing for creation of `PolyModular[modulus]` subclasses.

    >>> isinstance(PolyModular[2], MetaPoly)
    True
    """

    def _dict(cls, key: Any) -> dict[str, Any]:
        return super()._dict(key) | {"M": Modular[cls.attrs(key)[0]]}


class BasePoly(BaseModular):
    """
    The abstract base class of modular polynomials.

    Classes implementing vector spaces over modular integers should inherit the `modulus` class variable and
    declare `MetaPoly` (or any approriate subclass thereof) as metaclass. The underlying scalar field is
    exposed as the `M` class variable:

    >>> PolyModular[2].M(1)
    Modular[2](1)
    """

    M: Final[type[Modular]] = Modular
    """The modular field, set by the metaclass when the polynomial class is called with a specific modulus."""


@dataclass(frozen=True)
class PolyFormat:
    """
    Construct a format to parse and print polynomials.
    """

    var: str = "X"
    """The name of the variable."""

    add: str = "+"
    """The operator used to separate terms."""

    sub: str = "-"
    """The operator used for negative terms."""

    mul: str = "*"
    """The operator used between the coefficient and the variable."""

    exp: str = "**"
    """The operator used between the variable and the exponent."""

    sep: str = " "
    """The separator used before and after `add`."""

    big_endian: bool = True
    """Whether to print polynomials with the highest degree term first."""

    def term_str(self, coeff: Modular, deg: int) -> str:
        """
        Return a string representing a term.
        """
        if not coeff:
            return ""
        operator = self.add
        infix = f"{self.sep}{operator}{self.sep}"
        factor = abs(coeff) if deg == 0 else "" if coeff in (-1, 1) else f"{abs(coeff)}{self.mul}"
        term = "" if deg == 0 else f"{self.var}{'' if deg == 1 else self.exp + str(deg)}"
        return f"{infix}{factor}{term}"

    def poly_str(self, coeffs: list[Modular]) -> str:
        """
        Return a string representing a polynomial.
        """
        terms = (self.term_str(coeff=coeff, deg=deg) for deg, coeff in enumerate(coeffs))
        strs = "".join(reversed(tuple(terms)) if self.big_endian else terms)
        if not strs:
            return "0"
        return strs[1 + 2 * len(self.sep) :]

    def parse_coeffs(self, string: str) -> list[int]:
        """
        Return a list of integer coefficients parsed from a string.
        """
        if not (stripped := string.strip()):
            raise ValueError(f"invalid poly string: {string}")
        coeffs: dict[int, int] = {}
        for i, s in enumerate(stripped.replace(self.sub, self.add + self.sub).split(self.add)):
            if not (term := s.strip()):
                if i == 0:
                    continue  # Ignore leading plus sign
                raise ValueError(f"empty term in poly string: {string}")
            if self.var not in term:
                coeffs[0] = coeffs.get(0, 0) + int(term.replace(" ", ""))
                continue
            [factor, exponent] = [s.strip() for s in term.split(self.var, maxsplit=1)]
            if not factor:
                coeff = "1"
            elif factor == self.sub:
                coeff = "-1"
            else:
                coeff = factor.removesuffix(self.mul).rstrip()
            if not exponent:
                deg = "1"
            elif (deg := exponent.removeprefix(self.exp)) == exponent:
                raise ValueError(f"invalid exponent in term: {term}")
            coeffs[int(deg)] = coeffs.get(int(deg), 0) + int(coeff)
        return [coeffs.get(degree, 0) for degree in range(max(coeffs.keys()) + 1)]


DefaultFormat: Final[PolyFormat] = PolyFormat()
"""The default `PolyFormat`."""

X = TypeVar("X", bound=ProtoVar)
"""A type over the instances of which a `PolyModular` variable can have values."""


@dataclass(frozen=True)
class PolyModular(BasePoly, metaclass=MetaPoly):
    """
    Univariate modular polynomials are constructed from a modulus and a list of modular coefficients.

    Calling `PolyModular[m]` returns a subclass with the `modulus` class variable set. Such a subclass takes
    a single list argument `coeffs` to construct a modular polynomial.

    When the subclass is created, `elliptic.mod.isprime()` is called on the modulus: if it returns `False`,
    then `ValueError` is raised.

    Insignificant zeros in `coeffs` will be ignored:

    >>> P = PolyModular[2]
    >>> P([P.M(0), P.M(0), P.M(0)]).coeffs
    [Modular[2](0)]
    >>> P([P.M(0), P.M(1), P.M(0)]).coeffs
    [Modular[2](0), Modular[2](1)]
    """

    coeffs: list[Modular]
    """The coefficients of the polynomial, in little-endian order."""

    format: ClassVar[PolyFormat] = DefaultFormat
    """The format used to print and parse polynomials."""

    def __post_init__(self) -> None:
        if not getattr(self, "modulus", None):
            raise TypeError(f"modulus is required, use {self.__class__.__qualname__}[modulus]")
        if not isinstance(self.coeffs, list):
            raise TypeError(f"{self.__class__.__qualname__} coefficients must be passed as list")
        if self.dim == 0:
            object.__setattr__(self, "coeffs", [self.M.zero()])
        if not (ranks := [i for i, c in enumerate(self.coeffs) if c != 0]):
            # Strip the zero polynomial down to a single coeff
            object.__setattr__(self, "coeffs", self.coeffs[:1])
        elif (dim := ranks[-1]) != self.dim:
            # Strip leading zero coeffs from a nonzero polynomial
            object.__setattr__(self, "coeffs", self.coeffs[: dim + 1])

    def __hash__(self) -> int:
        return hash((self.modulus, tuple(self.coeffs), self.format))

    @classmethod
    def zero(cls) -> Self:
        """
        Return the polynomial equal to zero.
        """
        return cls([cls.M.zero()])

    @classmethod
    def one(cls) -> Self:
        """
        Return the polynomial equal to one.
        """
        return cls([cls.M.one()])

    @classmethod
    def from_coeffs(cls, *coeffs: Modular) -> Self:
        """
        Construct a polynomial from any number of coefficients.

        Coefficients are assumed little-endian (lowest degree first).
        """
        return cls(list(coeffs))

    @classmethod
    def from_roots(cls, *roots: Modular) -> Self:
        """
        Construct a polynomial from any number of roots.

        If no root is provided, then this is the same as calling `one()`.
        """
        if not roots:
            return cls.one()
        (root, *others) = roots
        return cls([-root, cls.M.one()]) * cls.from_roots(*others)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Construct a polynomial parsed from a string.

        The string must match the `format` of the polynomial class.
        """
        return cls([cls.M(coeff) for coeff in cls.format.parse_coeffs(string)])

    @classmethod
    def random(cls, deg: int) -> Self:
        """
        Construct a random polynomial of degree lower than `deg`.
        """
        if deg < 0:
            raise ValueError(f"invalid degree {deg}")
        return cls([cls.M.random() for _ in range(deg)])

    @property
    def dim(self) -> int:
        """
        The dimension of the polynomial.

        This is the number of coefficients (ignoring insignificant zeros).
        """
        return len(self.coeffs)

    @property
    def deg(self) -> int:
        """
        The degree of the polynomial.

        Its value is one less than `dim` unless the polynomial is zero, in which case the degree is -1 by
        convention.
        """
        if self == 0:
            return -1
        return self.dim - 1

    @property
    def nonzero(self) -> Modular | None:
        """
        The lowest non-zero coefficient if it exists, `None` otherwise.
        """
        for coeff in self.coeffs:
            if coeff != 0:
                return coeff
        return None

    @property
    def leading(self) -> Modular | None:
        """
        The highest non-zero coefficient if it exists, `None` otherwise.
        """
        for coeff in reversed(self.coeffs):
            if coeff != 0:
                return coeff
        return None

    @property
    def derivative(self) -> Self:
        """
        The derivative of the polynomial.
        """
        if self.deg < 1:
            return self.zero()
        return type(self)([i * coeff for i, coeff in enumerate(self.coeffs) if i > 0])

    @property
    def monic(self) -> Self:
        """
        The monic version of the polynomial.

        That is the polynomial multiplied by the inverse of its leading coefficient.
        """
        if not self.leading:
            return self
        return self.leading.inverse @ self

    def is_single(self) -> bool:
        """
        Return `True` if the polynomial has a single nonzero coefficient, `False` otherwise.
        """
        return any(more := iter(c != 0 for c in self.coeffs)) and not any(more)

    def of(self, value: X) -> X:
        """
        Return the result of applying the polynomial to *value*.

        The element passed as value must implement `__rmul__()` for `elliptic.mod.Modular` objects.
        """
        total: X = value - value
        for i, coeff in enumerate(self.coeffs):
            total += (value**i).__rmul__(coeff)
        return total

    def gcd(self, *others: Self) -> Self:
        """
        Return the greatest common divisor of the polynomial and *others*.

        The result is not normalized and not necessarily monic.
        """
        if not others:
            return self
        [other, *more] = others
        if more:
            return self.gcd(other).gcd(*more)
        if not (self and other):
            return self or other
        if self == other:
            return self
        if self > other:
            return other.gcd(self % other)
        return self.gcd(other % self)

    def sff(self) -> dict[Self, int]:
        """
        Return the square-free factors of the polynomial with their exponents.

        A polynomial is square-free when it is not divisible by the square of any non-constant polynomial.
        Equivalently, it is square-free when it is coprime with its own derivative.

        The returned dictionary is indexed by the square-free factors of the polynomial and its values are
        the corresponding exponents.
        """
        if self.deg < 1:
            return {} if self == self.one() else {self: 1}

        # Yun's algorithm
        facts: dict[Self, int] = {}
        mult = self.gcd(self.derivative).monic  # The GCD with its own derivative contains the multiple roots
        bare = self // mult  # Remove all factors whose multiplicity is divisible by modulus
        i = 1  # Multiplicity of the remaining factors will have to be restored
        while bare.deg > 0 or bare.nonzero != 1:  # Find all bare factors
            common = bare.gcd(mult).monic
            fact, bare = bare // common, common  # Extract a factor
            if fact != 1:  # if the factor is non-trivial
                facts |= {fact: i}
            mult //= common  # Remove the common factors
            i += 1
        if mult.deg > 0 or mult.nonzero != 1:  # The remaining factors have multiplicity divisible by modulus
            subst = [mult.coeffs[i] for i in range(mult.modulus, mult.dim, mult.modulus)]
            mult = mult.from_coeffs(mult.coeffs[0], *subst)  # Substitute X for X**(1/modulus)
            facts |= {f: e * f.modulus for f, e in mult.sff().items()}  # Find remaining factors by recursion
        return facts

    def ddf(self) -> dict[int, Self]:
        """
        Return the distinct-degree factors of the polynomial with their irreducible degree.

        The polynomial must be square-free. The returned dictionary `{d: f, ...}` is a
        factorization of the polynomial such that each factor *f* is a product of monic, irreducible
        polynomials of equal degree *d*.
        """
        if self.leading and self.leading != 1:
            r = {0: type(self)([self.leading])}
            self = self.monic
        else:
            r = {}

        # Gauss' algorithm
        i = 1
        while self.deg > 2 * i - 1:  # Find all distinct-degree factors
            # Gauss' lemma: the product of all monic irreducible
            # polynomials whose degree divides i is:        X**(self.modulus**i) - X
            gauss = PolyModular[self.modulus].from_string(f"X**{self.modulus**i} - X")
            fact = type(self)(gauss.gcd(self).coeffs).monic  # Extract a factor
            if fact != 1:  # if the factor is non-trivial
                r |= {i: fact}
                self //= fact
            i += 1
        if self != 1:  # The remaining part is irreducible
            r |= {self.deg: self}
        return r or {1: self}

    def edf(self, d: int) -> list[Self]:
        """
        Return the equal-degree factors of the polynomial.

        The polynomial must be a monic, square-free product of equal-degree irreducible factors.
        """
        if d == 0:
            return [self]
        nfacts, zero = divmod(self.deg, d)
        assert zero == 0, "EDF requires an equal-degree product"
        assert nfacts > 1, "EDF requires at least two factors"

        # Cantor–Zassenhaus algorithm
        facts = [self]
        while len(facts) < nfacts:  # Find all factors of degree d
            seed = self.random(self.deg).monic  # Go to Las Vegas

            # Build a polynomial g likely to contain a non-trivial factor
            if self.modulus == 2:  # if everything is a square
                guess = self.zero()
                # The trace has 1/2 probability of containing a non-trivial factor
                for _ in range(d):  # Compute the trace by repeated squaring
                    guess += seed % self
                    seed = seed**2
            else:  # if square roots of 1 can be used
                # A reducible equal-degree polynomial must share a factorof degree d with:
                #    seed**((self.modulus**d - 1) // 2) - self.one()
                guess = (seed ** ((self.modulus**d - 1) // 2) - self.one()) % self
                # For a random seed, that factor is non-trivial with more than 4/9 probability

            for reducible in [fact for fact in facts if fact.deg > d]:
                fact = reducible.gcd(guess).monic  # Extract a factor
                if fact != 1 and fact != reducible:  # if the factor is non-trivial
                    facts.remove(reducible)
                    facts += [fact, reducible // fact]
        return facts

    def factors(self) -> dict[Self, int]:
        """
        Return the irreducible factors of the polynomial with their exponents.
        """
        return {
            factor: exponent
            for squarefree, exponent in self.sff().items()
            for deg, equaldeg in squarefree.ddf().items()
            for factor in (equaldeg.monic.edf(deg) if deg < equaldeg.deg else [equaldeg])
        }

    def sqrt(self) -> Self | None:
        """
        Return the square root of the polynomial, or `None` if none exist.
        """
        if not (lead := self.leading):
            return self
        if (coeff := lead.sqrt()) is None:
            return None
        fact = self.factors()
        if any(exp != 1 and exp % 2 == 1 for exp in fact.values()):
            return None
        root = self.one()
        for f, exp in fact.items():
            root *= f ** (exp // 2)
        return coeff @ root

    def __str__(self) -> str:
        return self.format.poly_str(self.coeffs)

    def __bool__(self) -> bool:
        return self != 0

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return type(self)([-x for x in self.coeffs])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return all(c == 0 for c in self.coeffs) and other == 0 or self.coeffs == [self.M.one()] and other == 1
        return isinstance(other, PolyModular) and (self.modulus, self.coeffs) == (other.modulus, other.coeffs)

    def __abs__(self) -> int:
        if self == 0:
            return 0
        return sum(int(c * (-1) ** (self.deg - i)) * self.modulus**i for i, c in enumerate(self.coeffs))

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, PolyModular):
            return NotImplemented
        if self.zero() or self.deg < other.deg:
            return False
        if other.zero() or self.deg > other.deg:
            return True
        for i in range(self.dim):
            if self.coeffs[-1 - i] == other.coeffs[-1 - i]:
                continue
            return bool((-1) ** i * self.coeffs[-1 - i] > (-1) ** i * other.coeffs[-1 - i])
        return False

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, PolyModular):
            return NotImplemented
        return self == other or self > other

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PolyModular):
            return NotImplemented
        return not self >= other

    def __le__(self, other: object) -> bool:
        if not isinstance(other, PolyModular):
            return NotImplemented
        return not self > other

    def __lshift__(self, other: object) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        if other < 0:
            return self >> -other
        return type(self)([self.M.zero() for _ in range(0, other)] + self.coeffs)

    def __rshift__(self, other: object) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        if other < 0:
            return self << -other
        return type(self)(self.coeffs[other:])

    def __add__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        return type(self)([s + o for s, o in zip_longest(self.coeffs, other.coeffs, fillvalue=self.M.zero())])

    def __sub__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        return type(self)([s - o for s, o in zip_longest(self.coeffs, other.coeffs, fillvalue=self.M.zero())])

    def __rmatmul__(self, other: object) -> Self:
        if not isinstance(other, self.M):
            return NotImplemented
        if self == 0 or other == 0:
            return self.zero()
        return type(self)([other * s for s in self.coeffs])

    def __mul__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        if self.deg < 1:
            return type(self)([self.coeffs[0] * o for o in other.coeffs])
        if other.deg < 1:
            return type(self)([s * other.coeffs[0] for s in self.coeffs])
        if self.is_single():
            return type(self)([self.coeffs[-1] * o for o in other.coeffs]) << self.deg
        if other.is_single():
            return (other.coeffs[-1] @ self) << other.deg

        # Divide and conquer
        half = max(self.dim, other.dim) // 2
        s_low = type(self)(self.coeffs[:half])
        s_high = type(self)(self.coeffs[half:])
        o_low = type(self)(other.coeffs[:half])
        o_high = type(self)(other.coeffs[half:])
        low = s_low * o_low
        high = s_high * o_high
        # Factorize the middle part to compute it with a single multiplication
        mid = (s_low + s_high) * (o_low + o_high) - low - high
        return (high << 2 * half) + (mid << half) + low

    def __rmul__(self, other: object) -> Self:
        return other @ self

    def __divmod__(self, other: object) -> tuple[Self, Self]:
        if not isinstance(other, PolyModular):
            return NotImplemented
        if other == 0:
            raise ZeroDivisionError("division by zero")

        # Euclidian division
        quotient, remainder = self.zero(), self
        while remainder.deg >= other.deg:
            term = type(self)([remainder.coeffs[-1] / other.coeffs[-1]]) << remainder.deg - other.deg
            quotient += term
            remainder -= term * other
        return (quotient, remainder)

    def __floordiv__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        (q, _) = divmod(self, other)
        return q

    def __mod__(self, other: object) -> Self:
        if not isinstance(other, PolyModular):
            return NotImplemented
        (_, r) = divmod(self, other)
        return r

    def __pow__(self, other: int, _: None = None) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        if other < 0:
            raise ValueError(f"unsupported expononent for polynomial: {other}")
        if other == 0:
            return self.one()
        if other == 1:
            return self
        return self * self.__pow__(other - 1)
