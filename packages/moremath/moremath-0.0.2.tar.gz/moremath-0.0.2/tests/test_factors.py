import unittest
from moremath.factors import prime_factors

class TestPrimeFactors(unittest.TestCase):

    def test_prime_factors(self):
        self.assertEqual(prime_factors(7), [7])
        self.assertEqual(prime_factors(12), [2, 2, 3])
        self.assertEqual(prime_factors(1), [])
        self.assertEqual(prime_factors(0), [])
        self.assertEqual(prime_factors(97), [97])
        self.assertEqual(prime_factors(100), [2, 2, 5, 5])

if __name__ == '__main__':
    unittest.main()
