import threading
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog

import clienteG

#def loadWindow():
root = Tk()

frm = ttk.Frame(root, padding=10)
frm.grid(padx=5, pady=10)

#Vars
url_file = StringVar()
url_file.set("Aun no hay archivo")
loadOnce = True
#####

#Funcs
def setTextBox(widget, text):
    widget.configure(state="normal")
    widget.insert(tkinter.END, text)
    widget.configure(state="disable")
    widget.update()

def openFile(url_file):
    url = filedialog.askopenfilename(initialdir="/", title="Select file",
                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    url_file.set(url)


def loadMss(widget):
    while(True):
        if(clienteG.LOAD):
            widget.configure(state="normal")
            for text in clienteG.MSS:
                widget.insert(tkinter.END, (text+"\n"))
            widget.configure(state="disable")
            widget.update()
            clienteG.LOAD = False

######

ttk.Label(frm, text="Chat...", justify="left").grid(column=0, row=0, sticky="w")

sb = ttk.Scrollbar(frm)
cuadro_texto = tkinter.Text(frm, state="disable", height=20, width=50, pady=10, padx=10, yscrollcommand=Scrollbar(root).set)
cuadro_texto.grid(column=0, row=1, sticky="w", pady=10)
#cuadro_texto.update()
# Obtener info de la pantalla: cuadro_texto.get("1.0","end-1c")
sb.grid(column=1, row=1, sticky="wns") 
sb.config(command=cuadro_texto.yview)

chat = ttk.Entry(frm, width=55, state="disable")
chat.grid(column=0, row=3, sticky="sw")


ttk.Button(frm, text="Eviar mensaje", command=lambda: setTextBox(cuadro_texto, (chat.get()+"\n"))
            ).grid(column=1, row=3, sticky="sw", padx=5)

ttk.Separator(frm).grid(column=4, row=0)
labelURL = ttk.Label(frm, textvariable=url_file, justify="left")
labelURL.grid(column=5, row=0, sticky="s")
botonFile = ttk.Button(frm, text="Subir archivo", command=lambda:openFile(url_file))
botonFile.grid(column=5, row=1, sticky="n")

if(loadOnce):
    receiving_thread = threading.Thread(target=clienteG.runClient)
    receiving_thread.start()

    thread_box = threading.Thread(target=loadMss, args=[cuadro_texto])
    thread_box.start()
    loadOnce = False 
    
root.mainloop()
