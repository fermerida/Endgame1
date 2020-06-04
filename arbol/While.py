from instrucciones import Instruccion
import ts as TS
class While(Instruccion) :
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones
    
    def ejecutar(self, ts):
        while self.expLogica.GetValor(ts) :
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            for instr in self.instrucciones :
                instr.ejecutar(ts_local)
