from ex05 import negation_normal_form

def conjunction_to_end(expression :str):
    for e in (expression):
        if e == "&":
            expression = expression.erase(e, "", 1)
            expression += e
    
    for e in (expression):
        if e == "|" and expression[-1] != "&":
            expression = expression.replace(e, "", 1)
            expression += e
            
    return expression

def conjunctive_normal_form(expression : str) -> str:
    return conjunction_to_end(negation_normal_form(expression))
  
given_test = [
    ("AB&!","A!B!|"),
    ("AB|!","A!B!&"),
    ("AB|C&","AB|C&"),
    ("AB|C|D|","ABCD|||"),
    ("AB&C&D&","ABCD&&&"),
    ("AB&!C!|","A!B!C!||"),
    ("AB|!C!&","A!B!C!&&")
]

expressions =  [
            "AB&!", 
            "AB|!", 
            "AB>", 
            "AB=",
            "AB|C&!",
            "AB|C|D|",
            "AB&C&D&"
            "AB&!"
            ,"AB|!"
            ,"AB|C&"
            ,"AB|C|D|"
            ,"AB&C&D&"
            ,"AB&!C!|"
            ,"AB|!C!&"
]

print("### Testing CNF")
print("-----------------")
print("given test cases")
print("-------------------")
for t in given_test:
    nnf = negation_normal_form(t[0])
    cnf = conjunctive_normal_form(t[0])
    print(f"{t[0]} NNF-> {nnf} same? : {nnf == cnf} CNF-> {cnf} == {t[1]} | {'pass' if  cnf == t[1] else 'fail'}")

print("-----------------")
print("chosen test cases")
print("-------------------")
for e in expressions:
    print(f"{e} NNF-> {conjunctive_normal_form(e)}")
    
    

