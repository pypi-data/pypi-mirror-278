from decimal import Context, Decimal
from elliptic.inf import Rational, Real
from unittest import TestCase


class TestRational(TestCase):
    def test_init(self) -> None:
        r = Rational(3)
        self.assertEqual(r.numerator, 3)
        self.assertEqual(r.denominator, 1)
        r = Rational(2, 3)
        self.assertEqual(r.numerator, 2)
        self.assertEqual(r.denominator, 3)
        with self.assertRaises(ZeroDivisionError):
            Rational(1, 0)

    def test_eq(self) -> None:
        self.assertEqual(Rational("0"), 0)
        self.assertEqual(Rational("1"), 1)

    def test_add(self) -> None:
        self.assertEqual(Rational(1, 2) + Rational(3, 4), Rational(5, 4))
        self.assertEqual(Rational(1, 2) + Rational(-1, 2), Rational(0))
        self.assertEqual(Rational(1, 2) - Rational(1, 2), Rational(0))

    def test_mul(self) -> None:
        self.assertEqual(Rational(1, 2) * Rational(3, 4), Rational(3, 8))
        self.assertEqual(Rational(1, 2) / Rational(2, 4), Rational(1))


class TestReal(TestCase):
    def test_init(self) -> None:
        r = Real("1.234")
        self.assertEqual(r.value, Decimal("1.234"))
        c = Context(prec=2)
        r = Real("1.234", context=c)
        self.assertEqual(r.value, Decimal("1.234"))

    def test_eq(self) -> None:
        self.assertEqual(Real("0"), 0)
        self.assertEqual(Real("1"), 1)

    def test_add(self) -> None:
        self.assertEqual(Real("1.2") + Real("4.3"), Real("5.5"))
        self.assertEqual(Real("1.23") + Real("-1.23"), Real("0"))
        self.assertEqual(Real("1.23") - Real("1.23"), Real("0"))

    def test_mul(self) -> None:
        self.assertEqual(Real("1.2") * Real("1.2"), Real("1.44"))
        self.assertEqual(Real("1.23") / Real("1.23"), Real("1"))
