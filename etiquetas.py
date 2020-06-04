from instrucciones import Instruccion
from arbol import *
import ts as TS
class Etiqueta() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, instrucciones = []) :
        self.id = id
        self.tipo = tipo
        self.instrucciones = instrucciones
        self.next = None

    
    def ejecutar(self, ts):
        result = None
        for instr in self.instrucciones :
            result = instr.ejecutar(ts)
            if result == False:
               # print("iHere")
                break
        if  (self.next != None) and (result is None) :
           # print("I here too")
            self.next.ejecutar(ts)



    def inicializar(self, ts,next):
        simbolo = TS.Simbolo(self.id, self.tipo, self,"Etiqueta")    
        ts.agregar(simbolo)
        self.next = next

    def actualizar(self, ts,tipo,rol):
        simbolo = TS.Simbolo(self.id, tipo,self,rol)
        ts.actualizar(simbolo)

class ListaEtiqueta() :
    'Esta clase representa la tabla de simbolos'
