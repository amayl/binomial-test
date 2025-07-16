import unittest
from main import factorial, binomial_dist, cdf

class TestMain(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(7), 5040)

    def test_binomial_dist(self):
        # n=5, p=0.5, x=2: 5C2 * 0.5^2 * 0.5^3 = 10 * 0.25 * 0.125 = 0.3125
        self.assertAlmostEqual(binomial_dist(5, 0.5, 2), 0.3125)
        # n=10, p=0.2, x=3
        self.assertAlmostEqual(binomial_dist(10, 0.2, 3), 0.201326592, places=6)
        # n=4, p=0.7, x=4
        self.assertAlmostEqual(binomial_dist(4, 0.7, 4), 0.2401, places=6)

    def test_cdf(self):
        # n=5, p=0.5, x=2: sum of binomial_dist(5, 0.5, i) for i=0,1,2
        expected = sum([binomial_dist(5, 0.5, i) for i in range(3)])
        self.assertAlmostEqual(cdf(5, 0.5, 2), expected)
        # n=3, p=0.3, x=1
        expected = sum([binomial_dist(3, 0.3, i) for i in range(2)])
        self.assertAlmostEqual(cdf(3, 0.3, 1), expected)

    def test_binomial_dist_edge_cases(self):
        # x=0
        self.assertAlmostEqual(binomial_dist(5, 0.5, 0), 0.03125)
        # x=n
        self.assertAlmostEqual(binomial_dist(5, 0.5, 5), 0.03125)
        # p=0
        self.assertAlmostEqual(binomial_dist(5, 0, 0), 1.0)
        self.assertAlmostEqual(binomial_dist(5, 0, 1), 0.0)
        # p=1
        self.assertAlmostEqual(binomial_dist(5, 1, 5), 1.0)
        self.assertAlmostEqual(binomial_dist(5, 1, 4), 0.0)

    def test_cdf_edge_cases(self):
        # x < 0
        self.assertEqual(cdf(5, 0.5, -1), 0)
        # x >= n
        self.assertAlmostEqual(cdf(5, 0.5, 5), 1.0)

if __name__ == '__main__':
    unittest.main(verbosity=2)