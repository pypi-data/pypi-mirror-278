from elliptic.curves import BasePoint, Curve
from elliptic.inf import Real
from elliptic.mod import Modular
from typing import Any
from unittest import TestCase


class TestProjectivePoint(TestCase):
    infinities: list[BasePoint[Any]] = [
        BasePoint(Real(0), Real(1), Real(0)),
        BasePoint(Modular[5](5), Modular[5](1), Modular[5](0)),
    ]

    def test_str(self) -> None:
        M: type[Modular] = Modular[3]
        self.assertEqual(str(BasePoint(M(1), M(0))), "(1, 0)")
        self.assertEqual(str(BasePoint(M(0), M(1), M(0))), "(0, 1, 0)")

    def test_origin(self) -> None:
        with self.assertRaises(ValueError):
            BasePoint(Real(0), Real(0), Real(0))
        with self.assertRaises(ValueError):
            BasePoint(Modular[5](0), Modular[5](5), Modular[5](0))

    def test_infinity(self) -> None:
        for infinity in self.infinities:
            self.assertTrue(infinity.is_inf())
        self.assertFalse(BasePoint(Real(0), Real(1), Real(2)).is_inf())
        self.assertFalse(BasePoint(Modular[5](0), Modular[5](1), Modular[5](2)).is_inf())

    def test_homogeneous(self) -> None:
        with self.subTest("real"):
            p = BasePoint(Real(0), Real(1), Real(2))
            self.assertEqual((p.x, p.y), (Real(0), Real("0.5")))
            p = BasePoint(Real(0), Real(1))
            self.assertEqual((p.x, p.y), (Real(0), Real(1)))
        with self.subTest("modular"):
            q = BasePoint(Modular[5](0), Modular[5](1), Modular[5](2))
            self.assertEqual((q.x, q.y), (0, 3))
            q = BasePoint(Modular[5](0), Modular[5](1))
            self.assertEqual((q.x, q.y), (0, 1))

    def test_homogeneous_infinity(self) -> None:
        for infinity in self.infinities:
            with self.assertRaises(ZeroDivisionError):
                infinity.x
            with self.assertRaises(ZeroDivisionError):
                infinity.y

    def test_equal(self) -> None:
        with self.subTest("real"):
            self.assertEqual(BasePoint(Real(0), Real(1), Real(2)), BasePoint(Real(0), Real("0.5")))
            self.assertEqual(BasePoint(Real(2), Real(1), Real(2)), BasePoint(Real(1), Real("0.5")))
            self.assertNotEqual(BasePoint(Real(0), Real(1), Real(2)), BasePoint(Real(1), Real("0.5")))
            self.assertNotEqual(BasePoint(Real(0), Real(1), Real(2)), BasePoint(Real(0), Real(1)))
            self.assertEqual(BasePoint(Real(0), Real(1), Real(0)), BasePoint(Real(0), Real(2), Real(0)))
            self.assertNotEqual(BasePoint(Real(0), Real(1), Real(0)), BasePoint(Real(1), Real(2), Real(0)))
        with self.subTest("modular"):
            self.assertEqual(
                BasePoint(Modular[5](0), Modular[5](1), Modular[5](2)), BasePoint(Modular[5](0), Modular[5](3))
            )
            self.assertEqual(
                BasePoint(Modular[5](2), Modular[5](1), Modular[5](2)), BasePoint(Modular[5](1), Modular[5](3))
            )
            self.assertNotEqual(
                BasePoint(Modular[5](0), Modular[5](1), Modular[5](2)), BasePoint(Modular[5](1), Modular[5](3))
            )
            self.assertNotEqual(
                BasePoint(Modular[5](0), Modular[5](1), Modular[5](2)), BasePoint(Modular[5](0), Modular[5](1))
            )
            self.assertEqual(
                BasePoint(Modular[5](0), Modular[5](1), Modular[5](0)),
                BasePoint(Modular[5](0), Modular[5](2), Modular[5](0)),
            )
            self.assertNotEqual(
                BasePoint(Modular[5](0), Modular[5](1), Modular[5](0)),
                BasePoint(Modular[5](1), Modular[5](2), Modular[5](0)),
            )


class TestCurve(TestCase):
    a: int = -3
    b: int = 7
    modulus: int = 31
    c_real: Curve[Real]
    c_mod: Curve[Modular]
    M: type[Modular]

    def setUp(self) -> None:
        self.M = Modular[self.modulus]
        self.c_real = Curve[Real](a=Real(self.a), b=Real(self.b))
        self.c_mod = Curve[Modular](a=self.M(self.a), b=self.M(self.b))

    def test_infinity(self) -> None:
        with self.subTest("real"):
            self.assertTrue(self.c_real.infinity.is_inf())
        with self.subTest("modular"):
            self.assertTrue(self.c_mod.infinity.is_inf())

    def test_contains(self) -> None:
        with self.subTest("real"):
            self.assertFalse(self.c_real.contains(BasePoint(Real(2), Real(2))))
            self.assertTrue(self.c_real.contains(BasePoint(Real(2), Real(3.0))))
        with self.subTest("modular"):
            self.assertFalse(self.c_mod.contains(BasePoint(self.M(1), self.M(5))))
            self.assertTrue(self.c_mod.contains(BasePoint(self.M(1), self.M(6))))


class TestPoint(TestCase):
    a: int = -3
    b: int = 7
    modulus: int = 31
    c_real: Curve[Real]
    c_mod: Curve[Modular]
    M: type[Modular]

    def setUp(self) -> None:
        self.M = Modular[self.modulus]
        self.c_real = Curve[Real](a=Real(self.a), b=Real(self.b))
        self.c_mod = Curve[Modular](a=self.M(self.a), b=self.M(self.b))

    def test_eq(self) -> None:
        self.assertEqual(self.c_mod.infinity, 0)
