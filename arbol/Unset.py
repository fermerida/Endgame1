from instrucciones import Instruccion
from expresiones import *
import mensajes as MS

class Unset(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  var,linea,columna) :
        self.var = var
        self.linea = linea
        self.columna = columna

    def ejecutar(self, ts):
        if ( isinstance(self.var,ExpresionIdentificador)) or ( isinstance(self.var,ExpresionDobleComilla)):
            key = self.var.GetName(ts)
            #print("unsetting" + key)
            ts.eliminar(key)
        else:
            print("Error: unset no se puede manejar con este tipo")
            ms.AddMensaje(MS.Mensaje("Unset no se puede manejar con este tipo",self.linea,self.columna,True,"Semantico"))

        return None

