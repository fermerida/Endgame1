import AST as AR
from TreeMaker import *

parser = AR.AST()
f = open("./entrada.txt", "r")
input = f.read()
raiz = parser.parse(input)
graf = TreeMaker(raiz)
try:
    graf.crearArbol()
except:
    print ("No se genero el arbol")