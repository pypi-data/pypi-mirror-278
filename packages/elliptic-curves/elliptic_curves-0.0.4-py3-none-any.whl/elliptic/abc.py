# Copyright (C) 2023-2024 Nicolas Canceill
# This file is part of the `elliptic` package
# GNU General Public License v3.0+
# See COPYING.md or https://www.gnu.org/licenses/

"""
This module provides abstract base classes for elliptic curves.

## Introduction

Fields are specified by the `Field` interface. They act as scalars for the definition of elliptic curves.

Field implementations may be parametrized. This can be achieved with the `MetaSubscript` abstract base class.

Fields may also be used to define polynomials. Variables can be modeled by the `ProtoVar` interface.

## Numeric emulation

Fields implement operations using special methods. For more information, see section
[3.3.8. Emulating numeric types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)
of the Python documentation.

### Binary operations

Implementations of `Field` must define the `__add__()` and `__mul__()` numeric methods for the `+` and `*`
operations, along with the `__radd__()` and `__rmul__()` reverse methods. Since the two operations form group
structures, the `-` and `/` inverse operations must be defined as `__sub__()` and `__truediv__()` along
with their reverse counterparts. Dividing by zero should raise `ZeroDivisionError`.

### Unary operations

Fields must also define the `__pos__()` and `__neg__()` methods for unary operations. Since multiplication
forms a group, an `inverse()` method must be defined as well and should raise `ZeroDivisionError` when called
on the "zero" element.

### Exponentiation

The `__pow__()` method should be defined by multiplying an element (or its inverse in case of a negative
exponent) by itself as many times as required. When the exponent is zero, the "one" element should be
returned.

There is no need to support the third argument of `pow()` as it may not always make sense. Similarly,
implementations may return `NotImplemented` if the exponent is not an integer.

## Implementation notes

All the aforementioned methods return `Self` to show that the operations are closures of the field. This has
the downside of forcing cumbersome wrapping around those methods when building a field out of a class with
incompatible signatures.

Implementations must define the `__eq__()` method to provide a meaningful comparison between two field
elements. Additionally, that method should return `True` if the neutral elements of addition and
multiplication are compared to literals `0` and `1` respectively. This allows for simple comparison using
`==` without having to access the `Field.zero()` and `Field.one()` class methods.

Fields should also provide an ordering of their elements. The ordering relation should be transitive.

Field elements should be immutable. Implementing the `__hash__()` method is advised.

## Finite fields

The abstract subclass `FiniteField` can be used for fields with a finite number of elements, such as modular
integers. Implementations must define the `FiniteField.order` class method to return the number of elements.

The `FiniteField.ord` and `FiniteField.primitive` properties are defined for each element according to the
field's multiplicative group. They may be overwritten by implementations, for example to cache the results.

Finite fields can benefit from class parametrization, dynamically subclassing a generic implementation for
every value of the field order. For example, it makes sense for the field of integers modulo a prime number
`p` to be a dynamic subclass of a generic modular integer implementation. That may be achieved with the
`MetaSubscript` metaclass.
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Protocol, Self, TypeVar


class Field(ABC):
    """
    The abstract class representing a field.
    """

    @classmethod
    @abstractmethod
    def zero(cls) -> Self:
        """
        Return the neutral element of the additive group.
        """
        ...

    @classmethod
    @abstractmethod
    def one(cls) -> Self:
        """
        Return the neutral element of the multiplicative group.
        """
        ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __pos__(self) -> Self:
        ...

    @abstractmethod
    def __neg__(self) -> Self:
        ...

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __sub__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __mul__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __rmul__(self, other: int) -> Self:
        ...

    @property
    @abstractmethod
    def inverse(self) -> Self:
        """
        The multiplicative inverse of the field element.
        """
        ...

    @abstractmethod
    def __truediv__(self, other: Self) -> Self:
        ...

    @abstractmethod
    def __pow__(self, other: int, _: None = None) -> Self:
        ...


class FiniteField(Field):
    """
    The abstract class representing a finite field.

    The simplest finite fields have a prime number of elements and are implemented as modular integers. They
    can be extended to include all fields with a prime power number of elements.
    """

    @classmethod
    @abstractmethod
    def order(cls) -> int:
        """
        Return the number of elements in the field.
        """
        ...

    @property
    def ord(self) -> int:
        """
        The multiplicative order of the field element.

        The order is the highest exponent (up to the order of the field) to which the element can be
        raised before the result is one. If it is equal to `order() - 1` then the element is `primitive`.
        """
        if self == 0:
            return 0
        order = 1
        value = self
        while value != 1:
            order += 1
            value *= self
        return order

    @property
    def primitive(self) -> bool:
        """
        Whether the field element is a primitive root of one.

        Every element `x` of a finite field of order `q` is a `q-1`th root of one. It is a primitive root of
        one when there is no  integer `i < q - 1` such that `x ** i == 1`.
        """
        return self.ord == self.order() - 1


class MetaSubscript(ABCMeta):
    """
    The abstract metaclass of subcriptable classes.

    Implementations of this class can parametrize their instances with subscripts in order to set values for
    the class attributes of their instances.

    Note that using class subscripts for any purpose other than type hinting is implicitly discouraged by the
    official Python documentation. However, it provides a convenient way to parametrize classes at runtime
    with non-type values, such as the characteristic of a modular field or the dimension of a vector.

    >>> class Meta(MetaSubscript):
    ...     attr_names = "foo",
    ...
    ...     def attrs(cls, sub):
    ...         return sub,
    ...
    >>> class Demo(metaclass=Meta):
    ...     foo = "bar"
    ...
    >>> Demo["baz"].foo
    'baz'
    >>> Demo[0, 1].foo
    (0, 1)
    >>> Demo.foo
    'bar'

    This currently seems to be supported by `mypy` but requires explicit typing when using type variables:

    >>> D: type[Demo] = Demo["baz"]  # Fine
    >>> d = Demo["baz"]()            # Also fine
    >>> D = Demo["baz"]              # Raises mypy [valid-type] error
    """

    _Self = TypeVar("_Self", bound="MetaSubscript")  # PEP 673 does not allow `Self` in metaclasses

    @property
    @abstractmethod
    def attr_names(cls) -> tuple[str, ...]:
        """
        The names of the attributes passed as subscript.

        These attributes should be defined as class variables in the instances of the implementing metaclass.
        """
        ...

    @abstractmethod
    def attrs(cls, _: Any) -> tuple[Any, ...]:
        """
        Return the values of the attributes from the subcript.

        Implementations should take as argument whatever object they intend to accept for subscripting to the
        class and return a tuple of values with the same length as `attr_names`.

        The sole argument is the key passed to `__getitem__()`. Note that if the subscript includes a comma,
        then Python passes it as a `tuple` object.
        """
        ...

    def _bases(cls) -> tuple[type, ...]:
        return cls.__bases__ if cls in cls.__bases__ else (cls, *cls.__bases__)

    def _dict(cls, key: Any) -> dict[str, Any]:
        attrs = cls.attrs(key)
        assert len(cls.attr_names) == len(attrs)
        return dict(cls.__dict__) | {k: v for k, v in zip(cls.attr_names, attrs)}

    def __getitem__(cls: _Self, key: Any) -> _Self:
        new = type(cls.__qualname__, cls._bases(), cls._dict(key))
        assert isinstance(new, type(cls))
        return new

    def __eq__(cls, other: object) -> bool:
        if not isinstance(other, type) or cls.__bases__ != other.__bases__:
            return super().__eq__(other)
        return all(getattr(cls, attr, None) == getattr(other, attr, None) for attr in cls.attr_names)

    def __hash__(cls) -> int:
        return hash((cls.__qualname__, cls.__bases__, (getattr(cls, attr, None) for attr in cls.attr_names)))

    def __instancecheck__(cls, instance: Any) -> bool:
        return super().__instancecheck__(instance) or issubclass(type(instance), cls)

    def __subclasscheck__(cls, subclass: type) -> bool:
        if super().__subclasscheck__(subclass):
            return True
        if not isinstance(subclass, type(cls)) or not all(base in subclass.__bases__ for base in cls.__bases__):
            return False
        try:
            return all(getattr(cls, name) == getattr(subclass, name) for name in cls.attr_names)
        except AttributeError:
            return False


class ProtoVar(Protocol):
    """
    A protocol describing a polynomial variable.

    It requires `__add__()` so terms can be summed, `__sub__()` in order to determine zero, `__mul__()` and
    `__pow__()` so it can be exponentiated, and `__rmul__()` so it can be multiplied by coefficients.
    """

    def __add__(self, other: Self, /) -> Self:
        ...

    def __sub__(self, other: Self, /) -> Self:
        ...

    def __mul__(self, other: Self, /) -> Self:
        ...

    def __rmul__(self, other: Any, /) -> Self:
        ...

    def __pow__(self, other: int, _: None = None) -> Self:
        ...
