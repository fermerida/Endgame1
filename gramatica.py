
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

    def p_LETS_lista(self,t) :
        'LETS    : LETS ET'
        t[1].append(t[2])
        t[0] = t[1]


    def p_LETS_INS(self,t) :
        'LETS    : ET '
        t[0] = [t[1]]

    def p_ETQ(self,t) :
        '''ET      : ID dosp LINS'''
        t[0] = Etiqueta(t[1],None, t[3],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))


    def p_LINS_lista(self,t) :
        'LINS    : LINS INS'
        t[1].append(t[2])
        t[0] = t[1]


    def p_LINS_INS(self,t) :
        'LINS    : INS '
        t[0] = [t[1]]

    def p_INS(self,t) :
        '''INS      : PRINT
                    | ASIGNACION
                    | SALTO
                    | SIF
                    | EXIT
                    | UNSET'''
        t[0] = t[1]

    def p_VAR(self,t) :
        'VAR   : dollar ID LCOR'
        t[0] =Variable(t[2],t[3])

    def p_VARID(self,t) :
        'VAR   : dollar ID '
        t[0] =Variable(t[2],None)

    def p_LCOR(self,t) :
        'LCOR   : LCOR corcha EXP corchc'
        t[1].append(t[3])
        t[0] = t[1]

    def p_LCORC(self,t) :
        'LCOR   : corcha EXP corchc'
        t[0] = [t[2]]

    def p_INS_PRINT(self,t) :
        'PRINT     : wprint parea EXP parec ptocoma'
        t[0] =Print(t[3],t.slice[1].lineno,self.find_column(self.input,t.slice[2]))
    def p_ASIGNACION(self,t) :
        'ASIGNACION   : VAR igual EXP ptocoma'
        t[0] =Asignacion(t[1], t[3],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))

    def p_ASIGNACION_REF(self,t) :
        'ASIGNACION   : VAR igual band dollar ID ptocoma'
        t[0] =RefAsignacion(t[1], t[5],t.slice[2].lineno,self.find_column(self.input,t.slice[2]))


    def p_SALTO(self,t) :
        'SALTO   : wgoto ID ptocoma'
        t[0] =GoTo(t[2],t.slice[1].lineno,self.find_column(self.input,t.slice[1]))

    def p_EXIT(self,t) :
        'EXIT   : wexit ptocoma'
        t[0] =Exit()


    def p_UNSET(self,t) :
        'UNSET   : wunset parea EXP parec ptocoma'
        t[0] =Unset(t[3],t.slice[1].lineno,self.find_column(self.input,t.slice[2]))





    def p_SIF(self,t) :
        'SIF           : wif parea EXP parec SALTO'
        t[0] =If(t[3], t[5])



    def p_expresion_binaria(self,t):
        '''EXP : EXP mas EXP
                | EXP menos EXP
                | EXP por EXP
                | EXP dividido EXP
                | EXP modulo EXP'''
        if t[2] == '+'  : t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MAS)
        elif t[2] == '-': t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MENOS)
        elif t[2] == '*': t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.POR)
        elif t[2] == '/': t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
        elif t[2] == '%': t[0] = Aritmetica(t[1], t[3], OPERACION_ARITMETICA.MODULO)

    def p_EXP_REL(self,t) :
        '''EXP : EXP mayor EXP
                | EXP menor EXP
                | EXP mayorigual EXP
                | EXP menorigual EXP
                | EXP igualdad EXP
                | EXP diferente EXP
                '''
        if t[2] == '>'    : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MAYOR)
        elif t[2] == '<'  : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MENOR)
        elif t[2] == '>=' : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MAYORIGUAL)
        elif t[2] == '<=' : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.MENORIGUAL)
        elif t[2] == '==' : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.IGUAL)
        elif t[2] == '!=' : t[0] = Relacional(t[1], t[3], OPERACION_RELACIONAL.DIFERENTE)

    def p_EXP_LOG(self,t) :
        '''EXP : EXP land EXP
                | EXP lor EXP
                | EXP wxor EXP
                '''
        if t[2] == '&&'    : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.AND)
        elif t[2] == '||'  : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.OR)
        elif t[2] == 'xor' : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.XOR)

    def p_expresion_not(self,t):
        'EXP : lnot EXP'
        t[0] = Logica(t[2],None,OPERACION_LOGICA.NOT)

    def p_EXP_BIT(self,t) :
        '''EXP : EXP band EXP
                | EXP bor EXP
                | EXP bxor EXP
                | EXP bshiftl EXP
                | EXP bshiftr EXP
                '''
        if t[2] == '&'    : t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITAND)
        elif t[2] == '|'  : t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITOR)
        elif t[2] == '^' : t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.BITXOR)
        elif t[2] == '<<' : t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.SHIFTL)
        elif t[2] == '>>' : t[0] = Bitwise(t[1], t[3], OPERACION_BITWISE.SHIFTR)

    def p_expresion_bitnot(self,t):
        'EXP : bnot EXP'
        t[0] = Bitwise(t[2],None,OPERACION_BITWISE.BITNOT)

    def p_expresion_unaria(self,t):
        'EXP : menos EXP %prec Umenos'
        t[0] = ExpresionNegativo(t[2])

    def p_expresion_agrupacion(self,t):
        'EXP : parea EXP parec'
        t[0] = t[2]

    def p_expresion_absoluto(self,t):
        'EXP : wabs parea EXP parec'
        t[0] = ExpresionAbsoluto(t[3])

    def p_expresion_entero(self,t):
        '''EXP : ENTERO'''
        t[0] = ExpresionInteger(t[1])

    def p_expresion_float(self,t):
        '''EXP : DECIMAL'''
        t[0] = ExpresionFloat(t[1])

    def p_expresion_id(self,t):
        'EXP   : VAR'
        t[0] = t[1]

    def p_EXP_STR(self,t) :
        'EXP     : CADENA'
        t[0] = ExpresionDobleComilla(t[1])

    def p_EXP_CHAR(self,t) :
        'EXP     : CHAR'
        t[0] = ExpresionDobleComilla(t[1])

    def p_CONVERTIR(self,t) :
        '''EXP    :  parea wint parec EXP 
                    | parea wfloat parec EXP 
                    | parea wchar parec EXP 
                        '''
        if t[2] == 'int'  : t[0] = ExpConvertida(t[4], TIPO_DATO.INTEGER,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))
        elif t[2] == 'float': t[0] = ExpConvertida(t[4], TIPO_DATO.FLOAT,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))
        elif t[2] == 'char': t[0] = ExpConvertida(t[4], TIPO_DATO.CHAR,t.slice[2].lineno,self.find_column(self.input,t.slice[3]))



    def p_EXP_ARR(self,t) :
        'EXP     : warray parea parec '
        t[0] = Arreglo()

    def p_EXP_READ(self,t) :
        'EXP     : wread parea parec '
        t[0] = Read(t.slice[2].lineno,self.find_column(self.input,t.slice[1]))

    def p_error(self,p):
        if p is not None:
            self.ms_gramatica.AddMensaje(MS.Mensaje("Se encontro: "+str(p.value),p.lineno,self.find_column(self.input,p) ,True,"Sintactico"))
            print("Error sintáctico en '%s'" % p.value)
        elif p.value =="exit":
            self.ms_gramatica.AddMensaje(MS.Mensaje("No se pudo recuperar: ",0,0 ,True,"Sintactico"))
        else:
            self.ms_gramatica.AddMensaje(MS.Mensaje("No se pudo recuperar: ",0,0 ,True,"Sintactico"))
        while 1:
            tok = yacc.token()             # Get the next token
            if not tok or tok.type == 'ptocoma': 
                break
        yacc.restart()

    def parse(self,input) :
        self.input = input
        tokens = self.build()
        self.parser = yacc.yacc(module = self)
        return  self.parser.parse(input)

