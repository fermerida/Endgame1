
import ply.lex as lex
import ply.yacc as yacc
from Print import *
from Unset import *
from Asignacion import *
from RefAsignacion import *
from Exit import *
from GoTo import *
from Read import *
from If import *
from expresiones import *
from instrucciones import *
from etiquetas import *
from ts import *
from arreglo import*

class Gramatica():
    
    def __init__(self,ms_gramatica) :
        self.ms_gramatica = ms_gramatica
        self.input = ""



    reservadas = {
        'int'  : 'wint',
        'char' : 'wchar',
        'float': 'wfloat',
        'goto' : 'wgoto',
        'print': 'wprint',
        'exit' : 'wexit',
        'read' : 'wread',
        'unset': 'wunset',
        'abs'  : 'wabs',
        'xor'  : 'wxor',
        'if'  : 'wif',
        'array'  : 'warray'
    }

    tokens  = [
        'dollar',
        'ptocoma',
        'dosp',
        'parea',
        'parec',
        'corcha',
        'corchc',
        'igual',
        'mas',
        'menos',
        'por',
        'dividido',
        'modulo',
        'lnot',
        'land',
        'lor',
        'bnot',
        'band',
        'bor',
        'bxor',
        'bshiftl',
        'bshiftr',
        'menor',
        'mayor',
        'menorigual',
        'mayorigual',
        'igualdad',
        'diferente',
        'DECIMAL',
        'ENTERO',
        'CADENA',
        'CHAR',
        'ID'
    ] + list(reservadas.values())

    # Tokens
    t_dollar     = r'\$'
    t_ptocoma    = r';'
    t_dosp       = r':'
    t_parea      = r'\('
    t_parec      = r'\)'
    t_corcha      = r'\['
    t_corchc      = r'\]'
    t_igual      = r'='
    t_mas        = r'\+'
    t_menos      = r'-'
    t_por        = r'\*'
    t_dividido   = r'/'
    t_modulo     = r'%'
    t_lnot       = r'!'
    t_land       = r'&&'
    t_lor        = r'\|\|'
    t_bnot       = r'~'
    t_band       = r'&'
    t_bor        = r'\|'
    t_bxor       = r'\^'
    t_bshiftl    = r'<<'
    t_bshiftr    = r'>>'
    t_menor      = r'<'
    t_mayor      = r'>'
    t_menorigual = r'<='
    t_mayorigual = r'>='
    t_igualdad   = r'=='
    t_diferente  = r'!='

    def t_DECIMAL(self,t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        return t

    def t_ENTERO(self,t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reservadas.get(t.value.lower(),'ID')    # Check for reserved words
        return t

    def t_CADENA(self,t):
        r'\".*?\"'
        t.value = t.value[1:-1] # remuevo las comillas
        return t 

    def t_CHAR(self,t):
        r'\'.*?\''
        t.value = t.value[1:-1] # remuevo las comillas
        return t 

    # Comentario de múltiples líneas /* .. */
    def t_COMENTARIO_MULTILINEA(self,t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    # Comentario simple // ...
    def t_COMENTARIO_SIMPLE(self,t):
        r'\#.*\n'
        t.lexer.lineno += 1

    # Caracteres ignorados
    t_ignore = " \t"

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0]+"column" +str(self.find_column(self.input,t)))
        self.ms_gramatica.AddMensaje(MS.Mensaje("Caracter no encontrado: "+str(t.value[0]),t.lineno,self.find_column(self.input,t),True,"Lexico"))

        t.lexer.skip(1)

    # Construyendo el analizador léxico

    def build(self,**kwargs):
        self.errors = []
        return  lex.lex(module=self, **kwargs)


    # Asociación de operadores y precedencia
    precedence = (
        ('right','igual'),
        ('left','lor'),
        ('left','land'),
        ('left','bor'),
        ('left','wxor'),
        ('left','bxor'),
        ('left','band'),
        ('left','igualdad','diferente'),
        ('left','menor','mayor','menorigual','mayorigual'),
        ('left','bshiftl','bshiftr'),
        ('left','mas','menos'),
        ('left','por','dividido','modulo'),
        ('right','Umenos','lnot','bnot'),
        ('left','parea','parec','corcha','corchc'),
        )

    # Definición de la gramática
    def find_column(self,input,token):
        last_cr = input.rfind('\n',0,token.lexpos)+1
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    def p_INI(self,t) :
        'INI            : LETS'
        t[0] = t[1]
        GLO.gramatica[1] = GLO.gram[1]

    def p_LETS_lista(self,t) :
        'LETS    : LETS ET'
        t[1].append(t[2])
        t[0] = t[1]
        if GLO.isdesc:
            GLO.gramatica[2] = GLO.gram[58]
        else:
            GLO.gramatica[2] = GLO.gram[2]

    def p_LETS_INS(self,t) :
        'LETS    : ET '
        t[0] = [t[1]]
        GLO.gramatica[3] = GLO.gram[3]

    def p_ETQ(self,t) :
        '''ET      : ID dosp LINS'''
        t[0] = Etiqueta(t[1],None, t[3],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[4] = GLO.gram[4]


    def p_LINS_lista(self,t) :
        'LINS    : LINS INS'
        t[1].append(t[2])
        t[0] = t[1]
        if GLO.isdesc:
            GLO.gramatica[5] = GLO.gram[59]
        else:
            GLO.gramatica[5] = GLO.gram[5]


    def p_LINS_INS(self,t) :
        'LINS    : INS '
        t[0] = [t[1]]
        GLO.gramatica[6] = GLO.gram[6]

    def p_INS1(self,t) :
        'INS      : PRINT'
        t[0] = t[1]
        GLO.gramatica[7] = GLO.gram[7]

    def p_INS2(self,t) :
        'INS      : ASIGNACION'
        t[0] = t[1]
        GLO.gramatica[8] = GLO.gram[8]

    def p_INS3(self,t) :
        'INS      : SALTO'
        t[0] = t[1]
        GLO.gramatica[9] = GLO.gram[9]

    def p_INS4(self,t) :
        'INS      : SIF'
        t[0] = t[1]
        GLO.gramatica[10] = GLO.gram[10]


    def p_INS5(self,t) :
        'INS      : EXIT'
        t[0] = t[1]
        GLO.gramatica[11] = GLO.gram[11]
        
    def p_INS6(self,t) :
        'INS      : UNSET'
        t[0] = t[1]
        GLO.gramatica[12] = GLO.gram[12]


    def p_VAR(self,t) :
        'VAR   : dollar ID LCOR'
        t[0] =Variable(t[2],t[3],t.slice[1].lineno,self.find_column(self.input,t.slice[1]))
        print ("descendente?: "+ str(GLO.isdesc))
        if GLO.isdesc:
            GLO.gramatica[13] = GLO.gram[60]
            GLO.gramatica[13.5] = GLO.gram[61]
        else:
            GLO.gramatica[13] = GLO.gram[13]


    def p_VARID(self,t) :
        'VAR   : dollar ID '
        t[0] =Variable(t[2],None,t.slice[1].lineno,self.find_column(self.input,t.slice[1]))
        print ("descendente?: "+ str(GLO.isdesc))
        if GLO.isdesc:
            GLO.gramatica[14] = GLO.gram[60]
            GLO.gramatica[14.5] = GLO.gram[62]
        else:
            GLO.gramatica[14] = GLO.gram[14]

    def p_LCOR(self,t) :
        'LCOR   : LCOR corcha EXP corchc'
        t[1].append(t[3])
        t[0] = t[1]
        GLO.gramatica[15] = GLO.gram[15]

    def p_LCORC(self,t) :
        'LCOR   : corcha EXP corchc'
        t[0] = [t[2]]
        GLO.gramatica[16] = GLO.gram[16]

    def p_INS_PRINT(self,t) :
        'PRINT     : wprint parea EXP parec ptocoma'
        t[0] =Print(t[3],t.slice[1].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[17] = GLO.gram[17]


    def p_ASIGNACION(self,t) :
        'ASIGNACION   : VAR igual EXP ptocoma'
        t[0] =Asignacion(t[1], t[3],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[18] = GLO.gram[18]


    def p_ASIGNACION_REF(self,t) :
        'ASIGNACION   : VAR igual band dollar ID ptocoma'
        t[0] =RefAsignacion(t[1], t[5],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[19] = GLO.gram[19]


    def p_SALTO(self,t) :
        'SALTO   : wgoto ID ptocoma'
        t[0] =GoTo(t[2],t.slice[1].lineno,self.find_column(self.input,t.slice[1]))
        GLO.gramatica[20] = GLO.gram[20]

    def p_EXIT(self,t) :
        'EXIT   : wexit ptocoma'
        t[0] =Exit()
        GLO.gramatica[21] = GLO.gram[21]


    def p_UNSET(self,t) :
        'UNSET   : wunset parea EXP parec ptocoma'
        t[0] =Unset(t[3],t.slice[1].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[22] = GLO.gram[22]





    def p_SIF(self,t) :
        'SIF           : wif parea EXP parec SALTO'
        t[0] =If(t[3], t[5],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
        GLO.gramatica[23] = GLO.gram[23]



    def p_expresion_binaria(self,t):
        '''EXP : EXP mas EXP
                | EXP menos EXP
                | EXP por EXP
                | EXP dividido EXP
                | EXP modulo EXP'''
        if t[2] == '+'  : 
            t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MAS)
            GLO.gramatica[24] = GLO.gram[24]
        elif t[2] == '-': 
            t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MENOS)
            GLO.gramatica[25] = GLO.gram[25]
        elif t[2] == '*': 
            t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.POR)
            GLO.gramatica[26] = GLO.gram[26]
        elif t[2] == '/': 
            t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
            GLO.gramatica[27] = GLO.gram[27]
        elif t[2] == '%': 
            t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MODULO)
            GLO.gramatica[28] = GLO.gram[28]



    def p_EXP_REL(self,t) :
        '''EXP : EXP mayor EXP
                | EXP menor EXP
                | EXP mayorigual EXP
                | EXP menorigual EXP
                | EXP igualdad EXP
                | EXP diferente EXP
                '''
        if t[2] == '>'    : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MAYOR,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[29] = GLO.gram[29]
        elif t[2] == '<'  : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MENOR,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[30] = GLO.gram[30]
        elif t[2] == '>=' : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MAYORIGUAL,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[31] = GLO.gram[31]
        elif t[2] == '<=' : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MENORIGUAL,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[32] = GLO.gram[32]
        elif t[2] == '==' : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.IGUAL,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[33] = GLO.gram[33]
        elif t[2] == '!=' : 
            t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.DIFERENTE,t.slice[2].lineno,self.find_column(self.input,t.slice[2]))
            GLO.gramatica[34] = GLO.gram[34]

    def p_EXP_LOG(self,t) :
        '''EXP : EXP land EXP
                | EXP lor EXP
                | EXP wxor EXP
                '''
        if t[2] == '&&'    : 
            t[0] = Logica(t[1], t[3], OPERACION_LOGICA.AND)
            GLO.gramatica[35] = GLO.gram[35]
        elif t[2] == '||'  : 
            t[0] = Logica(t[1], t[3], OPERACION_LOGICA.OR)
            GLO.gramatica[36] = GLO.gram[36]
        elif t[2] == 'xor' : 
            t[0] = Logica(t[1], t[3], OPERACION_LOGICA.XOR)
            GLO.gramatica[37] = GLO.gram[37]

    def p_expresion_not(self,t):
        'EXP : lnot EXP'
        t[0] = Logica(t[2],None,OPERACION_LOGICA.NOT)
        GLO.gramatica[38] = GLO.gram[38]

    def p_EXP_BIT(self,t) :
        '''EXP : EXP band EXP
                | EXP bor EXP
                | EXP bxor EXP
                | EXP bshiftl EXP
                | EXP bshiftr EXP
                '''
        if t[2] == '&'    : 
            t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITAND)
            GLO.gramatica[39] = GLO.gram[39]
        elif t[2] == '|'  : 
            t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITOR)
            GLO.gramatica[40] = GLO.gram[40]
        elif t[2] == '^' : 
            t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITXOR)
            GLO.gramatica[41] = GLO.gram[41]
        elif t[2] == '<<' : 
            t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.SHIFTL)
            GLO.gramatica[42] = GLO.gram[42]
        elif t[2] == '>>' : 
            t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.SHIFTR)
            GLO.gramatica[43] = GLO.gram[43]

    def p_expresion_bitnot(self,t):
        'EXP : bnot EXP'
        t[0] = Bitwise(t[2],None,OPERACION_BITWISE.BITNOT)
        GLO.gramatica[44] = GLO.gram[44]

    def p_expresion_unaria(self,t):
        'EXP : menos EXP %prec Umenos'
        t[0] = ExpresionNegativo(t[2])
        GLO.gramatica[45] = GLO.gram[45]

    def p_expresion_agrupacion(self,t):
        'EXP : parea EXP parec'
        t[0] = t[2]
        GLO.gramatica[46] = GLO.gram[46]

    def p_expresion_absoluto(self,t):
        'EXP : wabs parea EXP parec'
        t[0] = ExpresionAbsoluto(t[3])
        GLO.gramatica[47] = GLO.gram[47]

    def p_expresion_entero(self,t):
        '''EXP : ENTERO'''
        t[0] = ExpresionInteger(t[1])
        GLO.gramatica[48] = GLO.gram[48]

    def p_expresion_float(self,t):
        '''EXP : DECIMAL'''
        t[0] = ExpresionFloat(t[1])
        GLO.gramatica[49] = GLO.gram[49]

    def p_expresion_id(self,t):
        'EXP   : VAR'
        t[0] = t[1]
        GLO.gramatica[50] = GLO.gram[50]
    def p_EXP_STR(self,t) :
        'EXP     : CADENA'
        t[0] = ExpresionDobleComilla(t[1])
        GLO.gramatica[51] = GLO.gram[51]

    def p_EXP_CHAR(self,t) :
        'EXP     : CHAR'
        t[0] = ExpresionDobleComilla(t[1])
        GLO.gramatica[52] = GLO.gram[52]

    def p_CONVERTIR(self,t) :
        '''EXP    :  parea wint parec EXP 
                    | parea wfloat parec EXP 
                    | parea wchar parec EXP 
                        '''
        if t[2] == 'int'  : 
            t[0] = ExpConvertida(t[4], TIPO_DATO.INTEGER,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))
            GLO.gramatica[53] = GLO.gram[53]
        elif t[2] == 'float': 
            t[0] = ExpConvertida(t[4], TIPO_DATO.FLOAT,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))
            GLO.gramatica[54] = GLO.gram[54]
        elif t[2] == 'char': 
            t[0] = ExpConvertida(t[4], TIPO_DATO.CHAR,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))
            GLO.gramatica[55] = GLO.gram[55]



    def p_EXP_ARR(self,t) :
        'EXP     : warray parea parec '
        t[0] = Arreglo()
        GLO.gramatica[56] = GLO.gram[56]

    def p_EXP_READ(self,t) :
        'EXP     : wread parea parec '
        t[0] = Read(t.slice[2].lineno,self.find_column(self.input,t.slice[1]))
        GLO.gramatica[57] = GLO.gram[57]

    def p_error(self,t):
        if t is not None:
            self.ms_gramatica.AddMensaje(MS.Mensaje("Se encontro: "+str(t.value),t.lineno,self.find_column(self.input,t) ,True,"Sintactico"))
            #print("Error sintáctico en '%s'" % p.value)
            while 1:
                tok = yacc.token()             # Get the next token
                if not tok or tok.type == 'ptocoma': 
                    break
            yacc.errok()
            return tok

        else:
            self.ms_gramatica.AddMensaje(MS.Mensaje("No se pudo recuperar: ",0,0 ,True,"Sintactico"))
       

    def parse(self,input) :
        self.input = input
        tokens = self.build()
        self.parser = yacc.yacc(module = self)
        return  self.parser.parse(input)

