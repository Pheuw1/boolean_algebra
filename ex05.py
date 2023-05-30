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
    convert_tree(root)
    remove_empty(root)
    if root.value == "":
        root = root.left
        root.parent = None

    return to_expression(root)
    

def main():
        
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


    print("### Testing NNF ###")
    for e in expressions:
        print(f"{e} NNF-> {negation_normal_form(e)}")
        

if __name__ == "__main__":
    main()
