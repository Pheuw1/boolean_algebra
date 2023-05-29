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
      elif (token == "!") :
        operand = result.pop()
        result.append(not int(operand))
      else:
        result.append(int(token))
    return result[-1]

def print_head(variables):
    print('|', end=' '); print(*(variables + ['=']), sep = " | ", end=' '); print('|')
    print('|', end='-'); print(*(['-'] * (len(variables) + 1)), sep = "-|-", end='-'); print('|')
    
def print_row(variables, mask : int, resutlt : bool):
    print('|', end=' '); print(*[(mask >> (len(variables) - 1 - i)) & 1 for i in range(len(variables))] + [int(resutlt)  ], sep = " | ", end=' ');print('|')

def print_truth_table(formula: str):
    variables = [x for x in list(dict.fromkeys(formula)) if x not in operators]
    mask = 0; # represents which variables should be set 
    cases = 1 << len(variables)
    print_head(variables)
    while (mask < cases): 
        tmp = formula
        for i,v in enumerate(variables): # set variables according to mask
            i = (len(variables) - 1) - i # stupid
            tmp = tmp.replace(v, str((mask >> i) & 1))
        print_row(variables, mask, eval_formula(tmp)) # output 
        mask += 1#mask = adder(mask, 1)
        
print_truth_table("AB&C|")
