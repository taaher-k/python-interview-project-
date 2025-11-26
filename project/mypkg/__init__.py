# mypkg/__init__.py
"""mypkg — small utilities for adding numbers."""

# Package version
__version__ = "0.1.0"

# Re-export the public functions and exceptions from simple_adder
from .simple_adder import parse_number, parse_count, sum_numbers, InputError

__all__ = ["parse_number", "parse_count", "sum_numbers", "InputError", "__version__"]