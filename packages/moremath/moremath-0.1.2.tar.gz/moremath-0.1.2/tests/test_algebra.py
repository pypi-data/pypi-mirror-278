import unittest
from moremath.algebra import exponentiation, logarithm


class TestAlgebraFunctions(unittest.TestCase):

    def test_exponentiation(self):
        self.assertEqual(exponentiation(2, 3), 8)
        self.assertEqual(exponentiation(5, 2), 25)
        self.assertAlmostEqual(exponentiation(2, 0.5), 1.4142135623730951, places=10)

    def test_logarithm(self):
        self.assertAlmostEqual(logarithm(100, 10), 2)
        self.assertAlmostEqual(logarithm(10, 10), 1)
        self.assertAlmostEqual(logarithm(1, 10), 0)
        self.assertAlmostEqual(logarithm(2, 2), 1)
        self.assertAlmostEqual(logarithm(1000, 10), 3)

    def test_exponentiation_invalid_input(self):
        with self.assertRaises(TypeError):
            exponentiation("2", 3)
        with self.assertRaises(TypeError):
            exponentiation(2, "3")

    def test_logarithm_invalid_input(self):
        with self.assertRaises(TypeError):
            logarithm("100", 10)
        with self.assertRaises(TypeError):
            logarithm(100, "10")
        with self.assertRaises(ValueError):
            logarithm(0, 10)
        with self.assertRaises(ValueError):
            logarithm(100, 0)
        with self.assertRaises(ValueError):
            logarithm(100, 1)


if __name__ == '__main__':
    unittest.main()
