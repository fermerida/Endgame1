from expresiones import *
import ts as TS
import mensajes as MS
import globalvar as GLO

import tkinter as tk
from tkinter import *
class CustomDialog(object):
    def __init__(self, parent, prompt="", default=""):
        self.root = parent
        self.popup = tk.Toplevel(parent)
        self.popup.title(prompt)
        self.popup.transient(parent)

        self.var = tk.StringVar(value=default)

        label = tk.Label(self.popup, text=prompt)
        entry = tk.Entry(self.popup, textvariable=self.var)
        buttons = tk.Frame(self.popup)

        buttons.pack(side="bottom", fill="x")
        label.pack(side="top", fill="x", padx=20, pady=10)
        entry.pack(side="top", fill="x", padx=20, pady=10)

        ok = tk.Button(buttons, text="Ok", command=self.popup.destroy)
        ok.pack(side="top")
        entry.bind("<Return>",  lambda e: self.popup.destroy)


        self.entry = entry

    def show(self):
        self.entry.focus_force()
        self.root.wait_window(self.popup)
        return self.var.get()
        
class Read(Exp) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,linea,columna) :
        self.root = GLO.window
        self.linea = linea
        self.columna = columna
        self.tipo = None



    def GetValor(self, ts,ms):

        dialog = CustomDialog(self.root, prompt="Ingresa valor para Read:")
        val = dialog.show()   
        try:
            val = int(val)
            self.tipo =TS.TIPO_DATO.INTEGER
        except ValueError:
            try:
                val = float(val)
                self.tipo =TS.TIPO_DATO.FLOAT
            except ValueError:
                self.tipo =  TS.TIPO_DATO.CHAR


        print ("valor: "+ str(val) + "tipo: "+ str(self.tipo) )
        return val

    def GetTipo(self, ts,ms):

        return self.tipo

