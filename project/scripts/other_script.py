# at top of scripts/other_script.py
import sys
sys.path.append("../")   # add project root to path (use absolute path in real projects)
from simple_adder import sum_numbers


from mypkg.simple_adder import sum_numbers, InputError

items = ["1", "2.5"]
try:
    total, count = sum_numbers(items)
    print(total, count)
except InputError as e:
    print("Input error:", e)
