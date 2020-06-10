from instrucciones import Instruccion
import ts as TS
class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfVerdadero) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
    
    def ejecutar(self, ts,ms):
        val =self.expLogica.GetValor(ts)
        if val :
            ret = self.instrIfVerdadero.ejecutar(ts)    
            if ret == False:
                return False     
   
        return None
