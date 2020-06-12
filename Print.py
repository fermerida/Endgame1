from instrucciones import Instruccion
from arreglo import Arreglo
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
            valor = valor.GetElements(ts,ms)
            #print("si es"+str(valor))

        if (valor != None):
            formatted = str(valor).replace('\\n','\n')
            ms.AddMensaje(MS.Mensaje(formatted,self.linea,self.columna,False,None))
            #print(ts.printts())
        else:
            #print("Error: Variable a imprimir no tiene valor")
            ms.AddMensaje(MS.Mensaje("Variable a imprimir no tiene valor",self.linea,self.columna,True,"Semantico"))
        return None

