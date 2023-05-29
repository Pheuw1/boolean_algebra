import astor
import ast
import treelib
import pptree

class Node:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
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


def group_ands(n : Node):
    if n.value == "&":
        if n.left.value == "&":
            n.left = n.left.left
            n.left.parent = n
            group_ands(n)
        if n.right.value == "&":
            n.right = n.right.right
            n.right.parent = n
            group_ands(n)

def group_ors(n : Node):
    if n.value == "|":
        if n.left.value == "|":
            n.left = n.left.left
            n.left.parent = n
            group_ors(n)
        if n.right.value == "|":
            n.right = n.right.right
            n.right.parent = n
            group_ors(n)
        
def convert_tree(n : Node):
    exclusive_or(n)
    equivalence(n)
    implication(n)
    negation(n)
    if (n.left != None):
        convert_tree(n.left)
    if (n.right != None):
        convert_tree(n.right)


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
    # root.display()
    convert_tree(root)
    remove_empty(root)
    if root.value == "":
        root = root.left
        root.parent = None
    # root.display()

    return to_expression(root)
    
expression = "ab&!a&!b&!"
expressions =  [
                "AB&!", 
                "AB|!", 
                "AB>", 
                "AB=",
                "AB|C&!",
                "AB|C|D|",
                "AB&C&D&",
                "AB|!C!&"
                ]

for e in expressions:
    print(f"{e} NNF-> {negation_normal_form(e)}")
    

