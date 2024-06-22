import ast
from astunparse import unparse
from json import dumps
from treediffer import treediff
import treediffer


RESET = '\33[0m'  # Reset style
ADD = '\33[32m'  # green
DEL = '\33[9;31m'  # striked out, red
MOVED = '\33[36m' # blue
ALTERED = '\33[35m' # NSEI
def read(filename):
    with open(filename, 'r') as file:
        return file.read()


a = read('code1.py')
parsed_tree_a = ast.parse(a)
#print(ast.dump(parsed_tree_a, indent=4))
body = parsed_tree_a.body
b = read('code2.py')
parsed_tree_b = ast.parse(b)
# print(ast.dump(parsed_tree_b, indent=4))
body2 = parsed_tree_b.body


def menorEntre(body, body2):
    menor = body
    if len(body) > len(body2):
        menor = body2
    return len(menor)


'''
def lcs(seq1, seq2):
    matrix = [[0 for i in range(len(seq2))] for j in range(len(seq1))]

    for i in range(1, len(seq1)):
        for j in range(1, len(seq2)):
            if type(seq1[i]) == type(seq2[j]):
                matrix[i][j] = matrix[i-1][j-1] + 1
            else:
                matrix[i][j] = max(matrix[i][j-1], matrix[i-1][j])

    return matrix


matrix = lcs(body, body2)
print(matrix)
'''

lista = []


def TipoDef(body, body2):
    if (body.name == body2.name): 
        nomeControle = "igual"
    else: 
        nomeControle = "diferente"
    
    if (nomeControle == "diferente"):
        if (len(body.body) != len(body2.body)):
            return 0
    
    if (nomeControle == "igual"):
        if (len(body.body) != len(body2.body)):
            return 2
        if (len(body.body) == len(body2.body)):
            if (unparse(body.body) != unparse(body2.body)):
                return 2
            return 1
    return 0            

def TipoIf(body, body2):
    if (body.test.left.id == body2.test.left.id):
        testeControle = "igual"
    else:
        testeControle = "diferente"
    
    if ((testeControle == "diferente") and len(body.body) != len(body2.body)):
        return 0
    if (testeControle == "igual"):
        if(len(body.body) == len(body2.body)):
            if (unparse(body.body) != unparse(body2.body)):
                return 2
            return 1
        if(len(body.body) != len(body2.body)):
            return 2
    return 0

def TipoWhile():
    print()

def isIn(body, body2, i):
    for j in range (len(body2)):
        if (type(body) == type(body2[j])):
            if (isinstance(body, ast.FunctionDef)):
                if (TipoDef(body, body2[j]) == 1):
                    if (i==j):
                        return 1
                    else: 
                        return 2
                if (TipoDef(body, body2[j]) == 2):
                    return 3
            if (isinstance(body, ast.If) or isinstance(body, ast.While)):
                if (TipoIf(body, body2[j]) == 1):
                    if (i==j):
                        return 1
                    else: 
                        return 2
                if (TipoIf(body, body2[j]) == 2):
                    return 4
    return 0        
                    


def Iterator(body, body2):
    for i in range (len(body2)):
        h = isIn(body2[i], body, i)
        if (h == 0):
            lista.append(ADD + unparse(body2[i])+RESET)   
        if (h==1): 
            lista.append(unparse(body2[i]))
        if (h==2):
            lista.append(MOVED + unparse(body2[i]) + RESET)
        if (h==3):
            lista.append(ALTERED +  "função " + body2[i].name + " teve seu corpo alterado" + RESET + '\n')
        if (h ==4):
            if (isinstance(body2[i], ast.If)):
                lista.append(ALTERED +  "if" + unparse(body2[i].test)+ "teve seu corpo alterado" + RESET)
            if (isinstance(body2[i], ast.While)):
                lista.append(ALTERED +  "while" + unparse(body2[i].test)+ "teve seu corpo alterado" + RESET)
    for i in range (len(body)):
        j = isIn(body[i], body2, i)
        if (j == 0):
            lista.insert(i, DEL + unparse(body[i])+RESET) 
        

     
Iterator(body, body2)                    

for i in lista:
    print(i)                  

                    


# # Convert the AST back to Python code
#python_code = unparse(parsed_tree_b.body[0].body)

# # Print the Python code
#print(python_code)
