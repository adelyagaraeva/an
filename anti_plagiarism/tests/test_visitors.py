import ast

import pytest
from backend.tree_visitors import *


def test_if():
    code = '''
if False or False:
    print(1)
    '''
    tree = ast.parse(code)
    visitor = Visitor()
    visitor.visit(tree)

    assert visitor.data == ['Module']

    code = '''
if 1:
    print(1)
    '''
    tree = ast.parse(code)
    visitor = Visitor()
    visitor.visit(tree)

    assert visitor.data == ['Module']


def test_import():
    code_1 = '''
import numpy, pandas
        '''

    code_2 = '''
import numpy
import pandas
            '''
    tree = ast.parse(code_1)
    visitor = Visitor()
    visitor.visit(tree)
    code_1_tree = visitor.data

    tree = ast.parse(code_2)
    visitor = Visitor()
    visitor.visit(tree)
    code_2_tree = visitor.data

    assert code_1_tree == code_2_tree


def test_constant():
    code = '''
a = 1
b = 10
a = a + b
    '''
    tree = ast.parse(code)
    visitor = Visitor()
    visitor.visit(tree)

    assert 1 in visitor.data and 10 in visitor.data and 11 not in visitor.data


def test_ann():
    code_1 = '''
a: int = 10
'''
    tree = ast.parse(code_1)
    visitor = Visitor()
    visitor.visit(tree)
    code_1_tree = visitor.data

    assert 'AnnAssign' not in code_1_tree


def test_sorting():
    code_1 = '''
def f(x):
    x += 1
    return x
    
def g(x):
    x.append(1)
    a = [x, 1]
    print(a)
    return x
'''
    code_2 = '''
def g(x):
    x.append(1)
    a = [x, 1]
    print(a)
    return x    
    
def f(x):
    x += 1
    return x
'''

    tree = ast.parse(code_1)
    visitor = NodeSorting()
    visitor.run(tree)
    visitor = Visitor()
    visitor.visit(tree)
    temp_tree = visitor.data

    tree_2 = ast.parse(code_2)
    visitor = NodeSorting()
    visitor.run(tree_2)
    visitor = Visitor()
    visitor.visit(tree_2)

    assert temp_tree == visitor.data


def test_binop():
    code_1 = '''
if x > y:
    print(2 + 2)
    '''
    code_2 = '''
if x > y:
    print(4)
    '''

    tree = ast.parse(code_1)
    visitor = NodeSorting()
    visitor.run(tree)
    visitor = Visitor()
    visitor.visit(tree)
    temp_tree = visitor.data

    tree_2 = ast.parse(code_2)
    visitor = NodeSorting()
    visitor.run(tree_2)
    visitor = Visitor()
    visitor.visit(tree_2)

    assert temp_tree == visitor.data


