from instrucciones import Instruccion
import ts as TS
class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, valor, rol) :
        self.id = id
        self.valor = valor
        self.rol = rol

    def ejecutar(self, ts):
        id = ts.obtener(self.id)
        val = self.valor.GetValor(ts)
        if id is not None:
            simbolo = TS.Simbolo(self.id, self.valor.GetTipo(ts), val,self.rol)
            ts.actualizar(simbolo)
            if(id.reference != None):
                reference = ts.obtener(id.reference)
                refsymbol = TS.Simbolo(id.reference, self.valor.GetTipo(ts), val,self.rol)
                ts.actualizar(refsymbol)

        else:
            simbolo = TS.Simbolo(self.id, self.valor.GetTipo(ts), val,self.rol)      # inicializamos con 0 como valor por defecto
            ts.agregar(simbolo)
        
        return None
