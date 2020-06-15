import mensajes as MS

readinput = None
window = None
ms_global = MS.Mensajes()
pila =0

gramatica={
    1:{
        'rule': "INI -> LETS",
        'action':"INI = LETS"
    },
    2:{
        'rule':'LETS -> LETS ET' ,
        'action': 'LETS1.append(ET); LETS = LETS1'
    },
    3:{
        'rule':'LETS -> ET ' ,
        'action': 'LETS = ET.dir'
    },
    4:{
        'rule': 'ET -> ID dosp LINS',
        'action': 'ET = new Etiqueta(ID.val, LINS);'
    },
    5:{
        'rule': 'LINS -> LINS INS',
        'action': 'LINS1.append(INS); LINS = LINS1;'
    },
    6:{
        'rule': 'LINS -> INS ',
        'action': 'LINS = INS.dir'
    },
    7:{
        'rule':'INS -> PRINT' ,
        'action': 'INS = PRINT'
    },
    8:{
        'rule': 'INS -> ASIGNACION',
        'action': 'INS = ASIGNACION'
    },
    9:{
        'rule': 'INS -> SALTO',
        'action': 'INS = SALTO'
    },
    10:{
        'rule': 'INS -> SIF',
        'action': 'INS = SIF'
    },
    11:{
        'rule': 'INS -> EXIT',
        'action': 'INS = EXIT'
    },
    12:{
        'rule': 'INS -> UNSET',
        'action': 'INS = UNSET'
    },
    13:{
        'rule': 'VAR -> dollar ID LCOR',
        'action': 'VAR = new Var(ID.lex,LCOR)'
    },
    14:{
        'rule': 'VAR -> dollar ID ',
        'action': 'VAR = new Var(ID.lex,Null)'
    },
    15:{
        'rule': 'LCOR -> LCOR corcha EXP corchc',
        'action': 'LCOR1.append(EXP); LCOR = LCOR1)'
    },
    16:{
        'rule': 'LCOR -> corcha EXP corchc',
        'action': 'LCOR = EXP.dir'
    },
    17:{
        'rule': 'PRINT -> wprint parea EXP parec ptocoma',
        'action': 'PRINT = new Print(EXP)'
    },
    18:{
        'rule': 'ASIGNACION -> VAR igual EXP ptocoma',
        'action': 'ASIGNACION = new Asignacion(VAR,EXP)'
    },
    19:{
        'rule': 'ASIGNACION -> VAR igual band VAR ptocoma',
        'action': 'ASIGNACION = new RefAsingacion(VAR, VAR1)'
    },
    20:{
        'rule': 'SALTO -> wgoto ID ptocoma',
        'action': 'SALTO = new Salto(ID)'
    },
    21:{
        'rule': 'EXIT -> wexit ptocoma',
        'action': 'EXIT= new Exit()'
    },
    22:{
        'rule': 'UNSET -> wunset parea EXP parec ptocoma',
        'action': 'UNSET = new Unset(Exp);'
    },
    23:{
        'rule': 'SIF -> wif parea EXP parec SALTO',
        'action': 'SIF = new If(EXP, SALTO)'
    },
    24:{
        'rule': 'EXP -> EXP mas EXP',
        'action': 'EXP = EXP1 + EXP2'
    },
    25:{
        'rule': 'EXP -> EXP menos EXP',
        'action': 'EXP = EXP1 - EXP2'
    },
    26:{
        'rule': 'EXP -> EXP por EXP',
        'action': 'EXP = EXP1 * EXP2'
    },
    27:{
        'rule': 'EXP -> EXP dividido EXP',
        'action': 'EXP = EXP1 / EXP2'
    },
    28:{
        'rule': 'EXP -> EXP modulo EXP',
        'action': 'EXP = EXP1 % EXP2'
    },
    29:{
        'rule': 'EXP -> EXP mayor EXP',
        'action': 'EXP = EXP1 > EXP2'
    },
    30:{
        'rule': 'EXP -> EXP menor EXP',
        'action': 'EXP = EXP1 < EXP2'
    },
    31:{
        'rule': 'EXP -> EXP mayorigual EXP',
        'action': 'EXP = EXP1 >= EXP2'
    },
    32:{
        'rule': 'EXP -> EXP menorigual EXP',
        'action': 'EXP = EXP1 <= EXP2'
    },
    33:{
        'rule': 'EXP -> EXP igualdad EXP',
        'action': 'EXP = EXP1 == EXP2'
    },
    34:{
        'rule': 'EXP -> EXP diferente EXP',
        'action': 'EXP = EXP1 != EXP2'
    },
    35:{
        'rule': 'EXP -> EXP land EXP',
        'action': 'EXP = EXP1 && EXP2'
    },
    36:{
        'rule': 'EXP -> EXP lor EXP',
        'action': 'EXP = EXP1 || EXP2'
    },
    37:{
        'rule': 'EXP -> EXP wxor EXP',
        'action': 'EXP = EXP1 ^^ EXP2'
    },
    38:{
        'rule': 'EXP -> lnot EXP',
        'action': 'EXP = !EXP1'
    },
    39:{
        'rule': 'EXP -> EXP band EXP',
        'action': 'EXP = EXP1 & EXP2'
    },
    40:{
        'rule': 'EXP -> EXP bor EXP',
        'action': 'EXP = EXP1 | EXP2'
    },
    41:{
        'rule': 'EXP -> EXP bxor EXP',
        'action': 'EXP = EXP1 ^ EXP2'
    },
    42:{
        'rule': 'EXP -> EXP bshiftl EXP',
        'action': 'EXP = EXP1 << EXP2'
    },
    43:{
        'rule': 'EXP -> EXP bshiftr EXP',
        'action': 'EXP = EXP1 >> EXP2'
    },
    44:{
        'rule': 'EXP -> bnot EXP',
        'action': 'EXP = ~EXP1'
    },
    45:{
        'rule': 'EXP -> menos EXP',
        'action': 'EXP = -EXP1'
    },
    46:{
        'rule': 'EXP -> parea EXP parec',
        'action': 'EXP = (EXP1)'
    },
    47:{
        'rule': 'EXP -> wabs parea EXP parec',
        'action': 'EXP = new Absolute(EXP)'
    },
    48:{
        'rule': 'EXP -> ENTERO',
        'action': 'EXP = ENTERO.lexval'
    },
    49:{
        'rule': 'EXP -> DECIMAL',
        'action': 'EXP = DECIMAL.lexval'
    },
    50:{
        'rule': 'EXP -> VAR',
        'action': 'EXP = VAR'
    },
    51:{
        'rule': 'EXP -> CADENA',
        'action': 'EXP = CADENA.lexval'
    },
    52:{
        'rule': 'EXP -> CHAR',
        'action': 'EXP = CHAR.lexval'
    },
    53:{
        'rule': 'EXP -> parea wint parec EXP ',
        'action': 'EXP = new Conversion(\'int\',EXP)'
    },
    54:{
        'rule': 'EXP -> parea wfloat parec EXP ',
        'action': 'EXP = new Conversion(\'float\',EXP)'
    },
    55:{
        'rule': 'EXP -> parea wchar parec EXP ',
        'action': 'EXP = new Conversion(\'char\',EXP)'
    },
    56:{
        'rule': 'EXP -> warray parea parec',
        'action': 'EXP = new Arreglo();'
    },
    56:{
        'rule': 'EXP -> wread parea parec',
        'action': 'EXP = new Read();'
    }
}

debugging = False
pila_action = None
action_puntero = 0
current_etiqueta = None
TSG= None