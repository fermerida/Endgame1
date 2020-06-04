
# -----------------------------------------------------------------------------
# Rainman Sián
# 26-02-2020
#
# Ejemplo interprete sencillo con Python utilizando ply en Ubuntu
# -----------------------------------------------------------------------------

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
    'if'  : 'wif'
}

tokens  = [
    'dollar',
    'ptocoma',
    'dosp',
    'parea',
    'parec',
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
    'ID'
] + list(reservadas.values())

# Tokens
t_dollar     = r'\$'
t_ptocoma    = r';'
t_dosp       = r':'
t_parea      = r'\('
t_parec      = r'\)'
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

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

def t_CADENA(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('right','igual'),
    ('left','lor'),
    ('left','land'),
    ('left','igualdad','diferente'),
    ('left','menor','mayor','menorigual','mayorigual'),
    ('left','mas','menos'),
    ('left','por','dividido'),
    ('right','Umenos'),
    ('left','parea','parec'),
    )

# Definición de la gramática

from expresiones import *
from instrucciones import *
from etiquetas import *
from arbol import *


def p_INI(t) :
    'INI            : LETS'
    t[0] = t[1]

def p_LETS_lista(t) :
    'LETS    : LETS ET'
    t[1].append(t[2])
    t[0] = t[1]


def p_LETS_INS(t) :
    'LETS    : ET '
    t[0] = [t[1]]

def p_ETQ(t) :
    '''ET      : ID dosp LINS'''
    t[0] = Etiqueta(t[1],None, t[3])


def p_LINS_lista(t) :
    'LINS    : LINS INS'
    t[1].append(t[2])
    t[0] = t[1]


def p_LINS_INS(t) :
    'LINS    : INS '
    t[0] = [t[1]]

def p_INS(t) :
    '''INS      : PRINT
                | ASIGNACION
                | SALTO
                | SIF
                | EXIT
                | UNSET
                | CONVERTIR'''
    t[0] = t[1]

def p_INS_PRINT(t) :
    'PRINT     : wprint parea EXP parec ptocoma'
    t[0] =Print(t[3])
def p_ASIGNACION(t) :
    'ASIGNACION   : dollar ID igual EXP ptocoma'
    t[0] =Asignacion(t[2], t[4], "Variable")

def p_ASIGNACION_REF(t) :
    'ASIGNACION   : dollar ID igual band dollar ID ptocoma'
    t[0] =RefAsignacion(t[2], t[6], "Variable")


def p_SALTO(t) :
    'SALTO   : wgoto ID ptocoma'
    t[0] =GoTo(t[2])

def p_EXIT(t) :
    'EXIT   : wexit ptocoma'
    t[0] =Exit()

def p_UNSET(t) :
    'UNSET   : wunset parea EXP parec ptocoma'
    t[0] =Unset(t[3])


def p_CONVERTIR(t) :
    '''CONVERTIR    : dollar ID igual parea wint parec dollar ID ptocoma
                    | 
                    '''
    t[0] =GoTo(t[2])


def p_SIF(t) :
    'SIF           : wif parea EXP parec SALTO'
    t[0] =If(t[3], t[5])



def p_expresion_binaria(t):
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

def p_EXP_REL(t) :
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

def p_EXP_LOG(t) :
    '''EXP : EXP land EXP
            | EXP lor EXP
            | EXP wxor EXP
            '''
    if t[2] == '&&'    : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.AND)
    elif t[2] == '||'  : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.OR)
    elif t[2] == 'xor' : t[0] = Logica(t[1], t[3], OPERACION_LOGICA.XOR)

def p_expresion_not(t):
    'EXP : lnot EXP'
    t[0] = Logica(t[2],None,OPERACION_LOGICA.NOT)

def p_EXP_BIT(t) :
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

def p_expresion_bitnot(t):
    'EXP : bnot EXP'
    t[0] = Bitwise(t[2],None,OPERACION_BITWISE.BITNOT)

def p_expresion_unaria(t):
    'EXP : menos EXP %prec Umenos'
    t[0] = ExpresionNegativo(t[2])

def p_expresion_agrupacion(t):
    'EXP : parea EXP parec'
    t[0] = t[2]

def p_expresion_absoluto(t):
    'EXP : wabs parea EXP parec'
    t[0] = ExpresionAbsoluto(t[3])

def p_expresion_entero(t):
    '''EXP : ENTERO'''
    t[0] = ExpresionInteger(t[1])

def p_expresion_float(t):
    '''EXP : DECIMAL'''
    t[0] = ExpresionFloat(t[1])

def p_expresion_id(t):
    'EXP   : dollar ID'
    t[0] = ExpresionIdentificador(t[2])


def p_EXP_STR(t) :
    'EXP     : CADENA'
    t[0] = ExpresionDobleComilla(t[1])





def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)