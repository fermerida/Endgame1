from instrucciones import Instruccion
import ts as TS
import mensajes as MS

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica, instrIfVerdadero,linea,columna) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, ts,ms):
        val =self.expLogica.GetValor(ts,ms)
        if val :
            ret = self.instrIfVerdadero.ejecutar(ts,ms)    
            if ret == False:
                return False
      
        return None
