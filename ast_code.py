import ast
from astunparse import unparse
from json import dumps
from treediffer import treediff


def read(filename):
    with open(filename, 'r') as file:
        return file.read()


a = read('code1.py')
parsed_tree_a = ast.parse(a)
# print(ast.dump(parsed_tree_a, indent=4))


'''
Visiting ast nodes

body = parsed_tree_a.body
print(body[0].name)
print(body[1].name)
print(body[2].test.left.id)

'''

# b = read('code2.py')
# parsed_tree_b = ast.parse(b)
# print(ast.dump(parsed_tree_b, indent=4))


# # Convert the AST back to Python code
# python_code = unparse(parsed_tree_a)
# # Print the Python code
# print(python_code)
