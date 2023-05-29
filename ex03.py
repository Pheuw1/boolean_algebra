def calculate(operation : str, a : bool, b : bool) -> bool:
  if   (operation == "&"): return a & b
  elif (operation == "|"): return a | b
  elif (operation == "^"): return a ^ b
  elif (operation == ">"): return a <= b
  elif (operation == "="): return a == b

def eval_formula(formula: str) -> bool:
    tokenList = list(formula)
    operators = ["&", "|", "^", ">", "="]
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


expressions = [
   "10&",
   "10|",
   "101|&",
   "10|1&",
   "1011||=",
   "10=",
   "11=",
   "11>",
   "10>",
   "00>",
   "01>",
   "10|",
   "10&"
]

print(" ### Reverse Polish Notation Parser ###")
for e in expressions:
  print("expression :", e)
  print("result =", eval_formula(e), "\n")