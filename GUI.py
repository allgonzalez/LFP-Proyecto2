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
    texto.insert(tk.END, textoLeido)

def obtenerTextoYGuardar():
    global textoObtenido

    textoObtenido = texto.get(1.0, tk.END+"-1c")

    print(textoObtenido)

    docLFP = open(archivo,"w")
    docLFP.write(textoObtenido)
    docLFP.close()

    archivos_texto = open(archivo, 'r')
    textoLeido = archivos_texto.read()
    analizador.scanner(textoLeido)
    analizador.imprimirTokens()
    analizador.imprimirErrores()


ventana = Tk()

ventana.geometry("1200x800")
ventana.title("Editor de base de datos")

texto = Text(ventana, height=35, width=60, bg="light yellow")
texto.place(x=10, y=100)

#Botones
btnAnalizar = Button(ventana, height=1, width=10, text="Compilar", command=obtenerTextoYGuardar)
btnAnalizar.place(x=500, y=80)

btnAbrirArchivo = Button(ventana, height=1, width=10, text="Abrir archivo", command = abrirArchvo1)
btnAbrirArchivo.place(x=500, y=150)

ventana.mainloop()
