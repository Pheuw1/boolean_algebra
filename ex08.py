from collections import Counter
import numpy as np

def powerset(set : list[int]) -> list[list[int]]:
    result = []
    for i in range(1 << len(set)):
        result.append([set[j] for j in range(len(set)) if (i & (1 << j))])
    return result

powersets = [
    [
        1,2,3
    ],
    [
        1,2,3,4
    ],
    [
        1
    ],
]


print("### Testing powerset ###")

for p in powersets:
    pwst = (powerset(p))
    count = Counter(map(len, pwst))
    print(f"powerset of {p} : {(pwst)}\n -> {count}")