
import ply.lex as lex
import ply.yacc as yacc
from NodoAST import *


class ASTDES:
    
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
        'if'   : 'wif',
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
        ('left','bor'),
        ('left','wxor'),
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
    def find_column(input, token):
        print("este es input: " +input)
        line_start = str(input).rfind('\n', 0, token.lEos) + 1
        print((token.lEos - line_start) + 1)
    


    def p_INI(self,t) :
        'INI            : LETS'
        temp = NodoAST("Raiz","Raiz",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        t[0] = temp

    def p_LETS_lista(self,t) :
        'LETS    :  ET LETS'
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
        'LINS    : INS LINS'
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
        temp1 = NodoAST("Variableaux","Variable Auxiliar",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[2],self.countN)
        self.countN+= 1
        temp1.addHijo(t[3])
        temp.addHijo(temp2)
        temp.addHijo(temp1)
        t[0] = temp

    def p_VARID(self,t) :
        'VAR   : dollar ID '
        temp = NodoAST("Variable","Variable",self.countN)
        self.countN+= 1
        temp1 = NodoAST("Variableaux","Variable Auxiliar",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ID",t[2],self.countN)
        self.countN+= 1
        temp3 = NodoAST("epsilon","epsilon",self.countN)
        self.countN+= 1
        temp1.addHijo(temp3)
        temp.addHijo(temp2)
        temp.addHijo(temp1)
        t[0] = temp

    def p_LCOR(self,t) :
        'LCOR   :  corcha EA corchc LCOR'
        temp = NodoAST("Corchetes","Corchetes",self.countN)
        self.countN+= 1
        temp.addHijo(t[2])
        temp.addHijo(t[4])
        t[0] = temp

    def p_LCORC(self,t) :
        'LCOR   : corcha EA corchc'
        temp = NodoAST("Corchetes","Corchetes",self.countN)
        self.countN+= 1
        temp.addHijo(t[2])
        t[0] = temp

    def p_INS_PRINT(self,t) :
        'PRINT     : wprint parea EA parec ptocoma'
        temp = NodoAST("Print","Print",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        t[0] = temp

    def p_ASIGNACION(self,t) :
        'ASIGNACION   : VAR igual EA ptocoma'
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
        'UNSET   : wunset parea EA parec ptocoma'
        temp = NodoAST("Unset","Unset",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        t[0] = temp



    def p_SIF(self,t) :
        'SIF           : wif parea EA parec SALTO'
        temp = NodoAST("SIF","Sentencia IF",self.countN)
        self.countN+= 1
        temp.addHijo(t[3])
        temp.addHijo(t[5])
        t[0] = temp





    def p_E_OR(self,t) :
        'EA : EB EAP'
        temp = NodoAST("EXP","Expresion OR",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp

    def p_E_ORB(self,t) :
        '''EAP :  lor EB EAP
                | empty'''
        temp = NodoAST("EXP","Expresion OR Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_E_AND(self,t) :
        'EB : EC EBP'
        temp = NodoAST("EXP","Expresion AND",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp

    def p_E_AND2(self,t) :
        '''EBP :  land EC EBP
                | empty'''    
        temp = NodoAST("EXP","Expresion And Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_E_BOR(self,t) :
        'EC : ED ECP'
        temp = NodoAST("EXP","Expresion Bit OR",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp

    def p_E_BOR2(self,t) :
        '''ECP :  bor ED ECP
                | empty'''  

        temp = NodoAST("EXP","Expresion Bit OR Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_E_WXOR(self,t) :
        'ED : EE EDP'
        temp = NodoAST("EXP","Expresion XOR",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp

    def p_E_WXOR2(self,t) :
        '''EDP :  wxor EE EDP
                | empty''' 

        temp = NodoAST("EXP","Expresion XOR Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_E_BXOR(self,t) :
        'EE : EF EEP'
        temp = NodoAST("EXP","Expresion Bit XOR",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_E_BXOR2(self,t) :
        '''EEP :  bxor EF EEP
                | empty'''
        temp = NodoAST("EXP","Expresion Bit XOR Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp
    
    def p_E_BAND(self,t) :
        'EF : EG  EFP'
        temp = NodoAST("EXP","Expresion Bit AND",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_E_BAND2(self,t) :
        '''EFP :  band EG EFP
                | empty'''
        temp = NodoAST("EXP","Expresion Bit AND Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_E_igual(self,t) :
        'EG : EH  EGP'
        temp = NodoAST("EXP","Expresion Igualdad",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp


    def p_E_igual2(self,t) :
        '''EGP : igualdad EH EGP
                | diferente EH EGP
                | empty
                '''
        temp = NodoAST("EXP","Expresion Igualdad Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp
        
    def p_E_REL(self,t) :
        'EH : EI  EHP'
        temp = NodoAST("EXP","Expresion Comparacion",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp

    def p_E_REL2(self,t) :
        '''EHP :  mayor EI EHP
                | menor EI EHP
                | mayorigual EI EHP
                | menorigual EI EHP
                | empty
                '''
        temp = NodoAST("EXP","Expresion Comparacion Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp


    def p_E_POR(self,t) :
        'EI : EJ  EIP'
        temp = NodoAST("EXP","Expresion Shift",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_E_POR2(self,t) :
        '''EIP : bshiftl EJ EIP
                | bshiftr EJ EIP
                | empty
                '''
        temp = NodoAST("EXP","Expresion Shift Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_Expresion_binaria(self,t):
        'EJ : EK  EJP'
        temp = NodoAST("EXP","Expresion Suma-Resta",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_Expresion_binaria2(self,t):
        '''EJP :  mas EK EJP
                | menos EK EJP
                | empty
                '''

        temp = NodoAST("EXP","Expresion  Suma-Resta Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp

    def p_Expresion_multi(self,t):
        'EK : E  EKP'
        temp = NodoAST("EXP","Expresion Multiplicacion-division-mod",self.countN)
        self.countN+= 1
        temp.addHijo(t[1])
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_Expresion_multi2(self,t):
        '''EKP : por E  EKP
                | dividido E  EKP
                | modulo E  EKP
                | empty
                '''
        temp = NodoAST("EXP","Expresion Multiplicacion-division-mod Auxiliar",self.countN)
        self.countN+= 1
        if t[1] is not None:
            temp2 = NodoAST("operador",t[1],self.countN)
            self.countN+= 1
            temp.addHijo(t[2])
            temp.addHijo(t[3])


        else:
            epsilon = NodoAST("Epsilon","Epsilon",self.countN)
            self.countN+= 1
            temp.addHijo(epsilon)
        t[0]=temp
        
    def p_Expresion_not(self,t):
        '''E : lnot E
                | bnot E
                | menos E %prec Umenos'''
        temp = NodoAST("EXP","Expresion Unaria",self.countN)
        self.countN+= 1
        temp1 = NodoAST("operador",t[1],self.countN)
        self.countN+= 1

        temp.addHijo(temp1)
        temp.addHijo(t[2])
        t[0] = temp
    
    def p_Expresion_agrupacion(self,t):
        'E : parea E parec'
        temp = NodoAST("EXP","Expresion",self.countN)
        self.countN+= 1
        temp.addHijo(t[2])
        t[0] = temp
    def p_Expresion_absoluto(self,t):
        'E : wabs parea E parec'
        temp = NodoAST("EXP","Expresion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("operador","Absoluto",self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[3])
        t[0] = temp
    def p_Expresion_entero(self,t):
        '''E : ENTERO'''
        temp = NodoAST("Entero",str(t[1]),self.countN)
        self.countN+= 1
        t[0] = temp

    def p_Expresion_float(self,t):
        '''E : DECIMAL'''
        temp = NodoAST("Decimal",t[1],self.countN)
        self.countN+= 1
        t[0] = temp

    def p_Expresion_id(self,t):
        'E   :    VAR'

        t[0] = t[1]

    def p_E_STR(self,t) :
        'E     : CADENA'
        temp = NodoAST("Cadena",t[1],self.countN)
        self.countN+= 1
        t[0] = temp
    
    def p_E_CHAR(self,t) :
        'E     : CHAR'
        temp = NodoAST("Char",t[1],self.countN)
        self.countN+= 1
        t[0] = temp

    def p_CONVERTIR(self,t) :
        '''E    :  parea wint parec E 
                    | parea wfloat parec E 
                    | parea wchar parec E 
                        '''
        temp = NodoAST("Conversion","Conversion",self.countN)
        self.countN+= 1
        temp2 = NodoAST("ctipo",t[2],self.countN)
        self.countN+= 1
        temp.addHijo(temp2)
        temp.addHijo(t[4])
        t[0] = temp




    def p_E_ARR(self,t) :
        'E     : warray parea parec '
        temp = NodoAST("Array","New Array",self.countN)
        self.countN+= 1
        t[0] = temp

    def p_E_READ(self,t) :
        'E     : wread parea parec '
        temp = NodoAST("Read","Read Data",self.countN)
        self.countN+= 1
        t[0] = temp

    def p_empty(self,p):
        'empty :'
        pass


    def p_error(self,t):
        t.value
        print("Error sintáctico en '%s'" % t.value + "linea: "+str(t.lineno))


    def parse(self,input) :
        tokens = self.build()
        self.parser = yacc.yacc(module = self)
        return  self.parser.parse(input)

