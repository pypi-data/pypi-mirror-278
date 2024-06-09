from elliptic.mod import Modular, ModularP, isprime, msqrt
from itertools import product
from unittest import TestCase


class TestPrime(TestCase):
    primes: list[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 2**31 - 1]
    nonprimes: list[int] = [-3, -2, -1, 0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 2**29 - 1]

    def test_isprime(self) -> None:
        for n in self.primes:
            with self.subTest(n):
                self.assertTrue(isprime(n))
        for n in self.nonprimes:
            with self.subTest(n):
                self.assertFalse(isprime(n))


class TestMsqrt(TestCase):
    mods: list[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 97]

    def test_msqrt(self) -> None:
        for mod in self.mods:
            for i in range(-2 * mod, 2 * mod):
                if (root := msqrt(i, mod)) is None:
                    for n in range(0, mod):
                        self.assertNotEqual(pow(base=n, exp=2, mod=mod), i % mod)
                else:
                    self.assertEqual(pow(base=root, exp=2, mod=mod), i % mod)


class TestMetaModular(TestCase):
    modulus: int = 31
    modulus_other: int = 29

    def test_eq(self) -> None:
        self.assertEqual(Modular, Modular)
        self.assertEqual(Modular[self.modulus], Modular[self.modulus])
        self.assertNotEqual(Modular[self.modulus], Modular[self.modulus_other])


class TestModular(TestCase):
    modulus: int = 31
    modulus_other: int = 29
    M: type[Modular]

    def setUp(self) -> None:
        self.M = Modular[self.modulus]
        assert isprime(self.modulus)
        assert isprime(self.modulus_other)
        assert self.modulus != self.modulus_other

    def test_init(self) -> None:
        _ = Modular[2](1)
        with self.assertRaises(TypeError):
            Modular(1)
        with self.assertRaises(TypeError):
            Modular[{"modulus": 2}](1)
        with self.assertRaises(ValueError):
            _ = Modular[4](1)
        try:
            _ = ModularP[4](1)
        except ValueError:
            self.fail()

    def test_int(self) -> None:
        for i in range(-2 * self.modulus, 2 * self.modulus):
            self.assertEqual(int(self.M(i)), i % self.modulus)

    def test_eq(self) -> None:
        self.assertEqual(self.M(0), 0)
        self.assertEqual(self.M(0), 0.0)
        self.assertEqual(self.M(0), Modular[self.modulus_other](0))
        for i in range(-2 * self.modulus, 2 * self.modulus):
            self.assertEqual(self.M(i), i % self.modulus)
            self.assertEqual(i % self.modulus, self.M(i))
            self.assertEqual(self.M(i), float(i) % self.modulus)
            self.assertEqual(float(i) % self.modulus, self.M(i))
            self.assertEqual(self.M(i), self.M(i))
            self.assertEqual(self.M(i + self.modulus), self.M(i))
            self.assertEqual(self.M(-i), self.M(self.modulus - i))

    def test_add(self) -> None:
        self.assertTrue(isinstance(self.M(1) + 1, Modular))
        self.assertTrue(isinstance(1 + self.M(1), Modular))
        with self.assertRaises(TypeError):
            _ = self.M(2) + Modular[self.modulus_other](2)
        with self.assertRaises(TypeError):
            _ = self.M(2) + 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 + self.M(2)
        for i, j in product(r := range(-self.modulus, self.modulus), r):
            self.assertEqual(int(self.M(i) + self.M(j)), (i + j) % self.modulus)
            self.assertEqual(int(self.M(i) + j), (i + j) % self.modulus)
            self.assertEqual(int(i + self.M(j)), (i + j) % self.modulus)

    def test_sub(self) -> None:
        self.assertTrue(isinstance(self.M(1) - 1, Modular))
        self.assertTrue(isinstance(1 - self.M(1), Modular))
        with self.assertRaises(TypeError):
            _ = self.M(2) - Modular[self.modulus_other](2)
        with self.assertRaises(TypeError):
            _ = self.M(2) - 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 - self.M(2)
        for i, j in product(r := range(-self.modulus, self.modulus), r):
            self.assertEqual(int(self.M(i) - self.M(j)), (i - j) % self.modulus)
            self.assertEqual(int(self.M(i) - j), (i - j) % self.modulus)
            self.assertEqual(int(i - self.M(j)), (i - j) % self.modulus)

    def test_mul(self) -> None:
        self.assertTrue(isinstance(self.M(1) * 1, Modular))
        self.assertTrue(isinstance(1 * self.M(1), Modular))
        with self.assertRaises(TypeError):
            _ = self.M(2) * Modular[self.modulus_other](2)
        with self.assertRaises(TypeError):
            _ = self.M(2) * 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 * self.M(2)
        for i, j in product(r := range(-self.modulus, self.modulus), r):
            self.assertEqual(int(self.M(i) * self.M(j)), (i * j) % self.modulus)
            self.assertEqual(int(self.M(i) * j), (i * j) % self.modulus)
            self.assertEqual(int(i * self.M(j)), (i * j) % self.modulus)

    def test_div(self) -> None:
        self.assertTrue(isinstance(self.M(1) / 1, Modular))
        self.assertTrue(isinstance(1 / self.M(1), Modular))
        with self.assertRaises(TypeError):
            _ = self.M(2) / Modular[self.modulus_other](2)
        with self.assertRaises(TypeError):
            _ = self.M(2) / 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 / self.M(2)
        for i in range(-2 * self.modulus, 2 * self.modulus):
            if i % self.modulus == 0:
                continue
            self.assertEqual(int(self.M(i) * self.M(i).inverse), 1)
            self.assertEqual(int(self.M(i) / self.M(i)), 1)
            self.assertEqual(int(0 / self.M(i)), 0)

    def test_pow(self) -> None:
        with self.assertRaises(TypeError):
            _ = self.M(2) ** 1.2  # type: ignore
        for i in range(-2 * self.modulus, 2 * self.modulus):
            for n in range(-7, 8):
                if i % self.modulus or n > -1:
                    self.assertEqual(int(self.M(i) ** n), pow(base=i, exp=n, mod=self.modulus))

    def test_primitive(self) -> None:
        self.assertFalse(Modular[2](0).primitive)
        self.assertTrue(Modular[2](1).primitive)
        M: type[Modular] = Modular[11]
        self.assertFalse(M(0).primitive)
        self.assertFalse(M(1).primitive)
        self.assertTrue(M(2).primitive)
        self.assertFalse(M(3).primitive)
        self.assertFalse(M(4).primitive)
        self.assertFalse(M(5).primitive)
        self.assertTrue(M(6).primitive)
        self.assertTrue(M(7).primitive)
        self.assertTrue(M(8).primitive)
        self.assertFalse(M(9).primitive)
        self.assertFalse(M(10).primitive)
