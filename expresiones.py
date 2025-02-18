from enum import Enum
import ts as TS
import mensajes as MS
import sys

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    MODULO = 5

class OPERACION_RELACIONAL(Enum) :
    MAYOR = 1
    MENOR = 2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    IGUAL = 5
    DIFERENTE = 6
    
class OPERACION_LOGICA(Enum) :
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4

class OPERACION_BITWISE(Enum) :
    BITNOT = 1
    BITAND = 2
    BITOR = 3
    BITXOR = 4
    SHIFTL = 5
    SHIFTR = 6

class Exp:

    def GetValor(self,ts,ms):
        pass
    def GetTipo(self,ts,ms):
        pass

class Aritmetica(Exp) :
 

    def __init__(self, exp1, exp2, operador,linea, columna) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna
    
    def MaxType(self,a,b):
        if (a == TS.TIPO_DATO.CHAR) or (b == TS.TIPO_DATO.CHAR):
            return TS.TIPO_DATO.CHAR
        else:
            return TS.TIPO_DATO.INTEGER

    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts,ms)
        exp2 = self.exp2.GetValor(ts,ms)
        tipo1 = self.exp1.GetTipo(ts,ms)
        tipo2 = self.exp2.GetTipo(ts,ms)

        maxi = self.MaxType(tipo1,tipo2)
        if (exp1 is not None) and (exp2 is not None):
            if maxi == TS.TIPO_DATO.INTEGER:
                if self.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
                if self.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
                if self.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
                if self.operador == OPERACION_ARITMETICA.DIVIDIDO : 
                    if exp2 != 0:
                        return exp1 / exp2
                    else:
                        print("No es posible dividr entre 0")
                        ms.AddMensaje(MS.Mensaje("No es posible dividir entre 0",self.linea,self.columna,True,"Semantico"))
                        return exp2
                if self.operador == OPERACION_ARITMETICA.MODULO : return exp1 % exp2
            elif maxi ==TS.TIPO_DATO.CHAR:
                if self.operador == OPERACION_ARITMETICA.MAS : return str(exp1) + str(exp2)
        else:
            print("Expresion en numero entero no tiene valor")
            ms.AddMensaje(MS.Mensaje("Expresion en numero entero no tiene valor",self.linea,self.columna,True,"Semantico"))


    def GetTipo(self,ts,ms):
        tipo1 = self.exp1.GetTipo(ts,ms)
        tipo2 = self.exp2.GetTipo(ts,ms)
        return self.MaxType(tipo1,tipo2)


class ExpresionNegativo(Exp) :
 
    def __init__(self, exp) :
        self.exp = exp

    def GetValor(self,ts,ms):
        exp = self.exp.GetValor(ts,ms)
        return exp * -1
    
    def GetTipo(self,ts,ms):
        return self.exp.GetTipo(ts,ms)

class ExpresionAbsoluto(Exp) :

    def __init__(self, exp) :
        self.exp = exp

    def GetValor(self,ts,ms):
        exp = self.exp.GetValor(ts,ms)
        return abs(exp)

    def GetTipo(self,ts,ms):
        return self.exp.GetTipo(ts,ms)

class ExpresionInteger(Exp) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0) :
        self.val = val


    def GetValor(self,ts,ms):
        return self.val; 

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.INTEGER

class RandomList(Exp) :
  

    def __init__(self, values) :
        self.values = values


    def GetValor(self,ts,ms):
        return self.__class__(self.values) 

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.ARRAY
class ExpresionFloat(Exp) :


    def __init__(self, val = 0) :
        self.val = val


    def GetValor(self,ts,ms):
        return self.val; 

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.FLOAT

class Variable(Exp) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id = "", accesos=None,linea=0, columna=0) :
        self.id = id
        self.accesos = accesos
        self.linea = linea
        self.columna = columna

    def GetName(self,ts,ms):
        return self.id
    
    def GetAccesos(self,list, ts,ms):
        expes = []
        for Exp in list:
            expes.append(Exp.GetValor(ts,ms))
        return expes

    def CheckInt(self,list, ts,ms):
        isint = True
        for Exp in list:
            if Exp.GetTipo(ts,ms) != TS.TIPO_DATO.INTEGER:
                isint=False
        return isint
        


    def GetValor(self,ts,ms):
        sym = ts.obtener(self.id)

        if sym != None:
            if self.accesos == None:
                if sym.reference == None:
                    return sym.valor
                else:
                    referencia = ts.obtener(sym.reference)
                    refsymbol = TS.Simbolo(self.id, referencia.tipo, referencia.valor,referencia.rol,referencia.dim,sym.ambito,sym.declarada)
                    ts.actualizar(refsymbol)
                    if referencia != None:
                        return referencia.valor
            else:
                accesos = self.GetAccesos(self.accesos,ts,ms)
                isint = self.CheckInt(self.accesos,ts,ms)
                recorrido = ""
                if (accesos is None):
                    print("Error obteniendo los accesos")
                    ms.AddMensaje(MS.Mensaje("Error obteniendo los accesos",self.linea,self.columna,True,"Semantico"))
                    return None
                if (sym.tipo== TS.TIPO_DATO.ARRAY) or (sym.tipo == TS.TIPO_DATO.STRUCT):
                    arreglo = sym.valor
                    
                    value = arreglo
                    level=arreglo.values
                    
                    #print("levels: "+str(level)+" from:"+ self.id)
                    for i in range(len(accesos)):
                        if i==(len(accesos))-1:
                            #print("fin"+str(i))
                            #obtiene valor
                            recorrido+=str(accesos[i])
                            if accesos[i] in level:
                                if sym.reference is None:
                                    value= level[accesos[i]] 
                                else:
                                    if sym.posicion is  not None:
                                        if recorrido in sym.posicion:
                                            refs = ts.obtener(sym.posicion[recorrido])

                                            value = refs.valor
                                            level[accesos[i]] = value
                                        else:
                                            value= level[accesos[i]]
                                    else:
                                        value= level[accesos[i]] 
                            else:
                                print("Error acceso a esta posicion esta vacios")
                                ms.AddMensaje(MS.Mensaje("Error acceso a esta posicion esta vacios",self.linea,self.columna,True,"Semantico"))

                        else:
                            recorrido+=str(accesos[i])
                            if accesos[i] in level:
                                if isinstance(level[accesos[i]],dict):
                                    #agregar a elemento
                                    level = level[accesos[i]]
                                elif isinstance(level[accesos[i]],str):
                                    if i + 2== len(accesos):
                                        if isint:
                                            if accesos[i+1] < len(level[accesos[i]]):
                                                #print("una cadenita:"+str(i))
                                                return level[accesos[i]][accesos[i+1]]
                                            else:
                                                print("Posicion mayor a cadena")
                                                ms.AddMensaje(MS.Mensaje("Posicion mayor a cadena",self.linea,self.columna,True,"Semantico"))
                                        else:
                                            print("Solo se puede acceder con un numero a una cadena")
                                            ms.AddMensaje(MS.Mensaje("Solo se puede acceder con un numero a una cadena",self.linea,self.columna,True,"Semantico"))

                                    else:
                                        print("Error no se puede acceder a este tipo de elemento")
                                        ms.AddMensaje(MS.Mensaje("Error no se puede acceder a este tipo de elemento",self.linea,self.columna,True,"Semantico"))
                                else:
                                    #error no se puede acceder a este tipo de elemento
                                    print("Error no se puede acceder a este tipo de elemento")
                                    ms.AddMensaje(MS.Mensaje("Error no se puede acceder a este tipo de elemento",self.linea,self.columna,True,"Semantico"))

                                    break       
                            else:
                                print("Error acceso a esta posicion esta vacio")
                                ms.AddMensaje(MS.Mensaje("Error acceso a esta posicion esta vacio",self.linea,self.columna,True,"Semantico"))
                                break   
                    return value
                elif sym.tipo == TS.TIPO_DATO.CHAR:
                    if len(accesos)==1:
                        if isint:
                            if accesos[0] < len(sym.valor):
                                return sym.valor[accesos[0]]
                            else:
                                print("Posicion mayor a cadena")
                                ms.AddMensaje(MS.Mensaje("Posicion mayor a cadena",self.linea,self.columna,True,"Semantico"))

                        else:
                            print("Solo se puede acceder con un numero a una cadena") 
                            ms.AddMensaje(MS.Mensaje("Solo se puede acceder con un numero a una cadena",self.linea,self.columna,True,"Semantico"))
                    else:
                        print("No se puede acceder multiples veces a una cadena")
                        ms.AddMensaje(MS.Mensaje("No se puede acceder multiples veces a una cadena",self.linea,self.columna,True,"Semantico"))

                else:
                    print("No se puede aceeder a una variable con este tipo")
                    ms.AddMensaje(MS.Mensaje("No se puede aceeder a una variable con este tipo",self.linea,self.columna,True,"Semantico"))


        print("No existe esta variable")
        ms.AddMensaje(MS.Mensaje("No existe esta variable",self.linea,self.columna,True,"Semantico"))

        return None

    def GetTipo(self,ts,ms):
        var = ts.obtener(self.id)
        if var != None:
            if var.reference == None:
                return var.tipo
            else:
                referencia = ts.obtener(var.reference)
                if referencia != None:
                    return referencia.tipo
        return None

        
class ExpresionCadena(Exp) :


    def __init__(self, val) :
        self.val = val

    def GetValor(self,ts,ms):
        return self.val

    def GetName(self,ts,ms):
        return self.val

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.CHAR



class Relacional() :


    def __init__(self, exp1, exp2, operador,linea,columna) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        self.linea = linea
        self.columna = columna
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts,ms)
        exp2 = self.exp2.GetValor(ts,ms)
        if (exp1 is not None) and (exp2 is not None):
            if self.operador == OPERACION_RELACIONAL.MAYOR : return exp1 > exp2
            if self.operador == OPERACION_RELACIONAL.MENOR : return exp1 < exp2
            if self.operador == OPERACION_RELACIONAL.MAYORIGUAL : return exp1 >= exp2
            if self.operador == OPERACION_RELACIONAL.MENORIGUAL : return exp1 <= exp2
            if self.operador == OPERACION_RELACIONAL.IGUAL : return exp1 == exp2
            if self.operador == OPERACION_RELACIONAL.DIFERENTE : return exp1 != exp2
        else:
            print("Uno de los valores para la operacion relacional no fue declarado")
            ms.AddMensaje(MS.Mensaje("Uno de los valores para la operacion relacional no fue declarado",self.linea,self.columna,True,"Semantico"))

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.BOOLEAN

class Logica() :


    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts,ms)
        if (self.exp2 != None):
            exp2 = self.exp2.GetValor(ts,ms)
        if exp1 is not None:
            if self.operador == OPERACION_LOGICA.NOT : return not(exp1)
            if self.operador == OPERACION_LOGICA.AND : return exp1 and exp2
            if self.operador == OPERACION_LOGICA.OR : return exp1 or exp2
            if self.operador == OPERACION_LOGICA.XOR : return (not exp2 and exp1) or (not exp1 and exp2)
        else:
            print("Operacion logica no tiene un valor")

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.BOOLEAN


class Bitwise() :


    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts,ms)
        if (self.exp2 !=None):
            exp2 = self.exp2.GetValor(ts,ms)
        if self.operador == OPERACION_BITWISE.BITNOT : return ~(exp1)
        if self.operador == OPERACION_BITWISE.BITAND : return exp1 & exp2
        if self.operador == OPERACION_BITWISE.BITOR : return exp1 | exp2
        if self.operador == OPERACION_BITWISE.BITXOR : return exp1 ^ exp2
        if self.operador == OPERACION_BITWISE.SHIFTL : return exp1 << exp2
        if self.operador == OPERACION_BITWISE.SHIFTR : return exp1 >> exp2

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.INTEGER



class ExpConvertida(Exp) :

    def __init__(self, exp, tipo,linea,columna) :
        self.exp = exp
        self.tipo = tipo
        self.linea =linea
        self.columna = columna

    def GetValor(self,ts,ms):
        extipo = self.exp.GetTipo(ts,ms)
        exvalor = self.exp.GetValor(ts,ms)
       # print("tipo: "+str(extipo))
       # print("valor: "+str(exvalor))
        if (self.tipo == TS.TIPO_DATO.INTEGER):
            if (extipo == TS.TIPO_DATO.FLOAT):
                return round(exvalor,0)
            elif (extipo == TS.TIPO_DATO.INTEGER):
                return exvalor
            elif (extipo == TS.TIPO_DATO.CHAR):
                fletter = exvalor[0]
                return ord(fletter)
            elif (extipo == TS.TIPO_DATO.ARRAY):
                fletter = self.GetFirst(exvalor.values)
                return ExpConvertida(fletter,self.tipo,self.linea,self.columna).GetValor(ts,ms)
            else:
                ms.AddMensaje(MS.Mensaje("No se puede convertir a tipo",self.linea,self.columna,True,"Semantico"))
                return None
        elif (self.tipo == TS.TIPO_DATO.FLOAT):
            if (extipo == TS.TIPO_DATO.INTEGER):
                return float(exvalor)
            elif (extipo == TS.TIPO_DATO.FLOAT):
                return exvalor
            elif (extipo == TS.TIPO_DATO.CHAR):
                fletter = exvalor[0]
                return float(ord(fletter))
            elif (extipo == TS.TIPO_DATO.ARRAY):
                fletter = self.GetFirst(exvalor.values)
                return ExpConvertida(fletter,self.tipo,self.linea,self.columna).GetValor(ts,ms)
            else:
                ms.AddMensaje(MS.Mensaje("No se puede convertir a tipo",self.linea,self.columna,True,"Semantico"))
                return None
        elif(self.tipo == TS.TIPO_DATO.CHAR):
            if (extipo == TS.TIPO_DATO.INTEGER):
                if(exvalor >=0) and (exvalor <=255):
                    return chr(exvalor)
                else:
                    mod = exvalor % 256
                    return chr(mod)
            elif (extipo == TS.TIPO_DATO.FLOAT):
                ent = round(exvalor,0)
                if(ent >=0) and (ent <=255):
                    return chr(ent)
                else:
                    mod = ent % 256
                    return chr(mod)
            elif (extipo == TS.TIPO_DATO.CHAR):
                fletter = exvalor[0]
                return ord(fletter)
            elif (extipo == TS.TIPO_DATO.ARRAY):
                fletter = self.GetFirst(exvalor.values)
                return ExpConvertida(fletter,self.tipo,self.linea,self.columna).GetValor(ts,ms)
            else:
                ms.AddMensaje(MS.Mensaje("No se puede convertir a tipo",self.linea,self.columna,True,"Semantico"))
                return None

        else:
            print("Error: No se puede convertir a tipo")
            ms.AddMensaje(MS.Mensaje("No se puede convertir a tipo",self.linea,self.columna,True,"Semantico"))

    
    def GetTipo(self,ts,ms):
        return self.tipo
    
    def GetFirst(self,elementos):
        i=0
        returnee = 0
        while i < 100:
            if i in elementos:
                returnee= elementos[i]
                break
            i+=1
        if isinstance(returnee, int):
            return ExpresionInteger(returnee)
        elif isinstance(returnee, float):
            return ExpresionFloat(returnee)
        
        elif isinstance(returnee, dict):
            return RandomList(returnee)
        else:
            return ExpresionCadena(returnee)

