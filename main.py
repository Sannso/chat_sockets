from tkinter import *
from tkinter import ttk
import tkinter
from traceback import print_tb

root = Tk()

frm = ttk.Frame(root, padding=10)
frm.grid(padx=5, pady=10)

#Vars
texto = ""
#####

#Funcs
def setTextBox(widget, text):
    widget.insert(tkinter.END, text)
    print(text)
    widget.update()

######

ttk.Label(frm, text="Chat...", justify="left").grid(column=0, row=0, sticky="w")

sb = ttk.Scrollbar(frm)
cuadro_texto = tkinter.Text(frm, height=20, width=50, pady=10, padx=10, yscrollcommand=Scrollbar(root).set)
cuadro_texto.grid(column=0, row=1, sticky="w", pady=10)
#cuadro_texto.update()
# Obtener info de la pantalla: cuadro_texto.get("1.0","end-1c")
sb.grid(column=1, row=1, sticky="wns") 
sb.config(command=cuadro_texto.yview)

chat = ttk.Entry(frm, width=50, textvariable= texto)
chat.grid(column=0, row=3, sticky="sw")


ttk.Button(frm, text="Eviar mensaje", command=lambda: setTextBox(cuadro_texto, (chat.get()+"\n"))
            ).grid(column=1, row=3, sticky="sw", padx=5)
 
ttk.Separator(frm).grid(column=4, row=0)
ttk.Label(frm, text="Aqui va un archivo", justify="left").grid(column=5, row=0, sticky="s")
ttk.Button(frm, text="Subir archivo").grid(column=5, row=1, sticky="n")



root.mainloop()
