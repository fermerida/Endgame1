from instrucciones import Instruccion
class Exit(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self) :
        pass

    def ejecutar(self, ts):
        return False

