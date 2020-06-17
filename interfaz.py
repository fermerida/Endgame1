import tkinter as tk
import os     
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import ttk
import gramatica as GR
import ts as TS
from GoTo import *
from Asignacion import *
from Print import *
import mensajes as MS
import globalvar as GLO
from instrucciones import *
from etiquetas import *
from arreglo import *
from pygments import highlight
from pygments import lex
from pygments.lexers import PhpLexer
from pygments.lexers import PythonLexer
from pygments.token import Token
import AST as AR
import ASTDES as ARDES
from TreeMaker import *
from scrollimage import ScrollableImage   
import sys
sys.setrecursionlimit(2000)

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result        

class Notepad: 
    ts_global = None
    ms_global = None
    def procesar_instrucciones(self,instrucciones, ts,ms) :
    ## lista de instrucciones recolectadas
        for i in range(len(instrucciones)) :
            if i < len(instrucciones)-1:
                instrucciones[i].inicializar(ts,ms,instrucciones[i+1])
            else:
                instrucciones[i].inicializar(ts,ms,None)
        encontrado = False
        for instr in instrucciones :
            if (instr.id=="main"):
                instr.ejecutar(ts,ms)
                encontrado = True
                break
        if encontrado == False:
            ms.AddMensaje(MS.Mensaje("Es necesario contener una instrucion main al inicio",0,0,True,"Semantico"))
        for instr in instrucciones:
            instr.actualizar(ts)

    def debug_instrucciones(self,instrucciones, ts,ms) :
    ## lista de instrucciones recolectadas
        for i in range(len(instrucciones)) :
            if i < len(instrucciones)-1:
                instrucciones[i].inicializar(ts,ms,instrucciones[i+1])
            else:
                instrucciones[i].inicializar(ts,ms,None)
        encontrado = False
        for instr in instrucciones :
            if (instr.id=="main"):
                #instr.debug(ts,ms)
                GLO.pila_action = instr.instrucciones
                GLO.current_etiqueta = instr
                encontrado = True
                break
        if encontrado == False:
            ms.AddMensaje(MS.Mensaje("Es necesario contener una instrucion main al inicio",0,0,True,"Semantico"))
        for instr in instrucciones:
            instr.actualizar(ts)

    def setText(self,text):
        GLO.ToConsole.delete(1.0,"end")
        GLO.ToConsole.insert(1.0, text)

    def enterPressed(self,event=None):
        text = GLO.ToConsole.get("1.0",'end-1c')
        lines = text.split("\n")
        last_line = lines[-1]
        GLO.readinput = last_line
        showinfo("Notepad",GLO.readinput)
    
    def GetRead(self):
        return self.readinput


    def showTS(self):
        def close_window(): 
            newWindow.destroy()
        newWindow = Tk()
        widht = 1400
        height =750
        # For top and bottom 
        newWindow.geometry('%dx%d' % (widht, 
                                              height))
        label = tk.Label(newWindow, text="Tabla de simbolos", font=("Arial",30)).grid(row=0, columnspan=3)
        cols = ('Identificador', 'Rol', 'Tipo','Dimensiones','Value','Declarada en', 'Referencias')
        f1 = tk.Frame(newWindow)
        f1.grid(column=0, row=1,columnspan=2, sticky="ns")
        newWindow.rowconfigure(1, weight=1)
        listBox = ttk.Treeview(f1, columns=cols, show='headings')
        for col in cols:
            listBox.heading(col, text=col)  
            listBox.column(col, width=200,anchor="center") 
        listBox.pack(expand=True, fill='y')
        
        for i in self.ts_global.simbolos:
            if self.ts_global.simbolos[i].tipo == TS.TIPO_DATO.INTEGER:
                tipo = "Entero"
            elif  self.ts_global.simbolos[i].tipo == TS.TIPO_DATO.CHAR:
                tipo = "Caracter"
            elif  self.ts_global.simbolos[i].tipo == TS.TIPO_DATO.ARRAY:
                tipo = "Arreglo"            
            elif  self.ts_global.simbolos[i].tipo == TS.TIPO_DATO.STRUCT:
                tipo = "Struct"
            elif  self.ts_global.simbolos[i].tipo == TS.TIPO_DATO.FLOAT:
                tipo = "Flotante"
            else:
                tipo = self.ts_global.simbolos[i].tipo
            if isinstance(self.ts_global.simbolos[i].valor,Etiqueta):
                vla = "Etiqueta"
            elif isinstance(self.ts_global.simbolos[i].valor,Arreglo):
                vla =self.ts_global.simbolos[i].valor.values
            else:
                vla =str(self.ts_global.simbolos[i].valor)
            listBox.insert("", "end", values=(str(self.ts_global.simbolos[i].id),str(self.ts_global.simbolos[i].rol),str(tipo),str(self.ts_global.simbolos[i].dim),vla,self.ts_global.simbolos[i].ambito,self.ts_global.simbolos[i].declarada))
            
        closeButton = tk.Button(newWindow, text="Close", width=15, command=close_window).grid(row=4, column=1)
        closeButton = tk.Button(newWindow, text="Exit", width=15, command=exit).grid(row=4, column=0)

    

    def showtree(self):

        newWindow = Tk()
        label = tk.Label(newWindow, text="Arbol Sintactico", font=("Arial",30))
        label.pack()
        screenWidth = newWindow.winfo_screenwidth() 
        screenHeight = newWindow.winfo_screenheight() 
        widht = 1400
        height =800
        # For left-alling 
        left = (screenWidth / 2) - (widht / 2)  
          
        # For right-allign 
        top = (screenHeight / 2) - (height /2)  
          
        # For top and bottom 
        newWindow.geometry('%dx%d+%d+%d' % (widht, 
                                              height, 
                                              left, top))  
        img = tk.PhotoImage(master=newWindow, file="Arbol.png")
        image_window = ScrollableImage(newWindow, image=img, scrollbarwidth=6, 
                               width=1400, height=800)

        image_window.pack()
    

    def showTE(self):
        def close_window(): 
            newWindow.destroy()
        newWindow = Tk()
        widht = 1200
        height =750
        # For top and bottom 
        newWindow.geometry('%dx%d' % (widht, 
                                              height))
        label = tk.Label(newWindow, text="Tabla de errores", font=("Arial",30)).grid(row=0, columnspan=3)
        cols = ('Tipo de error', 'Descripcion', 'Linea','Columna')
        f1 = tk.Frame(newWindow)
        f1.grid(column=0, row=1,columnspan=2, sticky="ns")
        newWindow.rowconfigure(1, weight=1)
        listBox = ttk.Treeview(f1, columns=cols, show='headings')
        for col in cols:
            listBox.heading(col, text=col)  
            listBox.column(col, width=300,anchor="center") 
        listBox.pack(expand=True, fill='y')
        
        for mensaje in self.errores:
            
            listBox.insert("", "end", values=(str(mensaje.errtype),str(mensaje.text),str(mensaje.linea),str(mensaje.columna)))
        
        closeButton = tk.Button(newWindow, text="Close", width=15, command=close_window).grid(row=4, column=1)
        closeButton = tk.Button(newWindow, text="Exit", width=15, command=exit).grid(row=4, column=0)

    def showGRA(self):
        def close_window(): 
            newWindow.destroy()
        newWindow = Tk()
        widht = 1200
        height =750
        # For top and bottom 
        newWindow.geometry('%dx%d' % (widht, 
                                              height))
        label = tk.Label(newWindow, text="Reporte gramatical", font=("Arial",30)).grid(row=0, columnspan=3)
        cols = ('Produccion', 'Acción')
        f1 = tk.Frame(newWindow)
        f1.grid(column=0, row=1,columnspan=2, sticky="ns")
        newWindow.rowconfigure(1, weight=1)

        listBox = ttk.Treeview(f1, columns=cols, show='headings')
        for col in cols:
            listBox.heading(col, text=col) 
            listBox.column(col, width=600,anchor="w") 
   
        listBox.pack(expand=True, fill='y')
        for regla in sorted(GLO.gramatica.keys()):
            
            listBox.insert("", "end", values=(GLO.gramatica[regla]['rule'],GLO.gramatica[regla]['action']))
        
        closeButton = tk.Button(newWindow, text="Close", width=15, command=close_window).grid(row=4, column=1)
        closeButton = tk.Button(newWindow, text="Exit", width=15, command=exit).grid(row=4, column=0)


    def debug_stop(self):

        print("Debugging Detenido")
        GLO.pila_action = None
        GLO.action_puntero = 0
        GLO.current_etiqueta = None
        GLO.TSG = None
        showinfo("Notice","Debugging Detenido")

        self.DebNX.config(state='disabled')
        self.DebST.config(state='disabled')
        self.ToDEB.config(state='normal')
        self.ToRun.config(state='normal')
        self.ToAST.config(state='normal')
        self.ToDES.config(state='normal')
        self.ToERR.config(state='normal')
        #print(str(GLO.pila_action))

    
    def debug_next(self):

        if GLO.pila_action is not None:
           #do
            if GLO.action_puntero< len(GLO.pila_action):
                instr = GLO.pila_action[GLO.action_puntero]
                print(str(instr))
                if isinstance(instr,GoTo):
                    
                    #change
                    Simbolo = self.ts_global.obtener(instr.id)
                    et = Simbolo.valor
                    if  isinstance(et, Etiqueta):
                        GLO.current_etiqueta = et
                        GLO.pila_action = et.instrucciones
                        GLO.action_puntero = -1
                        
                    else:
                        print("El salto no se dirige a una etiqueta")
                        ms.AddMensaje(MS.Mensaje("El salto no se dirige hacia una etiqueta",self.linea,self.columna,True,"Semantico"))

                elif isinstance(instr, Print):
                    result = instr.debug(self.ts_global,self.ms_global)
                else:
                    if isinstance(instr,Asignacion):
                        instr.etiqueta = GLO.current_etiqueta
                    result = instr.ejecutar(self.ts_global,self.ms_global)

                
                GLO.action_puntero +=1
            else:
                if GLO.current_etiqueta.next is not None:
                    GLO.pila_action = GLO.current_etiqueta.next.instrucciones
                    GLO.current_etiqueta = GLO.current_etiqueta.next
                    GLO.action_puntero = -1
                        
                else:
                    self.debug_stop()
                
        else:
            showinfo("Notice","No se tiene informacion en la pila")

        

        
    
    
    
    
    
    def debug(self):

        print("Iniciando analisis")
        ts_global = TS.TablaDeSimbolos()
        ms_global = MS.Mensajes()
        parser = GR.Gramatica(ms_global)
        input = self.ToAnalize.get("1.0",'end-1c')
        input += " \n exit;"
        instrucciones = parser.parse(input)
        #SinLex = parser.Errors()
        if instrucciones is not None:
                self.debug_instrucciones(instrucciones, ts_global, ms_global)
        salida=""
        showinfo("Notice","Debugging comenzado")

        self.DebNX.config(state='normal')
        self.DebST.config(state='normal')
        self.ToDEB.config(state='disabled')
        self.ToRun.config(state='disabled')
        self.ToAST.config(state='disabled')
        self.ToDES.config(state='disabled')
        self.ToERR.config(state='disabled')
        self.ts_global = ts_global
        self.ms_global = ms_global
        #print(str(GLO.pila_action))



    def analizardesc(self):

        print("Iniciando analisis")
        ts_global = TS.TablaDeSimbolos()
        ms_global = MS.Mensajes()
        parser = GR.Gramatica(ms_global)
        GLO.gramatica = {
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
        GLO.isdesc = True
        input = self.ToAnalize.get("1.0",'end-1c')
        input += " \n exit;"
        instrucciones = parser.parse(input)
        #SinLex = parser.Errors()

        if instrucciones is not None:
                self.procesar_instrucciones(instrucciones, ts_global, ms_global)
        salida=""
        if (ms_global.correcto):
            print("Analisis correcto")
            showinfo("Notepad","Analisis correcto")
            prints = ms_global.GetMensajes()
            for Mensaje in prints:
                print(Mensaje.constructMensaje())
                salida+=Mensaje.constructMensaje() 
            arparser = ARDES.ASTDES()
            raiz = arparser.parse(input)
            graf = TreeMaker(raiz)
            try:
                graf.crearArbol()
            except:
                print ("No se genero el arbol")
            #self.ToTS.config(state='normal')
            #self.ToERR.config(state='disabled')
            
        else:
            print("Se encontraron errores")
            showinfo("Notepad","Se encontraron errores")
            self.errores = ms_global.GetErrores()
            
            '''if (SinLex is not None):
                for Mensaje in SinLex.mensajes:
                    print(Mensaje.constructError())
                    salida+=Mensaje.constructError()'''
            for Mensaje in self.errores:
                print(Mensaje.constructError())
                salida+=Mensaje.constructError()
            #self.ToTS.config(state='disabled')
            #self.ToERR.config(state='normal')

        self.setText(salida)
        self.ts_global=ts_global
        self.ms_global = ms_global
        self.ts_global.printts()


    


    def analizar(self):
        print("current limit:"+str(sys.getrecursionlimit()))
        print("Iniciando analisis")
        ts_global = TS.TablaDeSimbolos()
        ms_global = MS.Mensajes()
        parser = GR.Gramatica(ms_global)
        GLO.gramatica = {}
        GLO.isdesc = False
        input = self.ToAnalize.get("1.0",'end-1c')
        input += " \n exit;"
        instrucciones = parser.parse(input)
        #SinLex = parser.Errors()



        if instrucciones is not None:
                self.procesar_instrucciones(instrucciones, ts_global, ms_global)
        salida=""
        if (ms_global.correcto):
            print("Analisis correcto")
            showinfo("Notepad","Analisis correcto")
            prints = ms_global.GetMensajes()
            for Mensaje in prints:
                print(Mensaje.constructMensaje())
                salida+=Mensaje.constructMensaje() 
            arparser = AR.AST()
            raiz = arparser.parse(input)
            graf = TreeMaker(raiz)
            try:
                graf.crearArbol()
            except:
                print ("No se genero el arbol")
            #self.ToTS.config(state='normal')
            #self.ToERR.config(state='disabled')
            
        else:
            print("Se encontraron errores")
            showinfo("Notepad","Se encontraron errores")
            self.errores = ms_global.GetErrores()
            
            '''if (SinLex is not None):
                for Mensaje in SinLex.mensajes:
                    print(Mensaje.constructError())
                    salida+=Mensaje.constructError()'''
            for Mensaje in self.errores:
                print(Mensaje.constructError())
                salida+=Mensaje.constructError()
            #self.ToTS.config(state='disabled')
            #self.ToERR.config(state='normal')

        self.setText(salida)
        self.ts_global = ts_global
        self.ms_global = ms_global
        self.ts_global.printts()



    def __init__(self,**kwargs): 
  
        GLO.window = Tk()
        # default window width and height 
        self.__thisWidth = 300
        self.__thisHeight = 300
        self.ToAnalize = CustomText(GLO.window)
        GLO.ToConsole = Text(GLO.window,height = 200, background="#2A2C2E",foreground="#24EA3C") 
        self.Frame1 = Frame(GLO.window,height = 40) 
        self.Frame2 = Frame(GLO.window,height = 20) 
        self.Fleft = Text(GLO.window,width = 30) 
        self.Fright = Text(GLO.window, width=20) 

        self.playico = PhotoImage(file="./ico/play7.png")
        self.playpic = self.playico.subsample(25,25)

        self.debico = PhotoImage(file="./ico/debug.png")
        self.debpic = self.debico.subsample(14,14)

        self.desico = PhotoImage(file="./ico/play4.png")
        self.despic = self.desico.subsample(12,12)

        self.ToRun = Button(self.Frame1, text = 'Analizar',bd=0, command =self.analizar)
        self.ToTS = Button(self.Frame1, text = 'Tabla de Simbolos', command =self.showTS, state='normal')
        self.ToAST = Button(self.Frame1, text = 'AST', command =self.showtree)
        self.ToDES = Button(self.Frame1, text = 'Descendente',bd=0, command =self.analizardesc)
        self.ToDEB = Button(self.Frame1, text = 'Debugger',bd=0, command =self.debug)
        self.DebNX = Button(self.Frame1, text = 'Next',bd=0,state ='disabled',command =self.debug_next)
        self.DebST = Button(self.Frame1, text = 'Stop',bd=0,state='disabled',command =self.debug_stop)
        self.ToGRA = Button(self.Frame1, text = 'Gramatica',command =self.showGRA)
        self.ToERR = Button(self.Frame1, text = 'Tabla Errores',command =self.showTE,state='normal')
        self.MenuBar = Menu(GLO.window) 
        self.BarFile = Menu(self.MenuBar, tearoff=0) 
        self.BarEdit = Menu(self.MenuBar, tearoff=0) 
        self.BarOptions = Menu(self.MenuBar, tearoff=0) 
        self.BarHelp = Menu(self.MenuBar, tearoff=0) 
        self.linenumbers = TextLineNumbers(self.Fleft, width=20)
        # To add scrollbar 
        self.ScrollA = Scrollbar(self.Fright)      
        self.ScrollC = Scrollbar(GLO.ToConsole)      
        self.archivo = None
        self.errores = None
        self.shouldcolor = False
        self.backcolor = 0
        self.shouldlines =True
        set
        # Set icon 
        try: 
                GLO.window.wm_iconbitmap("./ico/not2.png")  
        except: 
                pass
  
        # Set window size (the default is 300x300) 
  
        try: 
            self.__thisWidth = kwargs['width'] 
        except KeyError: 
            pass
  
        try: 
            self.__thisHeight = kwargs['height'] 
        except KeyError: 
            pass
  
        # Set the window text 
        GLO.window.title("Untitled - Notepad") 
  
        # Center the window 
        screenWidth = GLO.window.winfo_screenwidth() 
        screenHeight = GLO.window.winfo_screenheight() 
      
        # For left-alling 
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # For right-allign 
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # For top and bottom 
        GLO.window.geometry('%dx%d+%d+%d' % (self.__thisWidth, 
                                              self.__thisHeight, 
                                              left, top))  
  
        # To make the textarea auto resizable 
        GLO.window.rowconfigure(1, weight=3) 
        GLO.window.rowconfigure(3, weight=1) 
        GLO.window.columnconfigure(1, weight=1) 
  
        # Add controls (widget) 
        self.ToRun.config(image = self.playpic)
        self.ToDEB.config(image = self.debpic)
        self.ToDES.config(image = self.despic)
        self.ToRun.grid(row = 0,column=5,padx = 23)
        self.ToTS.grid(row = 0,column=0,padx = 21)
        self.ToAST.grid(row = 0,column=1,padx = 21)
        self.ToDES.grid(row = 0,column=6,padx = 21)
        self.ToERR.grid(row = 0,column=7,padx = 21)
        self.ToDEB.grid(row = 0,column=3)
        self.DebST.grid(row = 0,column=2)
        self.DebNX.grid(row = 0,column=4)
        self.ToGRA.grid(row = 0,column=8,padx = 21)
        self.ToAnalize.grid(row=1,column=1,sticky = N + E + S + W) 
        self.Frame1.grid(row=0,column=1,sticky = N + E + S + W)
        self.Frame2.grid(row=2,column=1,sticky = N + E + S + W)
        GLO.ToConsole.grid(row=3,column=1,sticky = N + E + S + W)
        self.Fleft.grid(row=1,column=0,sticky = N + E + S + W)
        self.Fright.grid(row=1,column=2,sticky = N + E + S + W)
          
        # To open new file 
        self.BarFile.add_command(label="New", 
                                        command=self.__newFile)     
          
        # To open a already existing file 
        self.BarFile.add_command(label="Open", 
                                        command=self.__openFile) 
          
        # To save current file 
        self.BarFile.add_command(label="Save", 
                                        command=self.__saveFile)  

        self.BarFile.add_command(label="Save As", 
                                        command=self.__saveFileAs)   

  
        # To create a line in the dialog         
        self.BarFile.add_separator()    
        self.BarFile.add_command(label="Close", 
                                        command=self.__newFile)                                          
        self.BarFile.add_command(label="Exit", 
                                        command=self.__quitApplication) 
        self.MenuBar.add_cascade(label="File", 
                                       menu=self.BarFile)      
          
        # To give a feature of cut  
        self.BarEdit.add_command(label="Cut", 
                                        command=self.__cut)              
      
        # to give a feature of copy     
        self.BarEdit.add_command(label="Copy", 
                                        command=self.__copy)          
          
        # To give a feature of paste 
        self.BarEdit.add_command(label="Paste", 
                                        command=self.__paste)          
          
        # To give a feature of editing 
        self.MenuBar.add_cascade(label="Edit", 
                                       menu=self.BarEdit)      

        # To give a feature of cut  
        self.BarOptions.add_command(label="Toogle Colors", 
                                        command=self.__toggleColors)  
        self.BarOptions.add_command(label="Toogle Lines", 
                                        command=self.__toggleLines)              
        self.BarOptions.add_command(label="Change Background color", 
                                        command=self.__backgroundchange)  
          
        # To give a feature of editing 
        self.MenuBar.add_cascade(label="Options", 
                                       menu=self.BarOptions)     
          
        # To create a feature of description of the notepad 
        self.BarHelp.add_command(label="Help", 
                                        command=self.__showAbout) 
        self.BarHelp.add_command(label="About", 
                                        command=self.__showAbout) 
        self.MenuBar.add_cascade(label="Help", 
                                       menu=self.BarHelp) 
  
        GLO.window.config(menu=self.MenuBar) 
  
        self.ScrollA.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        self.ScrollA.config(command=self.Fright.yview)      
        self.Fright.config(yscrollcommand=self.ScrollA.set) 

        self.ScrollC.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        self.ScrollC.config(command=GLO.ToConsole.yview)      
        GLO.ToConsole.config(yscrollcommand=self.ScrollC.set) 
      
        self.linenumbers.attach(self.ToAnalize)
        self.linenumbers.pack(side=LEFT, fill=Y)

        self.ToAnalize.bind("<<Change>>", self._on_change)
        self.ToAnalize.bind("<Configure>", self._on_change)
        GLO.window.bind("<space>", self.syn)


    def syn(self,event=None):

        def colorize(word, color):
            index = []
            index1 = self.ToAnalize.search(word, "1.0", "end")
            while index1:
                index2 = ".".join([index1.split(".")[0], str(int(index1.split(".")[1]) + len(word))])
                index.append((index1, index2))
                index1 = self.ToAnalize.search(word, index2, "end")
            for i, j in index:
                self.ToAnalize.tag_add(word, i, j)
                self.ToAnalize.tag_configure(word, foreground=color)
        if self.shouldcolor:
            text = self.ToAnalize.get("1.0", "end")
            for token, content in lex(text, PythonLexer()):
                if token == Token.Literal.Number.Integer:
                    colorize(content, color="purple")
                elif token == Token.Operator.Word:
                    colorize(content, color="red")
                elif token == Token.Name.Builtin:
                    colorize(content, color="blue")
                elif token == Token.Comment.Hashbang or token == Token.Comment.Single:
                    colorize(content, color="grey")
                elif token == Token.Keyword.Namespace:
                    colorize(content, color="yellow")
                elif token == Token.Namespace:
                    colorize(content, color="green")
                elif token == Token.Punctuation:
                    colorize(content, color="brown")
                elif token == Token.Literal.String.Double:
                    colorize(content, color="orange")
                elif token == Token.Name:
                    if (content == "char")or(content=="goto"):
                        colorize(content, color="#20C2BA")
                    else:
                        colorize(content, color="green")
                elif (content == "$"):
                        colorize(content, color="green")
            

    

    def _on_change(self, event):
        
        self.linenumbers.redraw()
        if self.shouldlines:
            self.linenumbers.pack(side=LEFT, fill=Y)
        else:
            self.linenumbers.pack_forget()


    def __quitApplication(self): 
        GLO.window.destroy() 
        # exit() 
  
    def __showAbout(self): 
        showinfo("About","Fernando Andrés Mérida Antón \n 201314713") 
  
    def __openFile(self): 
          
        self.archivo = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
  
        if self.archivo == "": 
              
            # no file to open 
            self.archivo = None
        else: 
              
            # Try to open the file 
            # set the window title 
            GLO.window.title(os.path.basename(self.archivo) + " - Notepad") 
            self.ToAnalize.delete(1.0,END) 
  
            file = open(self.archivo,"r") 
  
            self.ToAnalize.insert(1.0,file.read()) 
  
            file.close() 
  
          
    def __newFile(self): 
        GLO.window.title("Untitled - Notepad") 
        self.archivo = None
        self.ToAnalize.delete(1.0,END) 
  
    def __saveFile(self): 
  
        if self.archivo == None: 
            # Save as new file 
            self.archivo = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.archivo == "": 
                self.archivo = None
            else: 
                  
                # Try to save the file 
                file = open(self.archivo,"w") 
                file.write(self.ToAnalize.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                GLO.window.title(os.path.basename(self.archivo) + " - Notepad") 
                  
              
        else: 
            file = open(self.archivo,"w") 
            file.write(self.ToAnalize.get(1.0,END)) 
            file.close() 

    def __saveFileAs(self): 
  
            # Save as new file 
            self.archivo = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.archivo == "": 
                self.archivo = None
            else: 
                  
                # Try to save the file 
                file = open(self.archivo,"w") 
                file.write(self.ToAnalize.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                GLO.window.title(os.path.basename(self.archivo) + " - Notepad") 
                  
              
        
  
    def __cut(self): 
        self.ToAnalize.event_generate("<<Cut>>") 
  
    def __copy(self): 
        self.ToAnalize.event_generate("<<Copy>>") 
  
    def __paste(self): 
        self.ToAnalize.event_generate("<<Paste>>") 
    
    def __toggleColors(self): 
        if self.shouldcolor:
            self.shouldcolor = False
        else:
            self.shouldcolor = True

    def __toggleLines(self): 
        if self.shouldlines:
            self.shouldlines = False
        else:
            self.shouldlines = True
    
    def __backgroundchange(self): 
        self.backcolor +=1
        if self.backcolor == 0:
            self.ToAnalize.configure(background="white")
        elif self.backcolor == 1:
            self.ToAnalize.configure(background="#e1f1fa")
        elif self.backcolor == 2:
            self.ToAnalize.configure(background="#faded9")
        elif self.backcolor == 3:
            self.ToAnalize.configure(background="#ecffe6")
        elif self.backcolor == 4:
            self.ToAnalize.configure(background="#f6d5f7")
        elif self.backcolor == 5:
            self.ToAnalize.configure(background="#c1f6f7")
            self.backcolor = -1
        else:
            self.ToAnalize.configure(background="white")
  
    def run(self): 
  
        # Run main application 
        GLO.window.mainloop() 


  
  # Run main application 
notepad = Notepad(width=800,height=800) 
notepad.run() 