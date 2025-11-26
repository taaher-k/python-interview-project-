#!/usr/bin/env python3
"""
adder.py
Interactive, modular number adder with conversion, error handling, and
a fast path for large numeric lists.
"""

from decimal import Decimal, InvalidOperation, getcontext
from typing import Iterable, List, Tuple, Union, Optional
import logging

# Optional fast path
try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

# Decimal precision (adjust if you need more)
getcontext().prec = 28

logger = logging.getLogger("adder")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


class InvalidNumberError(ValueError):
    """Raised when an input cannot be parsed as a number."""


def parse_count(raw: str) -> int:
    """Parse the user's count input and validate it is a positive integer."""
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty input for count")
    try:
        n = int(raw)
    except Exception:
        raise ValueError("Please enter a valid integer for the count")
    if n <= 0:
        raise ValueError("Count must be a positive integer")
    return n


def convert_to_decimal(value: Union[str, int, float, Decimal]) -> Decimal:
    """
    Convert a single value to Decimal.
    Accepts numeric strings, ints, floats, and Decimal.
    Raises InvalidNumberError on failure.
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int,)):
        return Decimal(value)
    if isinstance(value, float):
        # Convert via str to reduce float representation surprises
        return Decimal(str(value))
    if isinstance(value, str):
        s = value.strip()
        if s == "":
            raise InvalidNumberError("Empty string is not a number")
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError) as exc:
            raise InvalidNumberError(f"Invalid numeric string: {value}") from exc
    raise InvalidNumberError(f"Unsupported type: {type(value)}")


def safe_sum_decimals(numbers: Iterable[Union[str, int, float, Decimal]]) -> Tuple[Decimal, int]:
    """
    Accurate sum using Decimal. Returns (sum, count).
    Use this when precision matters or inputs are mixed strings.
    """
    total = Decimal(0)
    count = 0
    for x in numbers:
        dec = convert_to_decimal(x)
        total += dec
        count += 1
    return total, count


def fast_sum_float(numbers: Iterable[Union[int, float, str]]) -> Tuple[float, int]:
    """
    Fast numeric sum using NumPy if available.
    Converts inputs to float; not as precise as Decimal for some cases.
    Returns (sum, count).
    """
    if not _HAS_NUMPY:
        # Fallback to Python float sum
        arr = [float(x) for x in numbers]
        return float(sum(arr)), len(arr)
    # Use numpy for speed on large arrays
    arr = np.asarray([float(x) for x in numbers], dtype=np.float64)
    return float(arr.sum()), int(arr.size)


def choose_strategy_and_sum(numbers: List[Union[str, int, float, Decimal]]) -> dict:
    """
    Choose a strategy:
    - If all inputs are numeric (int/float) and numpy is available and list is large,
      use fast_sum_float for performance.
    - Otherwise use safe_sum_decimals for accuracy.
    Returns a dict with sum, count, strategy.
    """
    count = len(numbers)
    all_numeric_simple = all(isinstance(x, (int, float)) for x in numbers)
    # If strings present but they are numeric strings, safe Decimal is preferred
    if all_numeric_simple and _HAS_NUMPY and count >= 1000:
        s, c = fast_sum_float(numbers)
        return {"sum": s, "count": c, "strategy": "numpy_float" if _HAS_NUMPY else "python_float"}
    # Default: accurate Decimal path
    s, c = safe_sum_decimals(numbers)
    return {"sum": s, "count": c, "strategy": "decimal"}


def interactive_input() -> List[Union[str, int, float]]:
    """
    Interactively ask the user how many numbers, then read that many inputs.
    Returns the raw inputs (strings preserved) for later conversion/validation.
    """
    while True:
        try:
            raw_count = input("How many numbers do you want to add? ").strip()
            n = parse_count(raw_count)
            break
        except Exception as e:
            print(f"Invalid input: {e}")
    inputs: List[Union[str, int, float]] = []
    for i in range(1, n + 1):
        while True:
            try:
                raw = input(f"Enter number {i}: ").strip()
                # Accept raw as-is; conversion happens later
                if raw == "":
                    raise InvalidNumberError("Empty input is not allowed")
                # Try to detect int or float quickly for convenience
                # But keep as string so conversion strategy can decide
                inputs.append(raw)
                break
            except InvalidNumberError as e:
                print(f"Invalid input: {e}")
    return inputs


def run_cli():
    """Main CLI runner with exception handling and friendly output."""
    try:
        raw_inputs = interactive_input()
        # Decide strategy and compute
        result = choose_strategy_and_sum(raw_inputs)
        total = result["sum"]
        # If Decimal, convert to string for stable display
        if isinstance(total, Decimal):
            total_display = str(total)
        else:
            total_display = repr(total)
        print("\n--- Result ---")
        print(f"Count   : {result['count']}")
        print(f"Strategy: {result['strategy']}")
        print(f"Sum     : {total_display}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except InvalidNumberError as e:
        print(f"Input error: {e}")
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    run_cli()
