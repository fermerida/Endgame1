import gramatica as g
import ts as TS
from instrucciones import *
from arbol import *
from etiquetas import *

def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for i in range(len(instrucciones)) :
        if i < len(instrucciones)-1:
            instrucciones[i].inicializar(ts,instrucciones[i+1])
        else:
            instrucciones[i].inicializar(ts,None)
    for instr in instrucciones :
        if (instr.id=="main"):
            instr.ejecutar(ts)

f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()

procesar_instrucciones(instrucciones, ts_global)
