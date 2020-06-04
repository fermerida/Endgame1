from instrucciones import Instruccion
from expresiones import *
class Unset(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  var) :
        self.var = var

    def ejecutar(self, ts):
        if ( isinstance(self.var,ExpresionIdentificador)) or ( isinstance(self.var,ExpresionDobleComilla)):
            key = self.var.GetName(ts)
            #print("unsetting" + key)
            ts.eliminar(key)
        else:
            print("Error: unset no se puede manejar con este tipo")
        return None

