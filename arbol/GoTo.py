from instrucciones import Instruccion
class GoTo(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  id) :
        self.id = id

    def ejecutar(self, ts):
        
        result = None
        Simbolo = ts.obtener(self.id)
        Etiqueta = Simbolo.valor
        for instr in Etiqueta.instrucciones :
            result = instr.ejecutar(ts)
            if result == False:
                break
        if  (Etiqueta.next != None) and (result is None) :
            Etiqueta.next.ejecutar(ts)
        
        return False

