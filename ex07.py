operators = ["&", "|", "^", ">", "="]

def calculate(operation : str, a : bool, b : bool) -> bool:
  if   (operation == "&"): return a & b
  elif (operation == "|"): return a | b
  elif (operation == "^"): return a ^ b
  elif (operation == ">"): return a <= b
  elif (operation == "="): return a == b

def eval_formula(formula: str) -> bool:
    tokenList = list(formula)
    result = []
    for token in tokenList:
      if token in operators: 
        operand2 = bool(result.pop())
        operand1 = bool(result.pop())
        result.append(calculate(token,operand1,operand2))
      elif (token == "!"):
        operand = result.pop()
        result.append(not int(operand))
      else:
        result.append(int(token))
    return result[-1]

def sat(formula: str):
    variables = [x for x in list(dict.fromkeys(formula)) if x not in operators and x != "!"]
    mask = 0; # represents which variables should be set 
    cases = 1 << len(variables)
    while (mask < cases): 
        tmp = formula
        for i,v in enumerate(variables): # set variables according to mask
            i = (len(variables) - 1) - i # stupid
            tmp = tmp.replace(v, str((mask >> i) & 1))
        if (eval_formula(tmp)): # output
            print(f"found True output : {tmp}")
            return True 
        mask += 1#mask = adder(mask, 1)
    return False


given_tests = [
("AB|",True),
("AB&",True),
("AA!&",False),
("AA^",False)
]

for t in given_tests:
    s = sat(t[0])
    print(f"{t[0]} -> {s} == {t[1]} | {'o' if  s == t[1] else 'x'}")

expressions = [
                "AB&!",
                "AB|!",
                "AB|C&",
                "AB|C|D|",
                "AB&C&D&",
                "A!B!C!&&"
]

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
for e in expressions:
    print(f"{e} -> {sat(e)}")