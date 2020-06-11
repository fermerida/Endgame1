import ts as TS
import mensajes as MS
class Arreglo() :

    def __init__(self) :
        self.values = {}
        self.isstruct = False
    
    def agregar(self, clave, valor) :
        self.values[clave] = valor

    def GetValor(self,ts,ms):
            return self.__class__()

    def GetElements(self,ts,ms):
            return self.values

    def Recorrer(self,dic):
        for x in dic:
            if isinstance(x, int):
                pass
            else:
                self.isstruct = True


    def GetTipo(self,ts,ms):
        self.Recorrer(self.values)
        if self.isstruct:
            return TS.TIPO_DATO.STRUCT
        else:
            return TS.TIPO_DATO.ARRAY
