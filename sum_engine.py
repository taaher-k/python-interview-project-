



# sum_engine.py
from decimal import Decimal, InvalidOperation, getcontext
from typing import Iterable, Tuple, Dict, Union, Optional
import logging
import uuid

# Optional: use numpy for large numeric arrays
try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

# Configure Decimal precision globally if needed
getcontext().prec = 28

logger = logging.getLogger("sum_engine")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '{"time":"%(asctime)s","level":"%(levelname)s","request_id":"%(request_id)s","msg":"%(message)s"}'
))
logger.addHandler(handler)


class SumError(Exception):
    """Base class for sum-related errors."""


class InvalidNumberError(SumError):
    """Raised when an input value cannot be parsed as a number."""


def _to_decimal(value) -> Decimal:
    """Convert a single value to Decimal with clear error on failure."""
    try:
        # Convert via str to avoid float precision surprises
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise InvalidNumberError(f"Invalid numeric value: {value}") from exc


def safe_sum(numbers: Iterable[Union[int, float, str, Decimal]]) -> Dict[str, Union[Decimal, int]]:
    """
    Sum an iterable of numbers using Decimal for precision.
    Returns a dict with sum, count, min, max.
    Raises InvalidNumberError on bad input.
    """
    total = Decimal(0)
    count = 0
    min_v: Optional[Decimal] = None
    max_v: Optional[Decimal] = None

    for n in numbers:
        dec = _to_decimal(n)
        total += dec
        count += 1
        if min_v is None or dec < min_v:
            min_v = dec
        if max_v is None or dec > max_v:
            max_v = dec

    return {"sum": total, "count": count, "min": min_v, "max": max_v}


def numpy_sum(numbers) -> Dict[str, Union[float, int]]:
    """
    Fast path for large numeric arrays using NumPy.
    Input should be array-like of numeric types.
    Returns float sum and metadata.
    """
    if not _HAS_NUMPY:
        raise RuntimeError("NumPy not available. Install numpy for this path.")
    arr = np.asarray(numbers, dtype=np.float64)
    total = float(arr.sum())
    return {"sum": total, "count": int(arr.size), "min": float(arr.min()) if arr.size else None,
            "max": float(arr.max()) if arr.size else None}


def stream_sum(file_obj, parser=float, chunk_size: int = 1024 * 1024) -> Dict[str, Union[float, int]]:
    """
    Stream numbers from a file-like object. Each line is expected to contain one number.
    parser: callable to convert string to numeric type (e.g., Decimal or float).
    """
    total = Decimal(0) if parser is Decimal else 0.0
    count = 0
    min_v = None
    max_v = None

    for line in file_obj:
        line = line.strip()
        if not line:
            continue
        try:
            val = parser(line) if parser is not Decimal else Decimal(line)
        except Exception as exc:
            raise InvalidNumberError(f"Invalid numeric value in stream: {line}") from exc

        total += val
        count += 1
        if min_v is None or val < min_v:
            min_v = val
        if max_v is None or val > max_v:
            max_v = val

    return {"sum": total, "count": count, "min": min_v, "max": max_v}


# Map-reduce helper for large datasets
def partial_sum_chunk(chunk: Iterable[Union[int, float, str]]) -> Tuple[Decimal, int]:
    """Return (partial_sum, count) for a chunk using Decimal."""
    s = Decimal(0)
    c = 0
    for x in chunk:
        s += _to_decimal(x)
        c += 1
    return s, c


def reduce_partials(partials: Iterable[Tuple[Decimal, int]]) -> Dict[str, Union[Decimal, int]]:
    """Aggregate partial sums into final result."""
    total = Decimal(0)
    count = 0
    for s, c in partials:
        total += s
        count += c
    return {"sum": total, "count": count}


# Utility wrapper to choose best strategy
def compute_sum(numbers: Iterable, strategy: str = "auto") -> Dict:
    """
    strategy: "auto", "safe", "numpy"
    - auto: use numpy if available and input is list/array-like
    - safe: use Decimal-based safe_sum
    - numpy: use numpy_sum (raises if numpy not available)
    """
    request_id = str(uuid.uuid4())
    extra = {"request_id": request_id}
    logger.info("compute_sum called", extra=extra)

    if strategy == "numpy":
        return numpy_sum(numbers)
    if strategy == "safe":
        return safe_sum(numbers)

    # auto
    if _HAS_NUMPY:
        try:
            # try numpy path for performance
            return numpy_sum(numbers)
        except Exception:
            # fallback to safe path
            logger.info("numpy path failed, falling back to safe_sum", extra=extra)
            return safe_sum(numbers)
    else:
        return safe_sum(numbers)





# at the end of sum_engine.py

if __name__ == "__main__":
    from sum_engine import compute_sum, InvalidNumberError  # local import is fine here

    sample = [1, 2, 3.5, "4.2"]
    try:
        result = compute_sum(sample, strategy="auto")
    except InvalidNumberError as e:
        print(f"Input error: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise SystemExit(2)

    total = result.get("sum")
    # Convert Decimal to string for safe printing/JSON
    if hasattr(total, "to_eng_string"):
        total = str(total)

    print("Input :", sample)
    print("Result:", {"sum": total, "count": result.get("count")})
