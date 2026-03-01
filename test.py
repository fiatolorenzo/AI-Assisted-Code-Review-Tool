import os
from analyzer.runner import run_cmd
run_cmd(["python", "-m", "pylint", "samples/test.py", "--output-format=json"])
user_input = input("Enter something: ")
eval(user_input)

def complex_example(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        total = 0
        for i in range(x):
            if i % 2 == 0:
                total += i
            else:
                total -= i
        if total > 10:
            return 1
        return 2