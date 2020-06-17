from instrucciones import Instruccion
import ts as TS
from arreglo import *
import mensajes as MS
import globalvar as GLO

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
        self.pila = 0

    
    def CheckA(self,list, ts,ms):
        isarray = True
        result = []
        for Exp in list:
            result.append(Exp.GetValor(ts,ms))
           
        return result
    
    def CheckInt(self,list, ts,ms):
        isint = True
        for Exp in list:
            if Exp.GetTipo(ts,ms) != TS.TIPO_DATO.INTEGER:
                isint=False
        return isint

    def Declaradaen(self):
        declarada = {}
        declarada["linea"] = str(self.linea)    
        declarada["columna"] = str(self.columna)    
        declarada["pila"] = str(GLO.pila)  
        return declarada  
       
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
                return "Puntero de pila"

            else:
                #puntero
                return "Pila"

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
                GLO.pila = GLO.pila +1
                self.pila = GLO.pila
                declarada = self.Declaradaen()
                simbolo = TS.Simbolo(self.var.id, self.valor.GetTipo(ts,ms), val,tipo_et,1,self.etiqueta.id,declarada)
                
                if(sym.reference != None):
                    reference = ts.obtener(sym.reference)
                    if reference.posicion is None:
                        refsymbol = TS.Simbolo(sym.reference, self.valor.GetTipo(ts,ms), val,tipo_et,1,self.etiqueta.id,declarada)
                        simbolo.SetReference(sym.reference)
                        ts.actualizar(refsymbol)
                    
                ts.actualizar(simbolo)

            else:
               
                if tipo_et == "Parametro":
                    self.etiqueta.rol = "Metodo"
                elif tipo_et =="Retorno de valor":
                    self.etiqueta.rol = "Funcion"
                GLO.pila = GLO.pila +1
                self.pila = GLO.pila
                declarada = self.Declaradaen()
                simbolo = TS.Simbolo(self.var.id, self.valor.GetTipo(ts,ms), val,tipo_et,1,self.etiqueta.id,declarada)    
                ts.agregar(simbolo)
        else:
            if sym is not None:
                if (sym.tipo == TS.TIPO_DATO.ARRAY) or (sym.tipo == TS.TIPO_DATO.STRUCT):
                    array = sym.valor
                    arreglo=array.values
                else:
                    print("Este temporal ya contiene un dato")
                    ms.AddMensaje(MS.Mensaje("Este temporal ya contiene un dato",self.linea,self.columna,True,"Semantico"))
                    return None
            else:
                array = Arreglo()
                arreglo = array.values
            accesos = self.CheckA(self.var.accesos,ts,ms)
            isint = self.CheckInt(self.var.accesos,ts,ms)
            level=arreglo
            for i in range(len(accesos)):
                #print("lenght: "+str(len(accesos)))
                if i==(len(accesos))-1:
                    #print("fin"+str(i)+str(accesos[i])+str(val)+str(level))
                    #guardar valor
                    level[accesos[i]] = val
                else:
                    if accesos[i] in level:
                        if type(level[accesos[i]]) is dict:
                            #agregar a elemento
                            #print("is instance")
                            level = level[accesos[i]]
                        elif isinstance(level[accesos[i]],str):
                                    if i + 2== len(accesos):
                                        if isinstance(accesos[i+1],int):
                                            if accesos[i+1] < len(level[accesos[i]]):
                                                #print("una cadenita:"+str(i))
                                                level[accesos[i]] = level[accesos[i]][:accesos[i+1]] + str(val) + level[accesos[i]][accesos[i+1]+1:] 
                                                break
                                            else:
                                                r = len(level[accesos[i]])
                                                adding = ""
                                                while r < accesos[i+1]:
                                                    adding = adding + " "
                                                    r+=1
                                                adding += str(val)
                                                level[accesos[i]] = level[accesos[i]] + adding
                                        else:
                                            print("Solo se puede acceder con un numero a una cadena")
                                            ms.AddMensaje(MS.Mensaje("Solo se puede acceder con un numero a una cadena",self.linea,self.columna,True,"Semantico"))
                                    else:
                                        print("Error no se puede acceder a este tipo de elemento")
                                        ms.AddMensaje(MS.Mensaje("Error no se puede acceder a este tipo de elemento",self.linea,self.columna,True,"Semantico"))
                        else:
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
            dim = len(accesos)
            GLO.pila = GLO.pila + dim + len(array.values)
            self.pila = GLO.pila
            declarada = self.Declaradaen()
            simbolo = TS.Simbolo(self.var.id, array.GetTipo(ts,ms), array,tipo_et,dim,self.etiqueta.id,declarada)

            if sym is not None:
                ts.actualizar(simbolo)
                if(sym.reference != None):
                    reference = ts.obtener(sym.reference)
                    refsymbol = TS.Simbolo(reference, array.GetTipo(ts,ms), array,tipo_et,dim,self.etiqueta.id,declarada)
                    ts.actualizar(refsymbol)
            
            else:
                ts.agregar(simbolo)
                
        
        return None
