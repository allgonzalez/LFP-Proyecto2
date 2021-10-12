from tkinter import filedialog
from Analizador import Analizador




def abrirArchivo():
    archivo = filedialog.askopenfilename(title="Abrir", filetypes=[("pixeles", "*.lfp")])
    archivos_texto = open(archivo, 'r')
    texto = archivos_texto.read()
    return texto

print('--------------------Analizador Léxico------------------------')
entrada = ''
opcion = 0
lexico = Analizador()


while opcion != 4:
    print('1. Ingresar archivo')
    print('2. Procesar archivo')
    print('3. Imprimir Tokens Validos')
    print('4. Salir')
    
    opcion = int(input('>Ingrese una opción: '))

    if opcion == 1:
        
        archivo = abrirArchivo()
        
    elif opcion == 2:
        lexico.scanner(archivo)
    
    elif opcion == 3:
        lexico.imprimirTokens()
        print("---Prueba--")
        lexico.Claves()
        print('')
        lexico.Registros()
        lexico.SintacticoImprimir()
    elif opcion ==4:
         break
    