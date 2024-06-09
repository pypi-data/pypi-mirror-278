from doctest import DocTestSuite
from elliptic import abc, curves, fin, inf, mod, poly
from unittest import TestCase


class TestDocstrings(TestCase):
    # If a test fails, run:
    #    python -m doctest -v FILE
    # to see the docstrings errors in FILE

    def test_abc(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(abc).run(result)
        self.assertTrue(result.wasSuccessful())

    def test_curves(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(curves).run(result)
        self.assertTrue(result.wasSuccessful())

    def test_inf(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(inf).run(result)
        self.assertTrue(result.wasSuccessful())

    def test_mod(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(mod).run(result)
        self.assertTrue(result.wasSuccessful())

    def test_poly(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(poly).run(result)
        self.assertTrue(result.wasSuccessful())

    def test_fin(self) -> None:
        result = self.defaultTestResult()
        DocTestSuite(fin).run(result)
        self.assertTrue(result.wasSuccessful())
