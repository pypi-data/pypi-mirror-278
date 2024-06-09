from elliptic.mod import Modular
from elliptic.poly import DefaultFormat, PolyModular
from unittest import TestCase


class TestMetaPoly(TestCase):
    modulus: int = 31
    modulus_other: int = 29

    def test_eq(self) -> None:
        self.assertEqual(PolyModular, PolyModular)
        self.assertEqual(PolyModular[self.modulus], PolyModular[self.modulus])
        self.assertNotEqual(PolyModular[self.modulus], PolyModular[self.modulus_other])


class TestPolyFormat(TestCase):
    modulus: int = 31
    M: type[Modular]

    def setUp(self) -> None:
        self.M = Modular[self.modulus]

    def test_parse(self) -> None:
        self.assertEqual(DefaultFormat.parse_coeffs("0"), [0])
        self.assertEqual(DefaultFormat.parse_coeffs("1"), [1])
        self.assertEqual(DefaultFormat.parse_coeffs("1 + 1"), [2])
        self.assertEqual(DefaultFormat.parse_coeffs("1 - 1"), [0])
        self.assertEqual(DefaultFormat.parse_coeffs("X + 1"), [1, 1])
        self.assertEqual(DefaultFormat.parse_coeffs("X - 1"), [-1, 1])
        self.assertEqual(DefaultFormat.parse_coeffs("3*X + 1"), [1, 3])
        self.assertEqual(DefaultFormat.parse_coeffs("-3*X + 1"), [1, -3])
        self.assertEqual(DefaultFormat.parse_coeffs("X + 1 + 2*X"), [1, 3])
        self.assertEqual(DefaultFormat.parse_coeffs("X**3 + X**2 + 1"), [1, 0, 1, 1])
        self.assertEqual(DefaultFormat.parse_coeffs("- X**3+X**2- 1"), [-1, 0, 1, -1])
        self.assertEqual(DefaultFormat.parse_coeffs("X + 2X**2"), [0, 1, 2])

    def test_str(self) -> None:
        self.assertEqual(DefaultFormat.poly_str([self.M(0)]), "0")
        self.assertEqual(DefaultFormat.poly_str([self.M(1)]), "1")
        self.assertEqual(DefaultFormat.poly_str([self.M(1), self.M(1)]), "X + 1")
        self.assertEqual(DefaultFormat.poly_str([self.M(1), self.M(3)]), "3*X + 1")
        self.assertEqual(DefaultFormat.poly_str([self.M(1), self.M(0), self.M(1), self.M(1)]), "X**3 + X**2 + 1")


class TestPolyModular(TestCase):
    modulus: int = 31
    M: type[Modular]
    P: type[PolyModular]

    def setUp(self) -> None:
        self.M = Modular[self.modulus]
        self.P = PolyModular[self.modulus]

    def test_init(self) -> None:
        _ = self.P([self.M(1)]), self.P([])
        with self.assertRaises(TypeError):
            PolyModular([self.M(1)])
        with self.assertRaises(TypeError):
            PolyModular[{"modulus": 2}]([self.M(1)])
        with self.assertRaises(ValueError):
            PolyModular[4]([self.M(1)])

    def test_zero(self) -> None:
        self.assertEqual(self.P.zero(), self.P([self.M(0)]))

    def test_one(self) -> None:
        self.assertEqual(self.P.one(), self.P([self.M(1)]))

    def test_from_roots(self) -> None:
        for i in range(self.modulus):
            root = self.M(i)
            self.assertEqual(self.P.from_string(f"X + {int(root)}"), self.P.from_roots(-root))
            self.assertEqual(self.P.from_string(f"X**2 + {int(-root**2)}"), self.P.from_roots(root, -root))
            self.assertEqual(self.P.from_string(f"X**2 + {int(-root**2)}"), self.P.from_roots(-root, root))

    def test_deg(self) -> None:
        self.assertEqual(self.P.from_string("0").deg, -1)
        self.assertEqual(self.P.from_string("3").deg, 0)
        self.assertEqual(self.P.from_string("2*X**2 + 3").deg, 2)

    def test_nonzero(self) -> None:
        self.assertEqual(self.P.from_string("0").nonzero, None)
        self.assertEqual(self.P.from_string("3").nonzero, self.M(3))
        self.assertEqual(self.P.from_string("2*X**2 + 3").nonzero, self.M(3))

    def test_leading(self) -> None:
        self.assertEqual(self.P.from_string("0").leading, None)
        self.assertEqual(self.P.from_string("3").leading, self.M(3))
        self.assertEqual(self.P.from_string("2*X**2 + 3").leading, self.M(2))

    def test_derivative(self) -> None:
        self.assertEqual(self.P.from_string("0").derivative, self.P.from_string("0"))
        self.assertEqual(self.P.from_string("3").derivative, self.P.from_string("0"))
        self.assertEqual(self.P.from_string("2*X**2 + 3").derivative, self.P.from_string("4*X"))

    def test_single(self) -> None:
        self.assertFalse(self.P.from_string("0").is_single())
        self.assertTrue(self.P.from_string("3").is_single())
        self.assertTrue(self.P.from_string("2*X**2").is_single())
        self.assertFalse(self.P.from_string("2*X**2 + 3").is_single())

    def test_bool(self) -> None:
        self.assertFalse(bool(self.P([self.M(0)])))
        self.assertTrue(bool(self.P([self.M(1)])))

    def test_eq(self) -> None:
        self.assertEqual(self.P([self.M(0)]), 0)
        self.assertEqual(self.P([self.M(0)]), self.P([self.M(0), self.M(0)]))
        self.assertNotEqual(self.P([self.M(1)]), 0)
        self.assertEqual(self.P([self.M(1)]), self.P([self.M(1), self.M(0)]))
        self.assertNotEqual(self.P([self.M(1)]), self.P([self.M(0), self.M(1)]))

    def test_order(self) -> None:
        P: type[PolyModular] = PolyModular[3]
        self.assertTrue(P.from_string("X + 2") < P.from_string("X + 1"))
        self.assertTrue(P.from_string("X**2 + 2X") < P.from_string("X**2 + X"))

    def test_of(self) -> None:
        self.assertEqual(self.P.from_string("3").of(self.M(2)), 3 % self.modulus)
        self.assertEqual(self.P.from_string("X + 3").of(self.M(2)), (2 + 3) % self.modulus)
        self.assertEqual(self.P.from_string("X**2 + 3").of(self.M(2)), (2**2 + 3) % self.modulus)
        self.assertEqual(self.P.from_string("X**3 + 3").of(self.M(2)), (2**3 + 3) % self.modulus)
        self.assertEqual(
            self.P.from_string("X**3 + 3").of(self.P.from_string("2")),
            self.P.from_string(f"{(2**3 + 3) % self.modulus}"),
        )
        self.assertEqual(
            self.P.from_string("X**2 + 3").of(self.P.from_string("X + 1")), self.P.from_string("X**2 + 2*X + 4")
        )

    def test_add(self) -> None:
        self.assertEqual(self.P.from_string("X") + self.P.from_string("1"), self.P.from_string("X + 1"))

    def test_sub(self) -> None:
        self.assertEqual(self.P.from_string("X + 2") - self.P.from_string("1"), self.P.from_string("X + 1"))

    def test_mul(self) -> None:
        self.assertEqual(self.P.from_string("X + 1") * self.P.from_string("1"), self.P.from_string("X + 1"))
        self.assertEqual(self.P.from_string("X + 1") * self.P.from_string("X"), self.P.from_string("X**2 + X"))
        self.assertEqual(
            self.P.from_string("X + 1") * self.P.from_string("X + 1"), self.P.from_string("X**2 + 2*X + 1")
        )
        self.assertEqual(
            self.P.from_string("X**9 + 2*X**6 + X**3 + 2") * self.P.from_string("X**2 + 2"),
            self.P.from_string("X**11 + 2*X**9 + 2*X**8 + 4*X**6 + X**5 + 2*X**3 + 2*X**2 + 4"),
        )

    def test_divmod(self) -> None:
        self.assertEqual(
            divmod(self.P.from_string("X**2 + 2*X + 1"), self.P.from_string("X + 1")),
            (self.P.from_string("X + 1"), self.P.zero()),
        )
        self.assertEqual(divmod(self.P.zero(), self.P.from_string("X + 1")), (self.P.zero(), self.P.zero()))

    def test_sff(self) -> None:
        P: type[PolyModular] = PolyModular[3]
        p = P.from_string("X**11 + 2*X**9 + 2*X**8 + X**6 + X**5 + 2*X**3 + 2*X**2 + 1")
        f1, f3, f4 = P.from_string("X+1"), P.from_string("X**2 + 1"), P.from_string("X+2")
        self.assertEqual(p.sff(), {f1: 1, f3: 3, f4: 4})
        self.assertEqual(p, f1 * f3**3 * f4**4)

    def test_factors(self) -> None:
        P: type[PolyModular] = PolyModular[3]
        self.assertEqual(P.zero().factors(), {P.zero(): 1})
        self.assertEqual(P.one().factors(), {})
        p1, p2 = P.from_string("X + 1"), P.from_string("X + 2")
        self.assertEqual(p1.factors(), {p1: 1})
        self.assertEqual((p1**2).factors(), {p1: 2})
        p = p1 * p2
        self.assertEqual(p.factors(), {p1: 1, p2: 1})
        q = P.M(2)
        self.assertEqual(P([q]).factors(), {P([q]): 1})
        self.assertEqual((q @ p1).factors(), {P([q]): 1, p1: 1})
        for m in [2, 3, 5, 7]:
            P = PolyModular[m]
            p = P.from_string("X**11 + 2*X**9 + 2*X**8 + X**6 + X**5 + 2*X**3 + 2*X**2 + 1")
            fs, prod = p.factors(), P.one()
            for f, e in fs.items():
                prod *= f**e
            self.assertEqual(p.monic, prod)

    def test_sqrt(self) -> None:
        P: type[PolyModular] = PolyModular[7]
        p, q = P.from_string("X**2 + 2*X + 1"), P.from_string("X + 1")
        assert p == q**2
        # In modulo 7 arithmetic, the square root of 2 is 4 and 3 has no square root
        self.assertEqual(p.sqrt(), q)
        self.assertEqual((P.M(2) @ p).sqrt(), P.M(4) @ q)
        self.assertEqual((P.M(3) @ p).sqrt(), None)
