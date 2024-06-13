import unittest
from moremath.statistics import mean, median, mode

class TestStatisticsFunctions(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(mean([1, 2, 3]), 2.0)
        self.assertEqual(mean([2, 4, 6, 8, 10]), 6.0)

    def test_median(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([1, 3, 5, 7, 9]), 5)
        self.assertEqual(median([2, 4, 6, 8, 10]), 6)

    def test_mode(self):
        self.assertEqual(mode([1, 2, 2, 3, 3, 3, 4, 4, 4, 4]), 4)
        self.assertEqual(mode([1, 1, 2, 3, 3, 3, 4, 4, 4, 4]), 4)
        self.assertEqual(mode([1, 2, 3, 4, 5]), 1)  

if __name__ == '__main__':
    unittest.main()
