# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

"""
This module defines modular integer fields.

## Introduction

Conceptually, a modular integer is an equivalence class of the congruence relation over all integers. Two
integers *x* and *y* are congruent modulo *n* when there is an integer *k* such that:

> *x* = *k* * *n* + *y*

Modular integers have a unique multiplicative inverse if and only if their modulus *n* is a prime number, in
which case they form a finite field of order *n*.

Modular integers are implemented by the `Modular` class. The field of integers modulo *p* can be constructed
as `Modular[p]` if *p* is a prime number. Members of the field are instantiated from an integer value:

>>> M = Modular[5]  # The field of integers modulo 5
>>> M(3) == M(8) == M(-2)
True

## Structure

The integers modulo a prime number *p* form a field, so `Modular` implements the `elliptic.abc.FiniteField`
interface. Since they behave as regular integers, `Modular` also subclasses `numbers.Integral`.

>>> print(*(cls.__name__ for cls in M.__bases__))
Modular BaseModular FiniteField Integral

Addition and substraction modulo *p* define the operations `+` and `-`:

>>> print(M(1) + M(2))
3
>>> print(M(1) + M(4))
0
>>> print(M(1) - M(2))
4
>>> print(M(-1))
4

Multiplication is also defined modulo *p* which, being a prime number, allows for computing the inverse of a
field element using Fermat's little theorem:

>>> print(M(2) * M(4))
3
>>> print(M(3).inverse)
2
>>> print(M(2) / M(3))
4

## Interface

Modular integers support comparison with integers and are fully ordered.

>>> M(5) == 0 == M(0)
True
>>> M(1) < M(-1)
True

Regular integer bitwise operations are implemented:

>>> print(M(1) | M(2))
3
>>> print(M(1) << M(2))
4

Basic type conversions also supported:

>>> bool(M(1)), bool(M(5))
(True, False)
>>> int(M(1)), int(M(5))
(1, 0)
>>> float(M(1)), float(M(5))
(1.0, 0.0)

Modular integers can be exponentiated to any integer power:

>>> print(M(2) ** 4)
1
>>> print(M(2) ** -1)
3
>>> print(M(2) ** M(-1))
1

"""

from abc import ABC
from dataclasses import dataclass
from elliptic.abc import FiniteField, MetaSubscript
from math import sqrt
from numbers import Integral
from random import randrange
from typing import Any, ClassVar, Final, Self, SupportsIndex


def isprime(n: int, /) -> bool:
    """
    Return `True` if *n* is prime, `False` otherwise.

    >>> isprime(-2), isprime(-1), isprime(0), isprime(1)
    (False, False, False, False)
    >>> isprime(2), isprime(3), isprime(5), isprime(7)
    (True, True, True, True)

    Implemented by trial division which has O(sqrt(*n*)) complexity (exponential).
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for i in range(1, int(sqrt(n) / 2) + 1):
        if n % (2 * i + 1) == 0:
            return False
    return True


def msqrt(n: int, mod: int, /) -> int | None:
    """
    Return the square root of *n* modulo *mod*.

    That is a positive integer *r* such that *r* < *mod* and *r*<sup>2</sup> % *mod* = *n*, or `None` if no
    such integer exists. Note that if *r* exists then -*r* is also a square root of *n* modulo *mod*. If
    *mod* is not a prime number then the behavior is undefined.

    >>> msqrt(2, 3), msqrt(2, 5)
    (None, None)
    >>> msqrt(4, 5)
    3
    >>> 3**2 % 5, (-3 % 5)**2 % 5
    (4, 4)
    >>> msqrt(2, 31)
    8
    >>> 8**2 % 31, (-8 % 31)**2 % 31
    (2, 2)

    Implemented with the Tonelli-Shanks algorithm, which has O(log(*n*)<sup>2</sup>) complexity (polynomial).
    """

    # Trivial mode
    if (bit := n % mod) in (0, 1):
        return bit
    assert mod != 2, f"{mod} must be odd"

    # Easy mode: mod+1 is divisible by 4
    if mod % 4 == 3:
        # Looking for a quadratic residue:
        #       pow(n, (mod - 1) // 2, mod) == 1              # Euler's criterion
        #       pow(n, (mod + 1) // 2, mod) == n % mod        # Multiply by n
        #       pow(n, (mod + 1) // 4, mod) == msqrt(n, mod)  # Take the square root
        guess = pow(n, (mod + 1) // 4, mod)  # if guess does not verify Euler's criterion then no square root exists
        return guess if pow(guess, 2, mod) == n % mod else None

    # Hard mode: Tonelli–Shanks algorithm
    evenlog, odd = 0, mod - 1
    while odd % 2 != 1:  # Split mod-1 into the odd part and the logarithm (base 2) of the even part
        odd //= 2
        evenlog += 1
    z = 0  # Find a quadratic nonresidue
    for z in range(2, mod + 1):
        if pow(z, (mod - 1) // 2, mod) == -1 % mod:
            break
    assert z and z != mod, "A quadratic nonresidue must exist"
    # Notice that:
    #          odd * 2**evenlog == mod - 1                            # Rebuild mod-1 from parts
    #          odd * 2**(evenlog-1) == (mod-1) // 2                   # Divide by 2
    #   pow(z, odd * 2**(evenlog-1), mod) == pow(z, (mod-1)//2, mod)  # Exponentiate z
    #   pow(z, odd * 2**(evenlog-1), mod) == -1 % mod                 # Euler's criterion
    #   pow(z, odd, mod) is a 2**(evenlog-1)'th root of -1
    c = pow(z, odd, mod)
    # Similarly:
    #   pow(n, odd, mod) is only a 2**(evenlog-1)'th root of 1 if a square root exists
    k = pow(n, odd, mod)
    max_ = evenlog
    root = pow(n, (odd + 1) // 2, mod)  # Try the square root of x * k
    while k != 1:
        # if k != 1 then find another square root of x * k where k is:
        # either equal to 1 or a 2**(evenlog-2)'th root of 1
        assert k, f"{k} must not be zero"
        i = 0  # Find the smallest i such that k is a 2**i'th root of 1
        for i in range(1, max_ + 1):
            if pow(k, 2**i, mod) == 1:
                break
        assert i, f"{max_} must not be zero"
        if i == max_:  # if k is not a 2**(max_-1)'th root of 1 then no square root exists
            return None
        b = pow(c, 2 ** (max_ - i - 1), mod)  # Define a clever factor b
        # Notice that:
        #   pow(b, 2, mod) is a 2**(i-1)'th root of -1
        c = pow(b, 2, mod)
        root = root * b % mod  # Build a new root candidate from b
        k = k * c % mod  # Update k accordingly
        max_ = i  # k is only a 2**(i-1)'th root of 1 if a square root exists
    return root


class MetaModular(MetaSubscript):
    """
    The metaclass of modular integers, allowing for creation of `Modular[modulus]` subclasses.

    >>> isinstance(Modular[2], MetaModular)
    True
    >>> issubclass(Modular[2], Modular)
    True
    """

    attr_names: ClassVar[tuple[str, ...]] = ("modulus",)
    """The name of the attribute passed as subscript: "modulus"."""

    def attrs(cls, key: Any) -> tuple[Any, ...]:
        """
        Return the *key* subscript if it is a prime number, raise `TypeError` or `ValueError` otherwise.
        """
        if not isinstance(key, int):
            raise TypeError(f"invalid index type: {type(key).__name__}")
        if not isprime(key):
            raise ValueError(f"modulus {key} is not prime")
        return (key,)


class MetaModularP(MetaModular):
    """
    This version of the `MetaModular` metaclass does not check the modulus for primality.
    """

    def attrs(cls, key: Any) -> tuple[Any, ...]:
        """
        Return the *key* subscript if it is an integer, raise `TypeError` otherwise.
        """
        if not isinstance(key, int):
            raise TypeError(f"invalid index type: {type(key).__name__}")
        return (key,)


class BaseModular(ABC):
    """
    The abstract base class of modular classes.

    Classes dealing with modular integers should inherit the `modulus` class variable from `BaseModular` and
    declare `MetaModular` (or any approriate subclass thereof) as metaclass. From then on, specific versions
    of the class may be instantiated by indexing the class with a modulus value:

    >>> class MyModular(BaseModular, metaclass=MetaModular):
    ...     @classmethod
    ...     def print_modulus(cls):
    ...         print(f"modulus: {cls.modulus}")
    ...
    >>> MyModular[2].print_modulus()
    modulus: 2
    """

    modulus: Final[int] = 0
    """The modulus of the class. Must be a prime number."""


@dataclass(frozen=True)
class Modular(BaseModular, FiniteField, Integral, metaclass=MetaModular):
    """
    Modular integers are constructed from a prime modulus and an integer value.

    Calling `Modular[m]` returns a subclass with the `modulus` class variable set. Such a subclass takes a
    single integer argument `value` to construct a modular integer.

    When the subclass is created, `isprime()` is called on the modulus: if it returns `False`,
    then `ValueError` is raised. To bypass this check, use `ModularP` instead.
    """

    value: int
    """The original integer value of the modular."""

    def __post_init__(self) -> None:
        if not getattr(self, "modulus", None):
            raise TypeError(f"modulus is required, use {self.__class__.__qualname__}[modulus]")
        if not isinstance(self.value, int):
            raise ValueError(f"invalid integer: {self.value}")

    @classmethod
    def zero(cls) -> Self:
        return cls(0)

    @classmethod
    def one(cls) -> Self:
        return cls(1)

    @classmethod
    def order(cls) -> int:
        return cls.modulus

    @classmethod
    def random(cls) -> Self:
        """
        Return a random modular integer.
        """
        return cls(randrange(cls.modulus))

    def __hash__(self) -> int:
        return hash((int(self), self.modulus))

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}[{self.modulus}]({self.value})"

    def __str__(self) -> str:
        return str(int(self))

    def __index__(self) -> int:
        return self.value % self.modulus

    def __int__(self) -> int:
        return self.value % self.modulus

    def __float__(self) -> float:
        return float(int(self))

    def __bool__(self) -> bool:
        return bool(int(self))

    def __round__(self, _: SupportsIndex | None = None) -> Any:
        return self

    def __trunc__(self) -> int:
        return int(self)

    def __floor__(self) -> int:
        return int(self)

    def __ceil__(self) -> int:
        return int(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, float):
            return float(self) == other
        if isinstance(other, int) or isinstance(other, Modular) and self.modulus == other.modulus:
            return int(self) == int(other)
        return not self and not other

    def __gt__(self, other: object) -> bool:
        if isinstance(other, (Modular, int)):
            return int(self) > int(other)
        if not isinstance(other, float):
            return NotImplemented
        return int(self) > other

    def __ge__(self, other: object) -> bool:
        if isinstance(other, (Modular, int)):
            return int(self) >= int(other)
        if not isinstance(other, float):
            return NotImplemented
        return int(self) >= other

    def __lt__(self, other: object) -> bool:
        if isinstance(other, (Modular, int)):
            return int(self) < int(other)
        if not isinstance(other, float):
            return NotImplemented
        return int(self) < other

    def __le__(self, other: object) -> bool:
        if isinstance(other, (Modular, int)):
            return int(self) <= int(other)
        if not isinstance(other, float):
            return NotImplemented
        return int(self) <= other

    def __abs__(self) -> Self:
        return self

    def __pos__(self) -> Self:
        return self

    def __neg__(self) -> Self:
        return type(self)(-int(self) % self.modulus)

    def __lshift__(self, other: object) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return type(self)(int(self) << int(other))

    def __rlshift__(self, other: object) -> int | Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return other << int(self)

    def __rshift__(self, other: object) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return type(self)(int(self) >> int(other))

    def __rrshift__(self, other: object) -> int | Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return other >> int(self)

    def __and__(self, other: object) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return type(self)(int(self) & int(other))

    def __rand__(self, other: object) -> int | Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return other & int(self)

    def __or__(self, other: object) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return type(self)(int(self) | int(other))

    def __ror__(self, other: object) -> int | Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return other | int(self)

    def __xor__(self, other: object) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return type(self)(int(self) ^ int(other))

    def __rxor__(self, other: object) -> int | Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        return other ^ int(self)

    def __invert__(self) -> Self:
        return type(self)(~int(self))

    def _operand(self, other: object, /) -> Self | None:
        if isinstance(other, int):
            return type(self)(int(other))
        if isinstance(other, Modular) and (int(other) in (0, 1) or self.modulus == other.modulus):
            return type(self)(int(other))
        return None

    def __add__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return type(self)((int(self) + int(o)) % self.modulus)

    def __radd__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return self + o

    def __sub__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return type(self)((int(self) - int(o)) % self.modulus)

    def __rsub__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return -self + o

    def __mul__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return type(self)((int(self) * int(o)) % self.modulus)

    def __rmul__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return self * o

    @property
    def inverse(self) -> Self:
        if int(self) == 0:
            raise ZeroDivisionError(f"division by zero modulo {self.modulus}")
        return self ** (self.modulus - 2)  # Le petit théorème de Fermat

    def __truediv__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        return self * o.inverse

    def __rtruediv__(self, other: object) -> Self:
        return self.inverse * other

    def __divmod__(self, other: object) -> tuple[Self, Self]:
        if (o := self._operand(other)) is None:
            return NotImplemented
        (quotient, remainder) = divmod(int(self), int(o))
        return (type(self)(quotient), type(self)(remainder))

    def __floordiv__(self, other: object) -> int:
        if (o := self._operand(other)) is None:
            return NotImplemented
        (quotient, _) = divmod(self, o)
        return int(quotient)

    def __rfloordiv__(self, other: object) -> int:
        if not isinstance(other, float):
            return NotImplemented
        return int(other // int(self))

    def __mod__(self, other: object) -> Self:
        if (o := self._operand(other)) is None:
            return NotImplemented
        (_, remainder) = divmod(self, o)
        return remainder

    def __rmod__(self, other: object) -> float:
        if not isinstance(other, float):
            return NotImplemented
        return other % int(self)

    def __pow__(self, other: int, _: None = None) -> Self:
        if not isinstance(other, (int, type(self))):
            return NotImplemented
        if other == 0:
            return self.one()
        if other < 0:
            if self == 0:
                raise ZeroDivisionError(f"division by zero modulo {self.modulus}")
            return self.inverse**-other
        if other % 2:
            return self * self ** (other - 1)
        root = self ** (other // 2)
        return root * root

    def __rpow__(self, other: object) -> complex:
        if not isinstance(other, complex):
            return NotImplemented
        return other ** int(self)

    def sqrt(self) -> Self | None:
        """
        Return a square root of the modular integer, or `None` if none exists.
        """
        return None if (root := msqrt(int(self), self.modulus)) is None else type(self)(root)


class ModularP(Modular, metaclass=MetaModularP):
    """
    This version of the `Modular` class does not check the modulus for primality.

    Keep in mind that the behavior of division is undefined when the modulus is not prime.
    """

    pass
