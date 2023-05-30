import matplotlib.pyplot as plt
import numpy as np
from ex10 import map, z_order


def reverse_map(x : float) -> tuple[int, int]:
    return (int(x * (2**32 - 1) / 2**16), int(x * (2**32 - 1) % 2**16))

def reverse_z_order(x: float) -> tuple[int, int]:
    result = int(x * (2**16 - 1))
    ret_x = 0
    ret_y = 0
    for i in range(16):
        ret_x |= ((result >> (2 * i)) & 1) << i
        ret_y |= ((result >> (2 * i + 1)) & 1) << i
    return (ret_x, ret_y)

result = []
for i in range(0, 2**16 - 1, 1000):
    for j in range(0, 2**16 - 1, 1000):
        result.append(reverse_map(map(i,j)))
        

print("### Testing Curve ###")
print("--------------------")
print("First : matrix mapping")
print("--------------------")

plt.scatter([x[0] for x in result], [x[1] for x in result])
plt.show()

result = []
for i in range(0, 2**16 - 1, 1000):
    for j in range(0, 2**16 - 1, 1000):
        result.append(reverse_z_order(map(i,j)))
        
print("Second : z-order mapping")
print("--------------------")

plt.scatter([x[0] for x in result], [x[1] for x in result])
plt.show()


