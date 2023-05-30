
from ctypes import *

def adder(a : c_uint32 , b : c_uint32) -> c_uint32 :
    keep , new = a , b
    while (new != 0) :
        carry = keep & new   
        keep = keep ^ new
        new = carry << 1
    return keep

tests = [
        (45,52),
        (0,0),
        (1,0),
        (0,1),
        (1,1),
        (0,2),
        (2,0),
        (0,3),
        (3,0),
        (2,2),
        (3,3),
        (100000,5),
        (100000,0),
        (0,100000),
         ]


print("### Testing adder ###")
for a,b in tests:
    print(f"{a} + {b} = {adder(a,b)} || {a+b}")