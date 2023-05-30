
class Node:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        
    def root(self):
        if self.parent == None:
            return self
        return self.parent.root()
    
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

def build_ast(expression):
    stack = []
    for token in expression:
        if token.isalpha():
            stack.append(Node(token))
        elif token == "!":
            right = stack.pop()
            stack.append(Node(token, right))
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(Node(token, left, right))
    def traverse(node):
        if node.left != None:
            node.left.parent = node
            traverse(node.left)
        if node.right != None:
            node.right.parent = node
            traverse(node.right)
    traverse(stack[0])
    return stack[0]

def exclusive_or(n : Node):
    if n.value == "^":
        n.value = "|"
        n.left = Node("!", n.left, None, n)
        n.right = Node("!", n.right, None, n)
        n.left = Node("&", n.left, n.right)
        n.right = None

def equivalence(n : Node):
    if n.value == "=":
        n.value = "|"
        n.left = Node("&", n.left, n.right)
        n.right = Node("&", Node("!", n.left.left, None, n), Node("!", n.left.right, None, n))
        
def implication(n : Node):
    if n.value == ">":
        n.value = "|"
        n.left = Node("!", n.left, None, n)
        
def negation(n : Node):
    if n.value == "!":  
        if n.left.value == "&":
            n.left.value = "|"
            n.left.left = Node("!", n.left.left, None, n.left)
            n.left.right = Node("!", n.left.right, None, n.left)
            n.value = ""
        elif n.left.value == "|":
            n.left.value = "&"
            n.left.left = Node("!", n.left.left, None, n.left)
            n.left.right = Node("!", n.left.right, None, n.left)
            n.left.parent = n.parent
            n.value = ""


def swap_branches(n1, n2):
    parent1 = n1.parent
    parent2 = n2.parent
    
    if parent1 is not None:
        if parent1.left == n1:
            parent1.left = n2
        else:
            parent1.right = n2
        n2.parent = parent1
    
    if parent2 is not None:
        if parent2.left == n2:
            parent2.left = n1
        else:
            parent2.right = n1
        n1.parent = parent2
    
    return n2, n1


def convert_tree_nnf(n : Node):
    exclusive_or(n)
    equivalence(n)
    implication(n)
    negation(n)
    if (n.left != None):
        convert_tree_nnf(n.left)
    if (n.right != None):
        convert_tree_nnf(n.right)

def to_expression(root : Node) -> str:
    if root == None:
        return ""
    return to_expression(root.left) + to_expression(root.right) + root.value

def remove_empty(node):
    if node.value == "":
        if node.left != None:
            node.left.parent = node.parent
            if node.parent != None:
                node.parent.left = node.left
        if node.right != None:
            node.right.parent = node.parent
            if node.parent != None:
              node.parent.right = node.right
    if node.left != None:
        remove_empty(node.left)
    if node.right != None:
        remove_empty(node.right)
        
 
 
def negation_normal_form(expression : str) -> str:
    root = build_ast(expression)
    convert_tree_nnf(root)
    remove_empty(root)
    if root.value == "":
        root = root.left
        root.parent = None

    return to_expression(root)
 
def conjunction_to_end(expression :str):
    for i,e in enumerate(expression):
        if e == "&":
            expression = expression.replace(e, "", 1)
            expression += e
            continue
        elif e == "|" and expression[-1] != "&":
            expression = expression.replace(e, "", 1)
            expression += e
    return expression

def conjunctive_normal_form(expression : str) -> str:
    root = build_ast(expression)
    convert_tree_nnf(root)
    return conjunction_to_end(to_expression(root))

  
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
    
    

