from enum import Enum

    
class TIPO_DATO(Enum) :
    INTEGER = 1
    CHAR = 2
    FLOAT = 3
    BOOLEAN = 4
    ARRAY = 5
    STRUCT = 6

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, valor,rol,dim,ambito,declarada) :
        self.id = id
        self.tipo = tipo
        self.valor = valor
        self.rol = rol
        self.reference = None
        self.dim= dim
        self.ambito = ambito
        self.declarada = declarada

    def SetReference(self, id):
        self.reference = id

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = None) :
        if simbolos is None:
            self.simbolos = {}
        else:
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
            print("Simbolo: "+ str(self.simbolos[simbolo].id) + " Tipo: " +str(self.simbolos[simbolo].tipo) +" Rol: "+str(self.simbolos[simbolo].rol)  +" Value:" +str(self.simbolos[simbolo].valor))