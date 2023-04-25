#Rodar o projecto
from view import*
import tkinter as tk 
from controller import*

if __name__=='__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
