import matplotlib.pyplot as plt
import numpy as np

def map(x : int, y :int) -> float:
    return (x * 2**16 + y) / (2**32 - 1)


def z_order(x : int, y : int) -> float:
    result = 0
    for i in range(16):
        result |= ((x >> i) & 1) << (2 * i)
        result |= ((y >> i) & 1) << (2 * i + 1)
    return result / (2**32 - 1)



def main():
    result = []
    for i in     range(0, 2**16 - 1, 1000):
        for j in range(0, 2**16 - 1, 1000):
            result.append(map(i,j))

    print("### Testing Curve ###")
    print("--------------------")
    print("First : matrix mapping")
    print("--------------------")
    plt.scatter(result,result,c=result, cmap = 'rainbow')
    plt.show()

    for i in     range(0, 2**16 - 1, 1000):
        for j in range(0, 2**16 - 1, 1000):
            result.append(z_order(i,j))

    print("Second : z-order mapping")
    print("--------------------")

    plt.scatter(result,result,c=result, cmap = 'rainbow')
    plt.show()
    
if __name__ == "__main__":
    main()