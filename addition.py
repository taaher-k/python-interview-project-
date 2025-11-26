from decimal import Decimal, InvalidOperation
from typing import Iterable, Dict

def safe_sum(numbers: Iterable) -> Dict:
    total = Decimal(0)
    count = 0
    for n in numbers:
        try:
            total += Decimal(str(n))
            count += 1
        except InvalidOperation:
            raise ValueError(f"Invalid numeric value: {n}")
    return {"sum": total, "count": count}
