__version__ = '1.0'

from .algebra import exponentiation as exp
from .algebra import logarithm as log
from .statistics import mean, median, mode
from .arithmetic import add, subtract, multiply, divide, factorial
from .geometry import (
    square_perimeter, square_area,
    rectangle_perimeter, rectangle_area,
    circle_perimeter, circle_area,
    cube_volume, cube_surface_area,
    sphere_volume, sphere_surface_area
)
from .factors import prime_factors
