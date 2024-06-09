from py_jaxtyping import PyArray
from jaxtyping import Int
Contour = PyArray[Int, int, "4 1 2"]
Contours = PyArray[Int, int, "N 4 1 2"]