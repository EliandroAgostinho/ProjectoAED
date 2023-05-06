#Interação com utilizador
import tkinter as tk

#def func_principal():
#   pass

class View:
    def __init__(self,master):
        self.master=master
        self.frame=tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Bem-vindo a AED")
        self.label.pack()

        self.text_entry=tk.Entry(self.frame)        
        self.text_entry.pack()