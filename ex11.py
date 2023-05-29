import matplotlib.pyplot as plt
import numpy as np
def map(x : int, y :int) -> float:
    return (x * 2**16 + y) / (2**32 - 1)


def reverse_map(x : float) -> tuple[int, int]:
    return (int(x * (2**32 - 1) / 2**16), int(x * (2**32 - 1) % 2**16))


result = []
for i in range(0, 2**16 - 1, 1000):
    for j in range(0, 2**16 - 1, 1000):
        result.append(reverse_map(map(i,j)))
        
plt.scatter([x[0] for x in result], [x[1] for x in result])
plt.show()