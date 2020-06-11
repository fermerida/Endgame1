class NodoAST :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  nombre ,label,c) :
        self.id = nombre + str(c)
        self.label=label
        self.hijos = []
    
    def addHijo(self, hijo):
        self.hijos.append(hijo)
    
    
    def changeLabel(lab):
        self.label = lab
    
    