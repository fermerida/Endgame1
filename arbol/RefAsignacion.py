from instrucciones import Instruccion
import ts as TS
import mensajes as MS

class RefAsignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, reference, rol) :
        self.id = id
        self.reference = reference
        self.rol = rol

    def ejecutar(self, ts,ms):
        id = ts.obtener(self.id)
        reference = ts.obtener(self.reference)
        if id is not None:
            simbolo = TS.Simbolo(self.id, reference.tipo, reference.valor,self.rol)
            simbolo.SetReference(reference.id)
            ts.actualizar(simbolo)
        else:
            simbolo = TS.Simbolo(self.id, reference.tipo, reference.valor,self.rol)      # inicializamos con 0 como valor por defecto
            simbolo.SetReference(reference.id)
            ts.agregar(simbolo)
        
        return None
