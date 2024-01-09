from coderuntime.env import execute
from coderuntime.utils import timedfunction
if __name__ == "__main__":
    code = """
import time
for i in range(1, 10):
    print(i)
    time.sleep(1)
"""
    time_taken, result = timedfunction(execute, code, "python3.10")
    print(time_taken, result)