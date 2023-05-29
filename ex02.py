from ctypes import *
from bitstring import BitArray
import graycode

def gray_code(n: c_uint32) -> c_uint32:
        return n ^ (n >> 1)
    

for i in range(16):
    print(f"{i} : {gray_code(i)}, {bin(gray_code(i))} || {graycode.tc_to_gray_code(i)}, {bin(graycode.tc_to_gray_code(i))}")