from instrucciones import Instruccion
import mensajes as MS

class Exit(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self) :
        pass

    def ejecutar(self, ts,ms):
        return False

