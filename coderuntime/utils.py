
import time

def timedfunction(func, *args, **kwargs):
    start_time = int(time.time())
    result = func(*args, **kwargs)
    end_time = int(time.time())
    return (end_time - start_time), result
