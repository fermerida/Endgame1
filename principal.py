import gramatica as GR
import ts as TS
import mensajes as MS
from instrucciones import *
from arbol import *
from etiquetas import *
import AST as AR
from TreeMaker import *

def procesar_instrucciones(instrucciones, ts,ms) :
    ## lista de instrucciones recolectadas
    for i in range(len(instrucciones)) :
        if i < len(instrucciones)-1:
            instrucciones[i].inicializar(ts,ms,instrucciones[i+1])
        else:
            instrucciones[i].inicializar(ts,ms,None)
    for instr in instrucciones :
        if (instr.id=="main"):
            instr.ejecutar(ts,ms)
    for instr in instrucciones:
        instr.actualizar(ts)

correct = False
f = open("./entrada.txt", "r")
input = f.read()

print("Iniciando analisis")

ms_global = MS.Mensajes()
parser = GR.Gramatica(ms_global)
instrucciones = parser.parse(input)
#SinLex = parser.Errors()

ts_global = TS.TablaDeSimbolos()


if instrucciones is not None:
        procesar_instrucciones(instrucciones, ts_global, ms_global)

if (ms_global.correcto):
    print("Analisis correcto")
    prints = ms_global.GetMensajes()
    for Mensaje in prints:
        print(Mensaje.constructMensaje())
    arparser = AR.AST()
    raiz = arparser.parse(input)
    graf = TreeMaker(raiz)
    try:
        graf.crearArbol()
    except:
        print ("No se genero el arbol")
else:
    print("Se encontraron errores")
    errores = ms_global.GetErrores()
    '''if (SinLex is not None):
        for Mensaje in SinLex.mensajes:
            print(Mensaje.constructError())'''
    for Mensaje in errores:
        print(Mensaje.constructError())

#ts_global.printts()