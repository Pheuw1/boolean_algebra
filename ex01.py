from ex00 import adder, c_uint32

def multiplier(a : c_uint32, b : c_uint32) -> c_uint32 :
    result, comp = 0 , 1
    while (comp < a):
        for i in range(comp & a):
            result = adder(result, b)
        comp = comp << 1
    return result


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

print("### Testing multiplier ###")
for a,b in tests:
    print(f"{a} * {b} = {multiplier(a,b)} || {a * b}")

