import ast
from graphviz import Digraph

code = '''
def greet(name):
    print("Hello, World!")
'''

tree = ast.parse(code)

# Create a Graphviz Digraph object
dot = Digraph()

# Define a function to recursively add nodes to the Digraph
def add_node(node, parent=None):
    node_name = str(node.__class__.__name__)
    dot.node(str(id(node)), node_name)
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    for child in ast.iter_child_nodes(node):
        add_node(child, node)


# Add nodes to the Digraph
add_node(tree)

# Render the Digraph as a PNG file
dot.format = 'png'
dot.render('my_ast1', view=True)
