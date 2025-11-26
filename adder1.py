# simple_adder.py



from decimal import Decimal, InvalidOperation

class InputError(Exception):
    pass

def parse_count(text: str) -> int:
    text = text.strip()
    if not text:
        raise InputError("Count required")
    n = int(text)
    if n <= 0:
        raise InputError("Count must be positive")
    return n

def parse_number(text: str) -> Decimal:
    text = text.strip()
    if text == "":
        raise InputError("Empty number")
    try:
        # Decimal handles ints, floats (via string) and numeric strings precisely
        return Decimal(text)
    except (InvalidOperation, ValueError):
        raise InputError(f"Invalid number: {text}")

def sum_numbers(items):
    total = Decimal(0)
    count = 0
    for it in items:
        total += parse_number(str(it))
        count += 1
    return total, count

def main():
    try:
        raw = input("How many numbers do you want to add? ")
        n = parse_count(raw)
        values = []
        for i in range(1, n+1):
            v = input(f"Enter number {i}: ")
            values.append(v)
        total, count = sum_numbers(values)
        print("\n--- Result ---")
        print(f"Count: {count}")
        print(f"Sum  : {total}")
    except InputError as e:
        print("Input error:", e)
    except KeyboardInterrupt:
        print("\nCancelled by user")
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()



"""
File header and purpose
python
# simple_adder.py
from decimal import Decimal, InvalidOperation
Explanation

# simple_adder.py is a comment naming the file.

from decimal import Decimal, InvalidOperation imports Decimal for precise numeric arithmetic and InvalidOperation to detect parse errors when converting strings to Decimal.

Custom exception
python
class InputError(Exception):
    pass
Explanation

class InputError(Exception): defines a custom exception type named InputError that inherits from Python’s built-in Exception.

pass means the class has no extra behavior; it exists so the program can raise and catch a clear, domain-specific error.

parse_count function
python
def parse_count(text: str) -> int:
    text = text.strip()
    if not text:
        raise InputError("Count required")
    n = int(text)
    if n <= 0:
        raise InputError("Count must be positive")
    return n
Explanation

def parse_count(text: str) -> int: declares a function that accepts a string and returns an integer.

text = text.strip() removes leading and trailing whitespace from the input.

if not text: checks for an empty string after trimming.

raise InputError("Count required") raises a clear error when the user provided nothing.

n = int(text) converts the cleaned string to an integer; this will raise ValueError if the string is not a valid integer.

if n <= 0: enforces that the count must be positive.

raise InputError("Count must be positive") signals invalid non-positive counts.

return n returns the validated positive integer.

parse_number function
python
def parse_number(text: str) -> Decimal:
    text = text.strip()
    if text == "":
        raise InputError("Empty number")
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        raise InputError(f"Invalid number: {text}")
Explanation

def parse_number(text: str) -> Decimal: declares a function that converts a string to a Decimal.

text = text.strip() trims whitespace from the input.

if text == "": checks for an empty entry and raises InputError("Empty number").

try: return Decimal(text) attempts to construct a Decimal from the string, handling integers, floats written as strings, and numeric strings precisely.

except (InvalidOperation, ValueError): catches parsing failures from Decimal or other conversion issues.

raise InputError(f"Invalid number: {text}") raises a user-friendly error including the offending input.

sum_numbers function
python
def sum_numbers(items):
    total = Decimal(0)
    count = 0
    for it in items:
        total += parse_number(str(it))
        count += 1
    return total, count
Explanation

def sum_numbers(items): defines a function that accepts an iterable of items and returns a tuple (total, count).

total = Decimal(0) initializes the accumulator as a Decimal zero for precise summation.

count = 0 initializes the counter.

for it in items: iterates over each provided item.

total += parse_number(str(it)) converts the item to string, parses it to Decimal via parse_number, and adds it to the running total.

count += 1 increments the number of processed items.

return total, count returns the final sum and the count.

main function and CLI flow
python
def main():
    try:
        raw = input("How many numbers do you want to add? ")
        n = parse_count(raw)
        values = []
        for i in range(1, n+1):
            v = input(f"Enter number {i}: ")
            values.append(v)
        total, count = sum_numbers(values)
        print("\n--- Result ---")
        print(f"Count: {count}")
        print(f"Sum  : {total}")
    except InputError as e:
        print("Input error:", e)
    except KeyboardInterrupt:
        print("\nCancelled by user")
    except Exception as e:
        print("Unexpected error:", e)
Explanation

def main(): defines the program’s entry point for interactive use.

try: begins a block that will catch and handle expected and unexpected errors.

raw = input("How many numbers do you want to add? ") prompts the user for how many numbers they will enter.

n = parse_count(raw) validates and converts that response to a positive integer.

values = [] prepares a list to collect user inputs.

for i in range(1, n+1): loops exactly n times to gather each number.

v = input(f"Enter number {i}: ") prompts for each number and stores the raw input.

values.append(v) appends the raw string to the list; conversion is deferred to sum_numbers.

total, count = sum_numbers(values) converts and sums all inputs, returning the total and count.

print("\n--- Result ---") prints a header for the results.

print(f"Count: {count}") prints how many numbers were summed.

print(f"Sum : {total}") prints the sum; Decimal prints in a human-friendly precise form.

except InputError as e: catches validation errors and prints a friendly message.

except KeyboardInterrupt: handles Ctrl+C gracefully and informs the user the operation was cancelled.

except Exception as e: catches any other unexpected errors and prints a generic message.

Module guard
python
if __name__ == "__main__":
    main()
Explanation

if __name__ == "__main__": ensures main() runs only when the file is executed as a script, not when it is imported as a module.

main() starts the interactive program.

Quick notes on behavior and reuse
Precision: using Decimal avoids floating-point rounding surprises when inputs are strings or mixed types.

Simplicity: functions are small and focused so you can import parse_number or sum_numbers into other scripts or tests.

Error handling: InputError provides clear, catchable validation errors; KeyboardInterrupt is handled for user cancellation.

How to run: execute python simple_adder.py and follow prompts.
"""