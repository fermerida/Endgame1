from instrucciones import Instruccion
from arbol import *
class Mensaje() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, text, linea, columna, iserror,errtype) :
        self.text = text
        self.linea = linea
        self.columna =  columna
        self.iserror = iserror
        self.errtype = errtype

    def constructError(self):
        return "Error " + str(self.errtype) + ": " + str(self.text) + " en linea:" + str(self.linea) + " y columna:"+str(self.columna) + "\n"

    def constructMensaje(self):
        return str(self.text)


class Mensajes() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self) :
        self.mensajes = []
        self.correcto = True

    def AddMensaje(self, mensaje):
        if mensaje.iserror:
            self.correcto = False
        self.mensajes.append(mensaje)

    def GetErrores(self):
        errores =[]
        for Mensaje in self.mensajes:
            if Mensaje.iserror:
                errores.append(Mensaje)
        return errores
    
    def GetMensajes(self):
        mens =[]
        for Mensaje in self.mensajes:
            if Mensaje.iserror == False:
                mens.append(Mensaje)
        return mens

