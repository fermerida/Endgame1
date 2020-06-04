from enum import Enum

    
class TIPO_DATO(Enum) :
    INTEGER = 1
    STRING = 2
    FLOAT = 3
    BOOLEAN = 4
    ARRAY = 5

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, valor,rol) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.rol = rol
        self.reference = None

    def SetReference(self, id):
        self.reference = id

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def eliminar(self, id) :
        if not id in self.simbolos :
            return None

        self.simbolos.pop(id)

    def obtener(self, id) :
        if not id in self.simbolos :
            return None

        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo

    def printts(self) :
        for simbolo in self.simbolos:
            print("Simbolo: "+ str(self.simbolos[simbolo].id) + " Value:" +str(self.simbolos[simbolo].valor))