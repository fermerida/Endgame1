from instrucciones import Instruccion
import ts as TS
from arreglo import *
import mensajes as MS

from enum import Enum

    
class TIPO_REG(Enum) :
    TEMPORAL = 1
    PARAMETRO = 2
    RETVAL = 3
    RETNIV = 4
    PILA = 5
    PUNTERO = 6
    ETIQUETA = 7

class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, var, valor,linea,columna) :
        self.var = var
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.etiqueta = None

    
    def CheckA(self,list, ts,ms):
        isarray = True
        result = []
        for Exp in list:
            result.append(Exp.GetValor(ts,ms))
           
        
            return result
       
    def DefineRol(self,id):
        var = id[0]
        if var == "t":
            # temporal
            return "Temporal"
        elif var == "a":
            #parametro
            return "Parametro"
        elif var == "v":
            #retorno funciones
            return "Retorno de valor"
        elif var == "r":
            #retorno de nivel
            return "Retorno de nivel"
        elif var == "s":
            if id =="sp":
                #pila
                return "Pila"

            else:
                #puntero
                return "Puntero de pila"

        else:
            #hay mas?
            return "Registro"

    def ejecutar(self, ts,ms):
        sym = ts.obtener(self.var.id)
        val = self.valor.GetValor(ts,ms)
        tipo_et=self.DefineRol(self.var.id)
        #print("id: "+str(self.var.id)+" accesos:"+str(self.var.accesos))
        if self.var.accesos == None:
            if sym is not None:
                simbolo = TS.Simbolo(self.var.id, self.valor.GetTipo(ts,ms), val,tipo_et)
                ts.actualizar(simbolo)
                if(sym.reference != None):
                    reference = ts.obtener(sym.reference)
                    refsymbol = TS.Simbolo(sym.reference, self.valor.GetTipo(ts,ms), val,tipo_et)
                    ts.actualizar(refsymbol)

            else:
                if tipo_et == "Parametro":
                    self.etiqueta.rol = "Metodo"
                elif tipo_et =="Retorno de valor":
                    self.etiqueta.rol = "Funcion"
                simbolo = TS.Simbolo(self.var.id, self.valor.GetTipo(ts,ms), val,tipo_et)    
                ts.agregar(simbolo)
        else:
            if sym is not None:
                array = sym.valor
                arreglo=array.values
            else:
                array = Arreglo()
                arreglo = array.values
            accesos = self.CheckA(self.var.accesos,ts,ms)
            value = arreglo
            level=value
            for i in range(len(accesos)):
                if i==(len(accesos))-1:
                    print("fin"+str(i)+str(accesos[i])+str(val)+str(level))
                    #guardar valor
                    level[accesos[i]] = val
                else:
                    if accesos[i] in level:
                        if type(level[accesos[i]]) is dict:
                            #agregar a elemento
                            #print("is instance")
                            level = level[accesos[i]]
                        else:
                            #error no se puede acceder a este tipo de elemento
                            ms.AddMensaje(MS.Mensaje("No se puede acceder a este tipo de elemento",self.linea,self.columna,True,"Semantico"))
                            print("error no se puede acceder a este tipo de elemento")
                            break       
                    else:
                        #iterar o crear
                        #print("I am not" + str(accesos[i]))
                        level[accesos[i]]={}
                        level = level[accesos[i]]
            if array.GetTipo(ts,ms) == TS.TIPO_DATO.ARRAY:
                rol = "Arreglo"
            else:
                rol = "Struct"
            simbolo = TS.Simbolo(self.var.id, array.GetTipo(ts,ms), value,rol)

            if sym is not None:
                ts.actualizar(simbolo)
                if(sym.reference != None):
                    reference = ts.obtener(sym.reference)
                    reference = TS.Simbolo(self.var.id, array.GetTipo(ts,ms), value,"Arreglo")
                    ts.actualizar(refsymbol)
            
            else:
                ts.agregar(simbolo)
                
        
        return None
