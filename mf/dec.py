import numpy as np
import errno

from time import time_ns

"""
Another python funcs file.

Needs to be cleaned and checked.

"""

# TimeIt: A decorator for timing a single execution of a function.
def timeit(func):
	def wrap_func(*args, **kwargs):
		t1 = time_ns()
		result = func(*args, **kwargs)
		t2 = time_ns()
		print(f"Function {func.__name__!r} took {(t2-t1)/1000000:.6f}ms")
		return result
	return wrap_func

# TimeItRepeated: A decorator for timing multiple executions of a function and reporting mean and standard deviation.
def timeitR(count):
	def decorator(func):
		def wrapper(*args, **kwargs):
			deltas = np.empty([0])
			for _ in range(count):
				t1 = time_ns()
				result = func(*args, **kwargs)
				t2 = time_ns()
				deltas = np.append(deltas, (t2-t1)/1000000)
			print(f"Function {func.__name__!r} took {np.mean(deltas):.6f} ms with std of {np.std(deltas):.6f}")
			return result
		return wrapper
	return decorator	


