import mensajes as MS

ToConsole = None
window = None
TextArea= None
ms_global = MS.Mensajes()
pila =0

isdesc = False
gramatica= {}
gram={
    1:{
        'rule': "INI -> LETS",
        'action':"INI.val = LETS.val"
    },
    2:{
        'rule':'LETS -> LETS ET' ,
        'action': 'LETS1.append(ET.dir); LETS.val = LETS1.val'
    },
    3:{
        'rule':'LETS -> ET ' ,
        'action': 'LETS.val = ET.dir'
    },
    4:{
        'rule': 'ET -> ID dosp LINS',
        'action': 'ET.val = new Etiqueta(ID.val, LINS.val);'
    },
    5:{
        'rule': 'LINS -> LINS INS',
        'action': 'LINS1.append(INS.dir); LINS.val = LINS1.val;'
    },
    6:{
        'rule': 'LINS -> INS ',
        'action': 'LINS.val = INS.dir'
    },
    7:{
        'rule':'INS -> PRINT' ,
        'action': 'INS.val = PRINT.val'
    },
    8:{
        'rule': 'INS -> ASIGNACION',
        'action': 'INS.val = ASIGNACION.val'
    },
    9:{
        'rule': 'INS -> SALTO',
        'action': 'INS.val = SALTO.val'
    },
    10:{
        'rule': 'INS -> SIF',
        'action': 'INS.val = SIF.val'
    },
    11:{
        'rule': 'INS -> EXIT',
        'action': 'INS.val = EXIT.val'
    },
    12:{
        'rule': 'INS -> UNSET',
        'action': 'INS.val = UNSET.val'
    },
    13:{
        'rule': 'VAR -> dollar ID LCOR',
        'action': 'VAR.val = new Var(ID.lex,LCOR.val)'
    },
    14:{
        'rule': 'VAR -> dollar ID ',
        'action': 'VAR.val = new Var(ID.lex,Null)'
    },
    15:{
        'rule': 'LCOR -> LCOR corcha EXP corchc',
        'action': 'LCOR1.append(EXP); LCOR.val = LCOR1.val)'
    },
    16:{
        'rule': 'LCOR -> corcha EXP corchc',
        'action': 'LCOR.val = EXP.dir'
    },
    17:{
        'rule': 'PRINT -> wprint parea EXP parec ptocoma',
        'action': 'PRINT.val = new Print(EXP)'
    },
    18:{
        'rule': 'ASIGNACION -> VAR igual EXP ptocoma',
        'action': 'ASIGNACION.val = new Asignacion(VAR.val,EXP.val)'
    },
    19:{
        'rule': 'ASIGNACION -> VAR igual band VAR ptocoma',
        'action': 'ASIGNACION.val = new RefAsingacion(VAR.val, VAR1.val)'
    },
    20:{
        'rule': 'SALTO -> wgoto ID ptocoma',
        'action': 'SALTO.val = new Salto(ID.lex'
    },
    21:{
        'rule': 'EXIT -> wexit ptocoma',
        'action': 'EXIT.val= new Exit()'
    },
    22:{
        'rule': 'UNSET -> wunset parea EXP parec ptocoma',
        'action': 'UNSET.val = new Unset(EXP.val);'
    },
    23:{
        'rule': 'SIF -> wif parea EXP parec SALTO',
        'action': 'SIF.val = new If(EXP.val, SALTO.val)'
    },
    24:{
        'rule': 'EXP -> EXP mas EXP',
        'action': 'EXP.val = EXP1.val + EXP2.val'
    },
    25:{
        'rule': 'EXP -> EXP menos EXP',
        'action': 'EXP.val = EXP1.val - EXP2.val'
    },
    26:{
        'rule': 'EXP -> EXP por EXP',
        'action': 'EXP.val = EXP1.val * EXP2.val'
    },
    27:{
        'rule': 'EXP -> EXP dividido EXP',
        'action': 'EXP.val = EXP1.val / EXP2.val'
    },
    28:{
        'rule': 'EXP -> EXP modulo EXP',
        'action': 'EXP.val = EXP1.val % EXP2.val'
    },
    29:{
        'rule': 'EXP -> EXP mayor EXP',
        'action': 'EXP.val = EXP1.val > EXP2.val'
    },
    30:{
        'rule': 'EXP -> EXP menor EXP',
        'action': 'EXP.val = EXP1.val < EXP2.val'
    },
    31:{
        'rule': 'EXP -> EXP mayorigual EXP',
        'action': 'EXP.val = EXP1.val >= EXP2.val'
    },
    32:{
        'rule': 'EXP -> EXP menorigual EXP',
        'action': 'EXP.val = EXP1.val <= EXP2.val'
    },
    33:{
        'rule': 'EXP -> EXP igualdad EXP',
        'action': 'EXP.val = EXP1.val == EXP2.val'
    },
    34:{
        'rule': 'EXP -> EXP diferente EXP',
        'action': 'EXP.val = EXP1.val != EXP2.val'
    },
    35:{
        'rule': 'EXP -> EXP land EXP',
        'action': 'EXP.val = EXP1.val && EXP2.val'
    },
    36:{
        'rule': 'EXP -> EXP lor EXP',
        'action': 'EXP.val = EXP1.val || EXP2.val'
    },
    37:{
        'rule': 'EXP -> EXP wxor EXP',
        'action': 'EXP.val = EXP1.val ^^ EXP2.val'
    },
    38:{
        'rule': 'EXP -> lnot EXP',
        'action': 'EXP.val = !EXP1.val'
    },
    39:{
        'rule': 'EXP -> EXP band EXP',
        'action': 'EXP.val = EXP1.val & EXP2.val'
    },
    40:{
        'rule': 'EXP -> EXP bor EXP',
        'action': 'EXP.val = EXP1.val | EXP2.val'
    },
    41:{
        'rule': 'EXP -> EXP bxor EXP',
        'action': 'EXP.val = EXP1.val ^ EXP2.val'
    },
    42:{
        'rule': 'EXP -> EXP bshiftl EXP',
        'action': 'EXP.val = EXP1.val << EXP2.val'
    },
    43:{
        'rule': 'EXP -> EXP bshiftr EXP',
        'action': 'EXP.val = EXP1.val >> EXP2.val'
    },
    44:{
        'rule': 'EXP -> bnot EXP',
        'action': 'EXP.val = ~EXP1.val'
    },
    45:{
        'rule': 'EXP -> menos EXP',
        'action': 'EXP.val = -EXP1.val'
    },
    46:{
        'rule': 'EXP -> parea EXP parec',
        'action': 'EXP.val = (EXP1.val)'
    },
    47:{
        'rule': 'EXP -> wabs parea EXP parec',
        'action': 'EXP.val= new Absolute(EXP.val)'
    },
    48:{
        'rule': 'EXP -> ENTERO',
        'action': 'EXP.val = ENTERO.lexval'
    },
    49:{
        'rule': 'EXP -> DECIMAL',
        'action': 'EXP.val = DECIMAL.lexval'
    },
    50:{
        'rule': 'EXP -> VAR',
        'action': 'EXP.val = VAR.val'
    },
    51:{
        'rule': 'EXP -> CADENA',
        'action': 'EXP.val = CADENA.lexval'
    },
    52:{
        'rule': 'EXP -> CHAR',
        'action': 'EXP.val = CHAR.lexval'
    },
    53:{
        'rule': 'EXP -> parea wint parec EXP ',
        'action': 'EXP.val = new Conversion(\'int\',EXP.val)'
    },
    54:{
        'rule': 'EXP -> parea wfloat parec EXP ',
        'action': 'EXP.val = new Conversion(\'float\',EXP.val)'
    },
    55:{
        'rule': 'EXP -> parea wchar parec EXP ',
        'action': 'EXP.val= new Conversion(\'char\',EXP.val)'
    },
    56:{
        'rule': 'EXP -> warray parea parec',
        'action': 'EXP.val = new Arreglo();'
    },
    57:{
        'rule': 'EXP -> wread parea parec',
        'action': 'EXP.val = new Read();'
    },



    58:{
        'rule': 'LETS -> ET LETS',
        'action': 'EXP.val = new Read();'
    },
    59:{
        'rule': 'LINS  -> INS LINS',
        'action': 'EXP.val = new Read();'
    },
    60:{
        'rule': 'VAR -> dollar ID VARP',
        'action': 'VAR.val = new Variable(ID.lex, VARP.val);'
    },
    61:{
        'rule': 'VARP -> LCOR',
        'action': 'EXP.val = new Read();'
    },
    62:{
        'rule': 'VARP -> epsilon',
        'action': 'EXP.val = new Read();'
    },
    63:{
        'rule': 'EA  -> EB EAP',
        'action': 'EA.val = EB.val + EAP.val;'
    },
    64:{
        'rule': 'EAP  -> empty',
        'action': 'EAP.val  = 0;'
    },
    65:{
        'rule': 'EB  -> EC EBP',
        'action': 'EB.val = EC.val + EBP.val;'
    },
    66:{
        'rule': 'EBP  -> empty',
        'action': 'EBP.val  = 0;'
    },
    67:{
        'rule': 'EC  -> ED ECP',
        'action': 'EB.val = ED.val + EBP.val;'
    },
    68:{
        'rule': 'ECP  -> empty',
        'action': 'ECP.val  = 0;'
    },
    69:{
        'rule': 'ED  -> EE EDP',
        'action': 'ED.val = EE.val + EDP.val;'
    },
    70:{
        'rule': 'EDP  -> empty',
        'action': 'EDP.val  = 0;'
    },
    71:{
        'rule': 'EE  -> EF EEP',
        'action': 'EE.val = EF.val + EEP.val;'
    },
    72:{
        'rule': 'EEP  -> empty',
        'action': 'EEP.val  = 0;'
    },
    73:{
        'rule': 'EF  -> EG EFP',
        'action': 'EF.val = EG.val + EFP.val;'
    },
    74:{
        'rule': 'EFP  -> empty',
        'action': 'EFP.val  = 0;'
    },
    75:{
        'rule': 'EG  -> EH EGP',
        'action': 'EG.val = EH.val + EGP.val;'
    },
    76:{
        'rule': 'EGP  -> empty',
        'action': 'EGP.val  = 0;'
    },
    77:{
        'rule': 'EH  -> EJ EHP',
        'action': 'EH.val = EJ.val + EHP.val;'
    },
    78:{
        'rule': 'EHP  -> empty',
        'action': 'EHP.val  = 0;'
    },
    79:{
        'rule': 'EJ -> EK EDJ',
        'action': 'EJ.val = EK.val + EJP.val;'
    },
    80:{
        'rule': 'EJP  -> empty',
        'action': 'EJP.val  = 0;'
    },
    81:{
        'rule': 'EK  -> E EKP',
        'action': 'EE.val = EF.val + EEP.val;'
    },
    82:{
        'rule': 'EKP  -> empty',
        'action': 'EKP.val  = 0;'
    }





}

debugging = False
pila_action = None
action_puntero = 0
current_etiqueta = None
TSG= None