from tkinter import*
import tkinter as tk
from tkinter import filedialog
from tkinter.font import families

from Analizador import Analizador

analizador = Analizador()

#Funciones


def reporteTokens():
    analizador.reporteTokensValidos()

def reporteErrores():
    analizador.reportesErrores()
    analizador.erroresSintacticos.clear()

def abrirArchvo1():
    global archivo, textoLeido

    textoEntrada.delete('1.0', END)

    archivo = filedialog.askopenfilename(title="Abrir", filetypes=[("pixeles", "*.lfp")])
    archivos_texto = open(archivo, 'r')
    textoLeido = archivos_texto.read()
    textoEntrada.insert(tk.END, textoLeido)

def Compilar():
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
    

    textoSalida.configure(state='normal')
    textoSalida.delete('1.0', END)
    textoSalida.configure(state='disabled')

    boolimprimir = False
    boolimprimirln = False
    boolpromedio = False
    boolsuma = False
    boolmax = False
    boolmin = False
    boolcontarsi = False
    boolreporte = False
    nombre = ''
    salidaN = ''
    clave = ''
    numero = 0


    if analizador.generarErrores == False:
        analizador.Claves()
        analizador.Registros()
        analizador.SintacticoImprimirReporte()
        analizador.sintacticoConteoDatos()
        analizador.sintacticoPromMaxMinSum()
        analizador.sintacticoContarSi()


    if analizador.generarErrores == False:
        

        for i in analizador.tokens:

            #Imprimir cadena sin salto de linea
            if i.getLexema().lower() == 'imprimir':
                boolimprimir = True
            elif i.getTipo() == 'CADENA' and boolimprimir:
                salidaN = str(i.getLexema()) 
                textoSalida.configure(state='normal')
                textoSalida.insert(END, salidaN)
                textoSalida.configure(state='disabled')
            elif i.getTipo() == 'PUNTO Y COMA' and boolimprimir:
                salidaN = ''
                boolimprimir= False
            
            #Imprimir cadenas con salto de linea
            elif i.getLexema().lower() == 'imprimirln':
                boolimprimirln = True

            elif i.getTipo() == 'CADENA' and boolimprimirln:
                salidaLn = str(i.getLexema())+'\n'
                textoSalida.configure(state='normal')
                textoSalida.insert(END, salidaLn)
                textoSalida.configure(state='disabled')
            elif i.getTipo() == 'PUNTO Y COMA' and boolimprimirln:
                salidaLn = ''
                boolimprimirln = False
            

            #Opcion de mostar los datos
            elif i.getLexema().lower() == 'datos':
                

                for i in analizador.claves:
                    textoSalida.configure(state='normal')
                    textoSalida.insert(END, i+'   ')
                    textoSalida.configure(state='disabled')
                
                #Crear un salto de linea
                textoSalida.configure(state='normal')
                textoSalida.insert(END,'\n')
                textoSalida.configure(state='disabled')
                cont = 0

                for j in analizador.registros:
                    if cont != len(analizador.claves):
                        textoSalida.configure(state='normal')
                        textoSalida.insert(END, j.getRegistro()+'       ')
                        textoSalida.configure(state='disabled')
                    else:
                        textoSalida.configure(state='normal')
                        textoSalida.insert(END,'\n' + j.getRegistro()+ '        ')
                        textoSalida.configure(state='disabled')
                        cont = 0
                    cont += 1
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END,'\n')
                textoSalida.configure(state='disabled')
            #Promedio
            elif i.getLexema().lower()=='promedio':
                boolpromedio = True
            
            elif i.getTipo() == 'CADENA' and boolpromedio:
                clave = i.getLexema()
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END, analizador.Promedio(clave) + '\n')
                textoSalida.configure(state='disabled')

                clave = ''
                boolpromedio = False

            #Conteo
            elif i.getLexema().lower() == 'conteo':
                datosTotales = (len(analizador.registros)) / (len(analizador.claves))
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END,str(datosTotales) +'\n')
                textoSalida.configure(state='disabled')
            
            #Suma de un campo
            elif i.getLexema().lower()=='sumar':
                boolsuma = True
            
            elif i.getTipo() == 'CADENA' and boolsuma:
                clave = i.getLexema()
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END, analizador.Sumar(clave) + '\n')
                textoSalida.configure(state='disabled')

                clave = ''
                boolsuma = False
            
            #Maximo
            elif i.getLexema().lower()=='max':
                boolmax = True
            
            elif i.getTipo() == 'CADENA' and boolmax:
                clave = i.getLexema()
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END, analizador.Maximo(clave) + '\n')
                textoSalida.configure(state='disabled')

                clave = ''
                boolmax = False
            
            #Minimo
            elif i.getLexema().lower()=='min':
                boolmin = True
            
            elif i.getTipo() == 'CADENA' and boolmin:
                clave = i.getLexema()
                
                textoSalida.configure(state='normal')
                textoSalida.insert(END, analizador.Minimo(clave) + '\n')
                textoSalida.configure(state='disabled')

                clave = ''
                boolmin = False

            #Contar si

            elif i.getLexema().lower() == 'contarsi':
                boolcontarsi = True
            
            elif i.getTipo() == 'CADENA' and boolcontarsi:
                clave = i.getLexema()
            elif i.getTipo() == 'NUMERO' and boolcontarsi:
                numero = i.getLexema()

                textoSalida.configure(state='normal')
                textoSalida.insert(END, analizador.ContarSi(clave,numero) + '\n')
                textoSalida.configure(state='disabled')

                clave = ''
                numero = 0
                boolcontarsi = False

            #Reporte html

            elif i.getLexema().lower()=='exportarreporte':
                boolreporte = True
            
            elif i.getTipo() == 'CADENA' and boolreporte:
                nombre = i.getLexema()
                analizador.exportarReporte(nombre) 
                nombre = ''
                boolreporte = False
        

    else:
        textoSalida.configure(state='normal')
        textoSalida.insert(END, "ERROR DE SINTAXIS O LEXICO :(")
        textoSalida.configure(state='disabled')
        analizador.imprimirErroresSintacticos()



    
    
    analizador.limpiarDatos()
    
    
   

            

   

#---------------------------------INTERFAZ GRÁFICA ------------------------------

#Root
ventana = Tk()
ventana.config(background="#044D9A")

ventana.geometry("1200x900")
ventana.title("Editor de base de datos")

#Ventana de edicion y lectura de texto
textoEntrada = Text(ventana, height=40, width=70, bg="#313131", fg="white", font=("Consolas", 11)) 
textoEntrada.place(x=10, y=100)


textoSalida = Text(ventana, height=40, width=70, bg="#313131",state='disabled', fg="white", font=("Consolas", 11))
textoSalida.place(x=600, y=100)







#Botones
btnAbrirArchivo = Button(ventana, height=2, width=10, text="Abrir archivo", command = abrirArchvo1, background="#368807", font=("Verdana",10), fg="white")
btnAbrirArchivo.place(x=320, y=50)

btnAnalizar = Button(ventana, height=2, width=10, text="Compilar", command=Compilar, background="#10139E", font=("Verdana",10), fg="white")
btnAnalizar.place(x=420, y=50)

btnReporeteTokensValidos = Button(ventana, height=2, width=12, text="Tokens válidos",command=reporteTokens, background="#8E8C08", font=("Verdana",10), fg="white")
btnReporeteTokensValidos.place(x=515, y=50)

btnReporeteTokensInvalidos = Button(ventana, height=2, width=13, text="Errores",command=reporteErrores, background="#B03314", font=("Verdana",10), fg="white")
btnReporeteTokensInvalidos.place(x=630, y=50)

btnReporeteGrpahviz = Button(ventana, height=2, width=10, text="Graphviz" , command=analizador.generarArbol, background="#0D9597", font=("Verdana",10), fg="white")
btnReporeteGrpahviz.place(x=750, y=50)

#Labels
labelEditor = Label (ventana, text ="EDITOR DE TEXTO", font=("Verdana",15), background="#044D9A", fg="white")
labelEditor.place(x=90, y=50)

labelTerminal = Label (ventana, text ="TERMINAL", font=("Verdana",15), background="#044D9A", fg="white")
labelTerminal.place(x=900, y=50)

ventana.mainloop()
