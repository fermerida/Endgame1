from instrucciones import Instruccion
from arreglo import *
import mensajes as MS
class Print(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  cad,linea,columna) :
        self.cad = cad
        self.linea= linea
        self.columna =columna

    def ejecutar(self, ts,ms):
        valor = self.cad.GetValor(ts,ms)
        if isinstance(valor,Arreglo):
            print("si es")
            valor = valor.GetElements(ts,ms)

        if (valor != None):
            ms.AddMensaje(MS.Mensaje(self.cad.GetValor(ts,ms),self.linea,self.columna,False,None))
            #print(self.cad.GetValor(ts,ms))
            #print(ts.printts())
        else:
            #print("Error: Variable a imprimir no tiene valor")
            ms.AddMensaje(MS.Mensaje("Variable a imprimir no tiene valor",self.linea,self.columna,True,"Semantico"))
        return None

