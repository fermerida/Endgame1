from enum import Enum
import ts as TS
import mensajes as MS
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
    '''
        Esta clase representa una expresión numérica
    '''
    def GetValor(self,ts,ms):
        pass
    def GetTipo(self,ts,ms):
        pass

class Aritmetica(Exp) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def MaxType(self,a,b):
        if (a == TS.TIPO_DATO.CHAR) or (b == TS.TIPO_DATO.CHAR):
            return TS.TIPO_DATO.CHAR
        else:
            return TS.TIPO_DATO.INTEGER

    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts)
        exp2 = self.exp2.GetValor(ts)
        tipo1 = self.exp1.GetTipo(ts)
        tipo2 = self.exp2.GetTipo(ts)

        maxi = self.MaxType(tipo1,tipo2)

        if maxi == TS.TIPO_DATO.INTEGER:
            if self.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
            if self.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
            if self.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
            if self.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
            if self.operador == OPERACION_ARITMETICA.MODULO : return exp1 % exp2
        elif maxi ==TS.TIPO_DATO.CHAR:
            if self.operador == OPERACION_ARITMETICA.MAS : return str(exp1) + str(exp2)


    def GetTipo(self,ts,ms):
        tipo1 = self.exp1.GetTipo(ts)
        tipo2 = self.exp2.GetTipo(ts)
        return self.MaxType(tipo1,tipo2)


class ExpresionNegativo(Exp) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp

    def GetValor(self,ts,ms):
        exp = self.exp.GetValor(ts,ms)
        return exp * -1
    
    def GetTipo(self,ts,ms):
        return self.exp.GetTipo(ts,ms)

class ExpresionAbsoluto(Exp) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp) :
        self.exp = exp

    def GetValor(self,ts,ms):
        exp = self.exp.GetValor(ts)
        return abs(exp)

    def GetTipo(self,ts,ms):
        return self.exp.GetTipo(ts)

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

class ExpresionFloat(Exp) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

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

    def __init__(self, id = "", accesos=None) :
        self.id = id
        self.accesos = accesos

    def GetName(self,ts,ms):
        return self.id
    
    def CheckInt(self,list, ts,ms):
        isint = True
        intes = []
        for Exp in list:
            if Exp.GetTipo(ts,ms) == TS.TIPO_DATO.INTEGER:
                intes.append(Exp.GetValor(ts,ms))
            else:
                isint=False
        if isint == True:
            return intes
        else:
            None

    def GetValor(self,ts,ms):
        sym = ts.obtener(self.id)

        if sym != None:
            if self.accesos == None:
                if sym.reference == None:
                    return sym.valor
                else:
                    referencia = ts.obtener(sym.reference)
                    if referencia != None:
                        return referencia.valor
            else:
                arreglo = sym.valor
                accesos = self.CheckInt(self.accesos,ts,ms)
                if (accesos is None):
                    return None
                value = arreglo
                level=value
                for i in range(len(accesos)):
                    if i==(len(accesos))-1:
                        #print("fin"+str(i))
                        #obtiene valor
                        if accesos[i] in level:
                            value= level[accesos[i]] 
                        else:
                            print("Error acceso a esta posicion esta vacio")
                    else:
                        if accesos[i] in level:
                            if type(level[accesos[i]]) is dict:
                                #agregar a elemento
                                level = level[accesos[i]]
                            else:
                                #error no se puede acceder a este tipo de elemento
                                print("Error no se puede acceder a este tipo de elemento")
                                break       
                        else:
                            print("Error acceso a esta posicion esta vacio")
                            break   
                return value
        print("No existe esta variable")
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

        
class ExpresionDobleComilla(Exp) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val) :
        self.val = val

    def GetValor(self,ts,ms):
        return self.val

    def GetName(self,ts,ms):
        return self.val

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.CHAR

class ExpresionCadenaNumerico(Exp) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp) :
        self.exp = exp

    def GetValor(self,ts,ms):
        return str(self.exp.GetValor(ts))

class Relacional() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts)
        exp2 = self.exp2.GetValor(ts)
        if self.operador == OPERACION_RELACIONAL.MAYOR : return exp1 > exp2
        if self.operador == OPERACION_RELACIONAL.MENOR : return exp1 < exp2
        if self.operador == OPERACION_RELACIONAL.MAYORIGUAL : return exp1 >= exp2
        if self.operador == OPERACION_RELACIONAL.MENORIGUAL : return exp1 <= exp2
        if self.operador == OPERACION_RELACIONAL.IGUAL : return exp1 == exp2
        if self.operador == OPERACION_RELACIONAL.DIFERENTE : return exp1 != exp2

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.BOOLEAN

class Logica() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts)
        if (self.exp2 != None):
            exp2 = self.exp2.GetValor(ts)
        if self.operador == OPERACION_LOGICA.NOT : return not(exp1)
        if self.operador == OPERACION_LOGICA.AND : return exp1 and exp2
        if self.operador == OPERACION_LOGICA.OR : return exp1 or exp2
        if self.operador == OPERACION_LOGICA.XOR : return (not exp2 and exp1) or (not exp1 and exp2)

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.BOOLEAN


class Bitwise() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def GetValor(self,ts,ms):
        exp1 = self.exp1.GetValor(ts)
        if (self.exp2 !=None):
            exp2 = self.exp2.GetValor(ts)
        if self.operador == OPERACION_BITWISE.BITNOT : return ~(exp1)
        if self.operador == OPERACION_BITWISE.BITAND : return exp1 & exp2
        if self.operador == OPERACION_BITWISE.BITOR : return exp1 | exp2
        if self.operador == OPERACION_BITWISE.BITXOR : return exp1 ^ exp2
        if self.operador == OPERACION_BITWISE.SHIFTL : return exp1 << exp2
        if self.operador == OPERACION_BITWISE.SHIFTR : return exp1 >> exp2

    def GetTipo(self,ts,ms):
        return TS.TIPO_DATO.INTEGER



class ExpConvertida(Exp) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp, tipo) :
        self.exp = exp
        self.tipo = tipo

    def GetValor(self,ts,ms):
        extipo = self.exp.GetTipo(ts,ms)
        exvalor = self.exp.GetValor(ts,ms)
       # print("tipo: "+str(extipo))
       # print("valor: "+str(exvalor))
        if (self.tipo == TS.TIPO_DATO.INTEGER):
            if (extipo == TS.TIPO_DATO.FLOAT):
                return round(exvalor,0)
            if (extipo == TS.TIPO_DATO.CHAR):
                fletter = exvalor[0]
                return ord(fletter)
        elif (self.tipo == TS.TIPO_DATO.FLOAT):
            if (extipo == TS.TIPO_DATO.INTEGER):
                return float(exvalor)
            if (extipo == TS.TIPO_DATO.CHAR):
                fletter = exvalor[0]
                return float(ord(fletter))
        elif(self.tipo == TS.TIPO_DATO.CHAR):
            if (extipo == TS.TIPO_DATO.INTEGER):
                if(exvalor >=0) and (exvalor <=255):
                    return chr(exvalor)
                else:
                    mod = exvalor % 256
                    return chr(mod)
            if (extipo == TS.TIPO_DATO.FLOAT):
                ent = round(exvalor,0)
                if(ent >=0) and (ent <=255):
                    return chr(ent)
                else:
                    mod = ent % 256
                    return chr(mod)

        else:
            print("Error: No se puede convertir a tipo")
            ms.AddMensaje(MS.Mensaje("No se puede convertir a tipo",self.linea,self.columna,True,"Semantico"))

    
    def GetTipo(self,ts,ms):
        return self.tipo

