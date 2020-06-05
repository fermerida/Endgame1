import tkinter as tk
import os     
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import gramatica as g
import ts as TS
from instrucciones import *
from arbol import *
from etiquetas import *
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

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
    def procesar_instrucciones(self,instrucciones, ts) :
    ## lista de instrucciones recolectadas
        for i in range(len(instrucciones)) :
            if i < len(instrucciones)-1:
                instrucciones[i].inicializar(ts,instrucciones[i+1])
            else:
                instrucciones[i].inicializar(ts,None)
        for instr in instrucciones :
            if (instr.id=="main"):
                instr.ejecutar(ts)


    def analizar(self):
        input = self.ToAnalize.get("1.0",'end-1c')
        instrucciones = g.parse(input)
        ts_global = TS.TablaDeSimbolos()

        self.procesar_instrucciones(instrucciones, ts_global)
        showinfo("Notepad",input) 


    def __init__(self,**kwargs): 
        self.window = Tk() 
    

        # default window width and height 
        self.__thisWidth = 300
        self.__thisHeight = 300
        self.ToAnalize = CustomText(self.window) 
        self.ToConsole = Text(self.window,height = 200, background="#2A2C2E",foreground="#24EA3C") 
        self.Frame1 = Frame(self.window,height = 40) 
        self.Frame2 = Frame(self.window,height = 20) 
        self.Fleft = Text(self.window,width = 10) 
        self.Fright = Text(self.window, width=20) 
        self.ToRun = Button(self.window, text = 'Analizar', command =self.analizar)
        self.__thisMenuBar = Menu(self.window) 
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0) 
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0) 
        self.__thisHelpMenu = Menu(self.__thisMenuBar, tearoff=0) 
        self.linenumbers = TextLineNumbers(self.Fleft, width=10)
        # To add scrollbar 
        self.ScrollA = Scrollbar(self.Fright)      
        self.ScrollC = Scrollbar(self.ToConsole)      
        self.__file = None
        set
        # Set icon 
        try: 
                self.window.wm_iconbitmap("Notepad.ico")  
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
        self.window.title("Untitled - Notepad") 
  
        # Center the window 
        screenWidth = self.window.winfo_screenwidth() 
        screenHeight = self.window.winfo_screenheight() 
      
        # For left-alling 
        left = (screenWidth / 2) - (self.__thisWidth / 2)  
          
        # For right-allign 
        top = (screenHeight / 2) - (self.__thisHeight /2)  
          
        # For top and bottom 
        self.window.geometry('%dx%d+%d+%d' % (self.__thisWidth, 
                                              self.__thisHeight, 
                                              left, top))  
  
        # To make the textarea auto resizable 
        self.window.rowconfigure(1, weight=3) 
        self.window.rowconfigure(3, weight=1) 
        self.window.columnconfigure(1, weight=1) 
  
        # Add controls (widget) 
        self.ToRun.grid(row = 0,column=1,padx = 100)
        self.ToAnalize.grid(row=1,column=1,sticky = N + E + S + W) 
        self.Frame1.grid(row=0,column=1,sticky = N + E + S + W)
        self.Frame2.grid(row=2,column=1,sticky = N + E + S + W)
        self.ToConsole.grid(row=3,column=1,sticky = N + E + S + W)
        self.Fleft.grid(row=1,column=0,sticky = N + E + S + W)
        self.Fright.grid(row=1,column=2,sticky = N + E + S + W)
          
        # To open new file 
        self.__thisFileMenu.add_command(label="New", 
                                        command=self.__newFile)     
          
        # To open a already existing file 
        self.__thisFileMenu.add_command(label="Open", 
                                        command=self.__openFile) 
          
        # To save current file 
        self.__thisFileMenu.add_command(label="Save", 
                                        command=self.__saveFile)     
  
        # To create a line in the dialog         
        self.__thisFileMenu.add_separator()                                          
        self.__thisFileMenu.add_command(label="Exit", 
                                        command=self.__quitApplication) 
        self.__thisMenuBar.add_cascade(label="File", 
                                       menu=self.__thisFileMenu)      
          
        # To give a feature of cut  
        self.__thisEditMenu.add_command(label="Cut", 
                                        command=self.__cut)              
      
        # to give a feature of copy     
        self.__thisEditMenu.add_command(label="Copy", 
                                        command=self.__copy)          
          
        # To give a feature of paste 
        self.__thisEditMenu.add_command(label="Paste", 
                                        command=self.__paste)          
          
        # To give a feature of editing 
        self.__thisMenuBar.add_cascade(label="Edit", 
                                       menu=self.__thisEditMenu)      
          
        # To create a feature of description of the notepad 
        self.__thisHelpMenu.add_command(label="About Notepad", 
                                        command=self.__showAbout)  
        self.__thisMenuBar.add_cascade(label="Help", 
                                       menu=self.__thisHelpMenu) 
  
        self.window.config(menu=self.__thisMenuBar) 
  
        self.ScrollA.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        self.ScrollA.config(command=self.Fright.yview)      
        self.Fright.config(yscrollcommand=self.ScrollA.set) 

        self.ScrollC.pack(side=RIGHT,fill=Y)                     
          
        # Scrollbar will adjust automatically according to the content         
        self.ScrollC.config(command=self.ToConsole.yview)      
        self.ToConsole.config(yscrollcommand=self.ScrollC.set) 
      
        self.linenumbers.attach(self.ToAnalize)
        self.linenumbers.pack(side=LEFT, fill=Y)

        self.ToAnalize.bind("<<Change>>", self._on_change)
        self.ToAnalize.bind("<Configure>", self._on_change)
        

    def _on_change(self, event):
        self.linenumbers.redraw()

    def __quitApplication(self): 
        self.window.destroy() 
        # exit() 
  
    def __showAbout(self): 
        showinfo("Notepad","Mrinal Verma") 
  
    def __openFile(self): 
          
        self.__file = askopenfilename(defaultextension=".txt", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Text Documents","*.txt")]) 
  
        if self.__file == "": 
              
            # no file to open 
            self.__file = None
        else: 
              
            # Try to open the file 
            # set the window title 
            self.window.title(os.path.basename(self.__file) + " - Notepad") 
            self.ToAnalize.delete(1.0,END) 
  
            file = open(self.__file,"r") 
  
            self.ToAnalize.insert(1.0,file.read()) 
  
            file.close() 
  
          
    def __newFile(self): 
        self.window.title("Untitled - Notepad") 
        self.__file = None
        self.ToAnalize.delete(1.0,END) 
  
    def __saveFile(self): 
  
        if self.__file == None: 
            # Save as new file 
            self.__file = asksaveasfilename(initialfile='Untitled.txt', 
                                            defaultextension=".txt", 
                                            filetypes=[("All Files","*.*"), 
                                                ("Text Documents","*.txt")]) 
  
            if self.__file == "": 
                self.__file = None
            else: 
                  
                # Try to save the file 
                file = open(self.__file,"w") 
                file.write(self.ToAnalize.get(1.0,END)) 
                file.close() 
                  
                # Change the window title 
                self.window.title(os.path.basename(self.__file) + " - Notepad") 
                  
              
        else: 
            file = open(self.__file,"w") 
            file.write(self.ToAnalize.get(1.0,END)) 
            file.close() 
  
    def __cut(self): 
        self.ToAnalize.event_generate("<<Cut>>") 
  
    def __copy(self): 
        self.ToAnalize.event_generate("<<Copy>>") 
  
    def __paste(self): 
        self.ToAnalize.event_generate("<<Paste>>") 
  
    def run(self): 
  
        # Run main application 
        self.window.mainloop() 



  
  
  # Run main application 
notepad = Notepad(width=800,height=700) 
notepad.run() 