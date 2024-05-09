import numpy as np
import time

# Generate random uint64 numbers
x = np.random.randint(0, 2**64, size=10000000, dtype=np.uint64)
y = np.random.randint(0, 2**64, size=10000000, dtype=np.uint64)

# Using Python '&' operator
start_time = time.time()
result_python = x & y
end_time = time.time()
python_time = end_time - start_time

# Using NumPy's bitwise_and function
start_time = time.time()
result_numpy = np.bitwise_and(x, y)
end_time = time.time()
numpy_time = end_time - start_time

print("Time taken by Python '&' operator:", python_time)
print("Time taken by NumPy's bitwise_and function:", numpy_time)