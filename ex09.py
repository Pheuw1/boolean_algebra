

def calculate(operation: str, a: set, b: set) -> set:
    if (operation == "|"):
        return a.union(b)
    elif (operation == "&"):
        return a.intersection(b)
    elif (operation == "^"):
        return a.symmetric_difference(b)
    elif (operation == ">"):
        return a.issubset(b)
    elif (operation == "="):
        return a.unique() == b.unique()


def eval_set(formula: str, sets: list[set]) -> set:
    vars = [x for x in list(dict.fromkeys(formula)) if x.isalpha()]
    if (len(vars) != len(sets)):
        return set()
    mapping = dict(zip(vars, sets))
    tokenList = list(formula)
    operators = ["&", "|", "^", ">", "="]
    result = []
    for token in tokenList:
        if token in operators:
            operand2 = result.pop()
            operand1 = result.pop()
            result.append(calculate(token, operand1, operand2))
        elif (token == "!"):
            result.pop()
            result.append(set())
        else:
            result.append(mapping[token])
    print(mapping)
    return result[0]


tests = [
    ([
        {0, 1, 2},
        {0, 3, 4},
    ],
        "AB&"),
    ([
        {0, 1, 2},
        {3, 4, 5},
    ],
        "AB|"),
    ([
        {0, 1, 2},
    ],
        "A!"),
    ([
        {0, 1, 2},
        {3, 4, 5},
        {3, 7, 8},
    ], 
        "AB|C&"),
        ([
        {0, 1, 2},
        {8, 4, 5},
        {8, 7, 5},
        {2, 8, 5},
    ], 
        "A!B|C&D&"),
]


for (s, f) in tests:
    print(f"{s} -> {f} == {eval_set(f, s)}\n")
