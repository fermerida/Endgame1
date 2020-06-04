from instrucciones import Instruccion
class Print(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  cad) :
        self.cad = cad

    def ejecutar(self, ts):
        valor = self.cad.GetValor(ts)
        if (valor != None):
            print(self.cad.GetValor(ts))
            #print(ts.printts())
        else:
            print("Error: Variable a imprimir no tiene valor")
        return None

