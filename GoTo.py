from instrucciones import *
from etiquetas import *
import mensajes as MS

class GoTo(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  id,linea, columna) :
        self.id = id
        self.linea = linea
        self.columna = columna

    def ejecutar(self, ts,ms):
        #ts.printts()
        result = None
        Simbolo = ts.obtener(self.id)
        et = Simbolo.valor
        if  isinstance(et, Etiqueta):
            for instr in et.instrucciones :
                if isinstance(instr,Asignacion):
                    instr.etiqueta = et
                result = instr.ejecutar(ts,ms)
                if result == False:
                    break
            if  (et.next != None) and (result is None) :
                et.next.ejecutar(ts,ms)
        else:
            ms.AddMensaje(MS.Mensaje("El salto no se dirige hacia una etiqueta",self.linea,self.columna,True,"Semantico"))

        
        
        return False

