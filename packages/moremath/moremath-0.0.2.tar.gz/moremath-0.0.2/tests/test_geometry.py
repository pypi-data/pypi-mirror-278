import unittest
from moremath.geometry import square_perimeter, square_area, rectangle_perimeter, rectangle_area, \
    circle_perimeter, circle_area, cube_volume, cube_surface_area, sphere_volume, sphere_surface_area
import math

class TestGeometryFunctions(unittest.TestCase):

    def test_square_perimeter(self):
        self.assertAlmostEqual(square_perimeter(4), 16)
        self.assertAlmostEqual(square_perimeter(5), 20)
        with self.assertRaises(ValueError):
            square_perimeter(-1)

    def test_square_area(self):
        self.assertAlmostEqual(square_area(4), 16)
        self.assertAlmostEqual(square_area(5), 25)
        with self.assertRaises(ValueError):
            square_area(-1)

    def test_rectangle_perimeter(self):
        self.assertAlmostEqual(rectangle_perimeter(4, 5), 18)
        self.assertAlmostEqual(rectangle_perimeter(2, 3), 10)
        with self.assertRaises(ValueError):
            rectangle_perimeter(-1, 5)
        with self.assertRaises(ValueError):
            rectangle_perimeter(4, -1)

    def test_rectangle_area(self):
        self.assertAlmostEqual(rectangle_area(4, 5), 20)
        self.assertAlmostEqual(rectangle_area(2, 3), 6)
        with self.assertRaises(ValueError):
            rectangle_area(-1, 5)
        with self.assertRaises(ValueError):
            rectangle_area(4, -1)

    def test_circle_perimeter(self):
        self.assertAlmostEqual(circle_perimeter(4), 2 * math.pi * 4)
        self.assertAlmostEqual(circle_perimeter(5), 2 * math.pi * 5)
        with self.assertRaises(ValueError):
            circle_perimeter(-1)

    def test_circle_area(self):
        self.assertAlmostEqual(circle_area(4), math.pi * 4 ** 2)
        self.assertAlmostEqual(circle_area(5), math.pi * 5 ** 2)
        with self.assertRaises(ValueError):
            circle_area(-1)

    def test_cube_volume(self):
        self.assertAlmostEqual(cube_volume(3), 27)
        self.assertAlmostEqual(cube_volume(4), 64)
        with self.assertRaises(ValueError):
            cube_volume(-1)

    def test_cube_surface_area(self):
        self.assertAlmostEqual(cube_surface_area(3), 6 * 3 ** 2)
        self.assertAlmostEqual(cube_surface_area(4), 6 * 4 ** 2)
        with self.assertRaises(ValueError):
            cube_surface_area(-1)

    def test_sphere_volume(self):
        self.assertAlmostEqual(sphere_volume(3), (4 / 3) * math.pi * 3 ** 3)
        self.assertAlmostEqual(sphere_volume(4), (4 / 3) * math.pi * 4 ** 3)
        with self.assertRaises(ValueError):
            sphere_volume(-1)

    def test_sphere_surface_area(self):
        self.assertAlmostEqual(sphere_surface_area(3), 4 * math.pi * 3 ** 2)
        self.assertAlmostEqual(sphere_surface_area(4), 4 * math.pi * 4 ** 2)
        with self.assertRaises(ValueError):
            sphere_surface_area(-1)

if __name__ == '__main__':
    unittest.main()
