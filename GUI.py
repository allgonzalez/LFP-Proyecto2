from tkinter import*
import tkinter as tk
from tkinter import filedialog

from Analizador import Analizador

analizador = Analizador()
#Funciones
def abrirArchvo1():
    global archivo, textoLeido
    archivo = filedialog.askopenfilename(title="Abrir", filetypes=[("pixeles", "*.lfp")])
    archivos_texto = open(archivo, 'r')
    textoLeido = archivos_texto.read()
    textoEntrada.insert(tk.END, textoLeido)

def obtenerTextoYGuardar():
    global textoObtenido

    textoObtenido = textoEntrada.get(1.0, tk.END+"-1c")

    print(textoObtenido)

    docLFP = open(archivo,"w")
    docLFP.write(textoObtenido)
    docLFP.close()

    archivos_texto = open(archivo, 'r')
    textoLeido = archivos_texto.read()
    analizador.scanner(textoLeido)
    analizador.imprimirTokens()
    analizador.imprimirErrores()
    analizador.Claves()
    analizador.Registros()


#Root
ventana = Tk()
ventana.config(background="#044D9A")

ventana.geometry("1200x900")
ventana.title("Editor de base de datos")

#Ventana de edicion y lectura de texto
textoEntrada = Text(ventana, height=40, width=70, bg="#313131", fg="white", font=("Consolas", 11)) 
textoEntrada.place(x=10, y=100)

textoSalida = Text(ventana, height=40, width=70, bg="#313131", fg="white", state="disable", font=("Consolas", 11))
textoSalida.place(x=600, y=100)

#Botones
btnAbrirArchivo = Button(ventana, height=2, width=10, text="Abrir archivo", command = abrirArchvo1, background="#368807", font=("Verdana",10), fg="white")
btnAbrirArchivo.place(x=320, y=50)

btnAnalizar = Button(ventana, height=2, width=10, text="Compilar", command=obtenerTextoYGuardar, background="#10139E", font=("Verdana",10), fg="white")
btnAnalizar.place(x=420, y=50)

btnReporeteTokensValidos = Button(ventana, height=2, width=12, text="Tokens válidos", background="#8E8C08", font=("Verdana",10), fg="white")
btnReporeteTokensValidos.place(x=515, y=50)

btnReporeteTokensInvalidos = Button(ventana, height=2, width=13, text="Tokens inválidos", background="#B03314", font=("Verdana",10), fg="white")
btnReporeteTokensInvalidos.place(x=630, y=50)

btnReporeteGrpahviz = Button(ventana, height=2, width=10, text="Graphviz" , background="#0D9597", font=("Verdana",10), fg="white")
btnReporeteGrpahviz.place(x=750, y=50)

#Labels
labelEditor = Label (ventana, text ="EDITOR DE TEXTO", font=("Verdana",15), background="#044D9A", fg="white")
labelEditor.place(x=90, y=50)

labelTerminal = Label (ventana, text ="TERMINAL", font=("Verdana",15), background="#044D9A", fg="white")
labelTerminal.place(x=900, y=50)

ventana.mainloop()
