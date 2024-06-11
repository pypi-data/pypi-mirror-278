from typing import Union, List
import math

def square_perimeter(side_length: float) -> float:
    """Calculate the perimeter of a square."""
    if side_length <= 0:
        raise ValueError("Side length must be a positive number.")
    return 4 * side_length

def square_area(side_length: float) -> float:
    """Calculate the area of a square."""
    if side_length <= 0:
        raise ValueError("Side length must be a positive number.")
    return side_length ** 2

def rectangle_perimeter(length: float, width: float) -> float:
    """Calculate the perimeter of a rectangle."""
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive numbers.")
    return 2 * (length + width)

def rectangle_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive numbers.")
    return length * width

def circle_perimeter(radius: float) -> float:
    """Calculate the perimeter of a circle."""
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")
    return 2 * math.pi * radius

def circle_area(radius: float) -> float:
    """Calculate the area of a circle."""
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")
    return math.pi * radius ** 2

def cube_volume(side_length: float) -> float:
    """Calculate the volume of a cube."""
    if side_length <= 0:
        raise ValueError("Side length must be a positive number.")
    return side_length ** 3

def cube_surface_area(side_length: float) -> float:
    """Calculate the surface area of a cube."""
    if side_length <= 0:
        raise ValueError("Side length must be a positive number.")
    return 6 * side_length ** 2

def sphere_volume(radius: float) -> float:
    """Calculate the volume of a sphere."""
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")
    return (4 / 3) * math.pi * radius ** 3

def sphere_surface_area(radius: float) -> float:
    """Calculate the surface area of a sphere."""
    if radius <= 0:
        raise ValueError("Radius must be a positive number.")
    return 4 * math.pi * radius ** 2
