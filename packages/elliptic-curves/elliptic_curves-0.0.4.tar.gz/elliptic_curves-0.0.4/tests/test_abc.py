from elliptic.abc import MetaSubscript
from typing import Any
from unittest import TestCase


class Meta(MetaSubscript):
    attr_names: tuple[str] = ("attr",)

    def attrs(cls, key: Any) -> tuple[Any, ...]:
        return (key,)


class BaseA:
    attr: Any


class A(BaseA, metaclass=Meta):
    pass


class BaseB(BaseA):
    pass


class B(BaseB, metaclass=Meta):
    pass


class TestMeta(TestCase):
    def test_equal(self) -> None:
        self.assertEqual(A, A)
        self.assertNotEqual(A["foo"], A)
        self.assertEqual(A["foo"], A["foo"])
        self.assertNotEqual(A["foo"], A["bar"])
        self.assertNotEqual(A, B)
        self.assertNotEqual(A["foo"], B["foo"])

    def test_subclass(self) -> None:
        self.assertTrue(issubclass(A, A))
        self.assertTrue(issubclass(A["foo"], A))
        self.assertTrue(issubclass(A["foo"], A["foo"]))
        self.assertFalse(issubclass(A["foo"], A["bar"]))
        self.assertFalse(issubclass(B, A))
        self.assertFalse(issubclass(B["foo"], A))
        self.assertFalse(issubclass(B["foo"], A["foo"]))
