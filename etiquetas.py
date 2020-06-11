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
        self.rol = "Sentencia de control"

    
    def ejecutar(self, ts,ms):
        result = None
        for instr in self.instrucciones :
            instr.etiqueta = self
            result = instr.ejecutar(ts,ms)
            if result == False:
               # print("iHere")
                break
        if  (self.next != None) and (result is None) :
           # print("I here too")
            self.next.ejecutar(ts,ms)



    def inicializar(self, ts,ms,next):
        simbolo = TS.Simbolo(self.id, "Etiqueta", self,"Etiqueta")    
        ts.agregar(simbolo)
        self.next = next

    def actualizar(self,ts):
        simbolo = TS.Simbolo(self.id,"Etiqueta", self,self.rol)
        ts.actualizar(simbolo)

class ListaEtiqueta() :
    'Esta clase representa la tabla de simbolos'
