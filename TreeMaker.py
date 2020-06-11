import os
class TreeMaker :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self, raiz) :
        self.raiz = raiz
        self.file = ""
        self.PrintStr = ""
        self.ToFile = ""
        self.body = ""
        self.bodyaux = ""
    
    def BodyBuilder(self, raiz):
        if raiz!=None:
            self.body += raiz.id+" [label=\""+raiz.label + "\"];\n"
            for hijo in raiz.hijos: 
                self.BodyBuilder(hijo)
                self.bodyaux+=raiz.id+"->"+hijo.id+";\n"
        
        
    
    
    def crearArbol(self):
        self.BodyBuilder(self.raiz)
        cuerpo="digraph arbolAST{\n"+self.body+self.bodyaux+"}\n"
        #print(cuerpo)

        try:
            file= open('Arbol.dot','w+')
            file.write(cuerpo)
            file.close()
        except: 
            print("An exception ocurred")

        cmd ='"C:\\Program Files (x86)\\Graphviz2.38\\bin\\dot.exe"' + " -Tpng Arbol.dot -o Arbol.png"
        try:
            os.system(cmd)
        except: 
            print("An exception ocurred")
    