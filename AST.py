
import ply.lex as lex
import ply.yacc as yacc
from NodoAST import *


class AST:
    
    def __init__(self) :
        self.countN = 0

   
        
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
        print("Illegal character '%s'" % t.value[0])
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
        ('left','igualdad','diferente'),
        ('left','menor','mayor','menorigual','mayorigual'),
        ('left','mas','menos'),
        ('left','por','dividido'),
        ('right','Umenos'),
        ('left','parea','parec'),
        )

    # Definición de la gramática
    def find_column(input, token):
        print("este es input: " +input)
        line_start = str(input).rfind('\n', 0, token.lexpos) + 1
        print((token.lexpos - line_start) + 1)
    


    def p_INI(self,t) :
        'INI            : LETS'
        temp = NodoAST("Raiz","Raiz",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        t[0] = temp

    def p_LETS_lista(self,t) :
        'LETS    : LETS ET'
        temp = NodoAST("ListaEtiquetas","ListaEtiquetas",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp


    def p_LETS_INS(self,t) :
        'LETS    : ET '
        temp = NodoAST("ListaEtiquetas","ListaEtiquetas",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        t[0] = temp


    def p_ETQ(self,t) :
        '''ET      : ID dosp LINS'''
        temp = NodoAST("Etiqueta","Etiqueta",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[1],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp



    def p_LINS_lista(self,t) :
        'LINS    : LINS INS'
        temp = NodoAST("ListInstrucciones","ListInstrucciones",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp


    def p_LINS_INS(self,t) :
        'LINS    : INS '
        temp = NodoAST("ListInstrucciones","ListInstrucciones",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        t[0] = temp

    def p_INS(self,t) :
        '''INS      : PRINT
                    | ASIGNACION
                    | SALTO
                    | SIF
                    | EXIT
                    | UNSET'''
        temp = NodoAST("Instruccion","Instruccion",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        t[0] = temp

    def p_VAR(self,t) :
        'VAR   : dollar ID LCOR'
        temp = NodoAST("Variable","Variable",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp

    def p_VARID(self,t) :
        'VAR   : dollar ID '
        temp = NodoAST("Variable","Variable",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        t[0] = temp

    def p_LCOR(self,t) :
        'LCOR   : LCOR corcha EXP corchc'
        temp = NodoAST("Corchetes","Corchetes",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[3])
        t[0] = temp

    def p_LCORC(self,t) :
        'LCOR   : corcha EXP corchc'
        temp = NodoAST("Corchetes","Corchetes",self.countN)
        self.countN+= 1
        temp.addHijo(t[2])
        t[0] = temp

    def p_INS_PRINT(self,t) :
        'PRINT     : wprint parea EXP parec ptocoma'
        temp = NodoAST("Print","Print",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        t[0] = temp

    def p_ASIGNACION(self,t) :
        'ASIGNACION   : VAR igual EXP ptocoma'
        temp = NodoAST("Asignacion","Asignacion",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[3])
        t[0] = temp

    def p_ASIGNACION_REF(self,t) :
        'ASIGNACION   : VAR igual band VAR ptocoma'
        temp = NodoAST("Asignacion","Asignacion Referenciada",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[4])
        t[0] = temp

    def p_SALTO(self,t) :
        'SALTO   : wgoto ID ptocoma'
        temp = NodoAST("Salto","Salto",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        t[0] = temp

    def p_EXIT(self,t) :
        'EXIT   : wexit ptocoma'
        temp = NodoAST("Exit","Exit",self.countN)
        self.countN+= 1
        t[0] = temp

    def p_UNSET(self,t) :
        'UNSET   : wunset parea EXP parec ptocoma'
        temp = NodoAST("Unset","Unset",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        t[0] = temp



    def p_SIF(self,t) :
        'SIF           : wif parea EXP parec SALTO'
        temp = NodoAST("SIF","Sentencia IF",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        temp.addHijo(t[5])
        t[0] = temp
    def p_expresion_binaria(self,t):
        '''EXP : EXP mas EXP
                | EXP menos EXP
                | EXP por EXP
                | EXP dividido EXP
                | EXP modulo EXP'''
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp

    def p_EXP_REL(self,t) :
        '''EXP : EXP mayor EXP
                | EXP menor EXP
                | EXP mayorigual EXP
                | EXP menorigual EXP
                | EXP igualdad EXP
                | EXP diferente EXP
                '''
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp
    def p_EXP_LOG(self,t) :
        '''EXP : EXP land EXP
                | EXP lor EXP
                | EXP wxor EXP
                '''
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp
    def p_expresion_not(self,t):
        'EXP : lnot EXP'
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador","Not",self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[2])
        t[0] = temp
    def p_EXP_BIT(self,t) :
        '''EXP : EXP band EXP
                | EXP bor EXP
                | EXP bxor EXP
                | EXP bshiftl EXP
                | EXP bshiftr EXP
                '''
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp
    def p_expresion_bitnot(self,t):
        'EXP : bnot EXP'
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador","Bit Not",self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[2])
        t[0] = temp
    def p_expresion_unaria(self,t):
        'EXP : menos EXP %prec Umenos'
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador","-",self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[2])
        t[0] = temp
    def p_expresion_agrupacion(self,t):
        'EXP : parea EXP parec'
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp.addHijo(t[2])
        t[0] = temp
    def p_expresion_absoluto(self,t):
        'EXP : wabs parea EXP parec'
        temp = NodoAST("Exp","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador","Absoluto",self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp
    def p_expresion_entero(self,t):
        '''EXP : ENTERO'''
        temp = NodoAST("Entero",str(t[1]),self.countN)
        self.countN+= 1
        t[0] = temp

    def p_expresion_float(self,t):
        '''EXP : DECIMAL'''
        temp = NodoAST("Decimal",t[1],self.countN)
        self.countN+= 1
        t[0] = temp

    def p_expresion_id(self,t):
        'EXP   :    VAR'

        t[0] = t[1]

    def p_EXP_STR(self,t) :
        'EXP     : CADENA'
        temp = NodoAST("Cadena",t[1],self.countN)
        self.countN+= 1
        t[0] = temp
    
    def p_EXP_CHAR(self,t) :
        'EXP     : CHAR'
        temp = NodoAST("Char",t[1],self.countN)
        self.countN+= 1
        t[0] = temp

    def p_CONVERTIR(self,t) :
        '''EXP    :  parea wint parec EXP 
                    | parea wfloat parec EXP 
                    | parea wchar parec EXP 
                        '''
        temp = NodoAST("Conversion","Conversion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ctipo",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[4])
        t[0] = temp




    def p_EXP_ARR(self,t) :
        'EXP     : warray parea parec '
        temp = NodoAST("Array","New Array",self.countN)
        self.countN+= 1
        t[0] = temp


    def p_error(self,t):
        t.value
        print("Error sintáctico en '%s'" % t.value + "linea: "+str(t.lineno))


    def parse(self,input) :
        tokens = self.build()
        self.parser = yacc.yacc(module = self)
        return  self.parser.parse(input)

