from instrucciones import Instruccion
from Asignacion import *
import ts as TS
import globalvar as GLO

class Etiqueta() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, instrucciones = [],linea=0, columna=0) :
        self.id = id
        self.tipo = tipo
        self.instrucciones = instrucciones
        self.next = None
        self.rol = "Sentencia de control"
        self.linea = linea
        self.columna = columna
        GLO.pila +=1
        self.pila = GLO.pila

    def Declaradaen(self):
        declarada = {}
        declarada["linea"] = str(self.linea)    
        declarada["columna"] = str(self.columna)    
        declarada["pila"] = str(self.pila)  
        return declarada  

    def ejecutar(self, ts,ms):
        result = None
        for instr in self.instrucciones :
            if isinstance(instr,Asignacion):
                instr.etiqueta = self
            result = instr.ejecutar(ts,ms)
            if result == False:
               # print("iHere")
                break
        if  (self.next != None) and (result is None) :
           # print("I here too")
            self.next.ejecutar(ts,ms)

    def debuggear(self, ts,ms):
        result = None
        for instr in self.instrucciones :
            if isinstance(instr,Asignacion):
                instr.etiqueta = self
            result = instr.ejecutar(ts,ms)
            if result == False:
               # print("iHere")
                break
        if  (self.next != None) and (result is None) :
           # print("I here too")
            self.next.ejecutar(ts,ms)


    def inicializar(self, ts,ms,next):
        declarada = self.Declaradaen()
        simbolo = TS.Simbolo(self.id, "Etiqueta", self,"Etiqueta",0,"Global",declarada)    
        ts.agregar(simbolo)
        self.next = next

    def actualizar(self,ts):
        declarada = self.Declaradaen()
        simbolo = TS.Simbolo(self.id,"Etiqueta", self,self.rol,0,"Global",declarada)
        ts.actualizar(simbolo)

class ListaEtiqueta() :
    'Esta clase representa la tabla de simbolos'
