from elliptic.fin import Galois, factors
from elliptic.poly import PolyModular
from itertools import combinations
from math import prod
from unittest import TestCase


class TestFactors(TestCase):
    max_exp: int = 6
    mods: list[int] = [2, 3, 5, 7]

    def test_factors(self) -> None:
        def exp_cases(max_exp: int, nfactors: int) -> list[list[int]]:
            if nfactors < 2:
                return [[i + 1] for i in range(max_exp)]
            return [prev + [i + 1] for prev in exp_cases(max_exp, nfactors - 1) for i in range(max_exp)]

        for i in range(len(self.mods)):
            all_exps = exp_cases(self.max_exp, i + 1)
            for facs in combinations(self.mods, i + 1):
                for case in [{facs[j]: exps[j] for j in range(i + 1)} for exps in all_exps]:
                    n = prod(fac**exp for fac, exp in case.items())
                    self.assertEqual(factors(n), case)


class TestMetaGalois(TestCase):
    modulus: int = 2
    modulus_other: int = 3
    degree: int = 1
    degree_other: int = 2

    def test_eq(self) -> None:
        self.assertEqual(Galois, Galois)
        self.assertEqual(Galois[self.modulus, self.degree], Galois[self.modulus, self.degree])
        self.assertNotEqual(Galois[self.modulus, self.degree], Galois[self.modulus_other, self.degree])
        self.assertNotEqual(Galois[self.modulus, self.degree], Galois[self.modulus, self.degree_other])


class TestGalois(TestCase):
    def test_eq(self) -> None:
        G: type[Galois] = Galois[2, 3]
        self.assertEqual(G.zero(), 0)
        self.assertEqual(G.one(), 1)

    def test_monics(self) -> None:
        self.assertEqual(list(Galois[3, 0].monics()), [PolyModular[3].from_string("1")])
        self.assertEqual(
            list(Galois[3, 1].monics()), [PolyModular[3].from_string(string) for string in ("X", "X + 2", "X + 1")]
        )
        self.assertEqual(
            list(Galois[3, 2].monics()),
            [
                PolyModular[3].from_string(string)
                for string in (
                    "X**2",
                    "X**2 + 1",
                    "X**2 + 2",
                    "X**2 + 2*X",
                    "X**2 + 2*X+ 1",
                    "X**2 + 2*X + 2",
                    "X**2 + X",
                    "X**2 + X+ 1",
                    "X**2 + X + 2",
                )
            ],
        )

    def test_conway(self) -> None:
        self.assertEqual(Galois[2, 1].conway(), PolyModular[2].from_string("X + 1"))
        self.assertEqual(Galois[2, 2].conway(), PolyModular[2].from_string("X**2 + X + 1"))
        self.assertEqual(Galois[2, 3].conway(), PolyModular[2].from_string("X**3 + X + 1"))
        self.assertEqual(Galois[2, 4].conway(), PolyModular[2].from_string("X**4 + X + 1"))
        self.assertEqual(Galois[2, 5].conway(), PolyModular[2].from_string("X**5 + X**2 + 1"))
        self.assertEqual(Galois[2, 6].conway(), PolyModular[2].from_string("X**6 + X**4 + X**3 + X + 1"))
        self.assertEqual(Galois[3, 1].conway(), PolyModular[3].from_string("X + 1"))
        self.assertEqual(Galois[3, 2].conway(), PolyModular[3].from_string("X**2 + 2*X + 2"))
        self.assertEqual(Galois[3, 3].conway(), PolyModular[3].from_string("X**3 + 2*X + 1"))
        self.assertEqual(Galois[3, 4].conway(), PolyModular[3].from_string("X**4 + 2*X**3 + 2"))
        self.assertEqual(Galois[3, 5].conway(), PolyModular[3].from_string("X**5 + 2*X + 1"))

    def test_inverse(self) -> None:
        G: type[Galois] = Galois[2, 3]
        with self.assertRaises(ZeroDivisionError):
            G.zero().inverse
        self.assertEqual(G.one().inverse, 1)
        G = Galois[3, 3]
        self.assertEqual(G.from_string("2").inverse, G.from_string("2"))

    def test_factors(self) -> None:
        G: type[Galois] = Galois[3, 3]
        p1, p2 = G.from_string("X + 1"), G.from_string("X + 2")
        p = p1 * p2
        self.assertEqual(p.factors(), {p1: 1, p2: 1})

    def test_sqrt(self) -> None:
        G: type[Galois] = Galois[3, 3]
        p = G.from_string("X**2 + X")
        self.assertEqual((p**2).sqrt(), p)
        self.assertEqual(G.from_string("X").sqrt(), None)
        for i in (3, 4, 5):
            G = Galois[2, i]
            p = G.from_string("X**2 + X")
            self.assertEqual((p**2).sqrt(), p)
