import numpy as np
from linalg import *

a = np.array([0, 2])
b = np.array([1, 0])

matrix = get_rotation(a, b, 2, 1)

print(a@matrix * 0.5)

test = np.array([-2, 0])

print(test@matrix)
