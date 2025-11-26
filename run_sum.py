# run_sum.py
from sum_engine import compute_sum, InvalidNumberError

def main():
    sample = [1, 2, 3.5, "4.2"]
    try:
        result = compute_sum(sample, strategy="auto")
    except InvalidNumberError as e:
        print(f"Input error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 2

    total = result["sum"]
    if hasattr(total, "to_eng_string"):
        total = str(total)

    print("Input :", sample)
    print("Result:", {"sum": total, "count": result["count"]})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
