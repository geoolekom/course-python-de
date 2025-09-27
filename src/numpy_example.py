from utils.timeit import timeit

import numpy

with timeit("Python list"):
    python_list = list(range(1_000_000))
    python_list = [x * 2 for x in python_list]


with timeit("Numpy array"):
    numpy_list = numpy.arange(1_000_000)
    numpy_list = numpy_list * 2

# multiple two vectors (1, 2, 3) and (4, 5, 6) = (4 + 10 + 18) = 32


def dot_product(a: list[int], b: list[int]) -> int:
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


with timeit("Dot product Python list"):
    dot_product(python_list, python_list)

with timeit("Dot product Numpy array"):
    numpy.dot(numpy_list, numpy_list)

with timeit("Sum Python list"):
    v = max(python_list)

print(v)

with timeit("Sum Numpy array"):
    v = numpy.max(numpy_list)

print(v)
