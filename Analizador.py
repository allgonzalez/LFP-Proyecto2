from tkinter.font import families
from Tokens import Token
from Registros import Registros
from Error_Sintactico import ErrorSintactico
import webbrowser
from os import system, startfile


class Analizador:
    #Variable que guardará lo que vaya recorriendo poco a poco
    lexema = ''
    #Arreglo de tokens
    tokens = []
    #Arrreglo de Claves
    claves = []
    #Arreglo de registros
    registros = []
    #Arreglos de errores sintácticos
    erroresSintacticos = []
    #EStados para ir distribuyendo los distintos símbolos encontrados
    estado = 1
    #Fila en la que estoy
    fila = 1
    #Columna en la que estoy 
    columna = 1
    #Ayuda a ver si generamos un reporte de errores por si hay símbolos que son desconocidos
    generarErrores = False

    tildes = ['á','é','í','ó','ú']
    

 #----------------------------------------------Analizador lexico----------------------------------------------   

    def scanner(self, entrada):
        #Manejo de tipos
        global tipos
        tipos = Token("random", 0, 0,0) #Llenamos de datos random para importar las variables
        
        self.estado = 1
        self.lexema = ''
        self.tokens = []
        self.fila = 1
        self.columna = 1
        self.generarErrores = False
        
        #Variables de apoyo temporales
        temp = ''
        habilitar_comentario = False
        
        habilitar_cadena = True

        entrada = entrada + '$'
        actual = ''
        longitud = len(entrada)

        for i in range(longitud):
            actual = entrada[i]

            if self.estado == 1:
                if actual.isalpha(): #Se verifica si es alfabetico [a-zA-Z]
                    self.estado = 2  #Agregamos los estados para ir concatenando
                    self.columna += 1
                    self.lexema += actual
                    continue

                elif actual.isdigit(): #VErificamos si es dígito [0-9]
                    self.estado = 3
                    self.columna += 1
                    self.lexema += actual
                    
                
                elif actual == '"':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.COMILLAS_DOBLE)
                    self.estado = 4 
                    continue

                elif actual == "'":
                    self.estado = 7
                    self.columna +=1
                    self.lexema += actual
                    

                elif actual == '=':  
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.IGUAL) #Como el igual no es signo que se combine con otros mas se agrega a la lista de tokens
                
                elif actual == '{':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.LLAVE_I)
                elif actual == '}':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.LLAVE_D)
                
                elif actual == '[':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.CORCHETE_I)
                elif actual == ']':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.CORCHETE_D)
                
                elif actual == ',':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.COMA)
                
                elif actual == '(':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.PARENTESIS_D)
                
                elif actual == ')':
                    self.columna +=1
                    self.lexema += actual
                    self.agregarToken(tipos.PARENTESIS_D)
                
                elif actual == ';':
                    self.columna += 1
                    self.lexema += actual
                    self.agregarToken(tipos.PUNTO_COMA)
            
                elif actual == '#':
                    self.estado = 5
                    self.columna += 1
                    self.lexema += actual
        
                elif actual == ' ':
                    self.columna += 1
                    self.estado = 1
                
                elif actual == '\n':
                    self.fila += 1
                    self.columna = 1
                    self.estado = 1
                
                elif actual == '\r':
                    self.estado = 1
                
                elif actual == '\t':
                    self.columna += 5
                    self.estado = 1
                

                elif actual == '$' and i == longitud-1:
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.FIN_DOCUMENTO)
                    print('Análisis finalizado con éxito :) ')
                
                else:
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.DESCONOCIDO)
                    self.generarErrores = True

            #Estado para palabras reservadas    
            elif self.estado == 2:
                if actual.isalpha():
                    self.estado = 2
                    self.columna += 1
                    self.lexema += actual
                    continue
                elif actual.isdigit():
                    self.agregarToken(tipos.DESCONOCIDO)
                    self.generarErrores = True
                    
                else:
                    if self.palabra_reservada(self.lexema):
                        self.agregarToken(tipos.PALABRA_RESERVADA)
                        if actual == ";":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.PUNTO_COMA)
                        elif actual == ",":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.COMA)
                        elif actual == "=":
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.IGUAL)
                        elif actual == ' ':
                            self.columna +=1
                        elif actual == '(':
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.PARENTESIS_I)
                        elif actual == ')':
                            self.lexema = actual
                            self.columna += 1
                            self.agregarToken(tipos.PARENTESIS_D)
                        
                        elif actual == '$':
                            self.lexema = actual 
                            self.columna += 1
                            self.agregarToken(tipos.FIN_DOCUMENTO)
                        
                        elif actual == '"':
                            self.lexema = actual 
                            self.columna += 1
                            self.agregarToken(tipos.COMILLAS_DOBLE)

                    else:
                        self.lexema += actual
                        self.columna += 1
                        self.agregarToken(tipos.DESCONOCIDO)
                        self.generarErrores = True

            
            #Estado para los numeros
            elif self.estado == 3:
                if actual.isdigit() or actual == '.':
                    self.estado = 3
                    self.columna +=1
                    self.lexema += actual
                else:
                    self.agregarToken(tipos.NUMERO)
                    self.lexema = actual
                    self.columna += 1
                    if actual == ";":
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.PUNTO_COMA)
                    elif actual == ",":
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.COMA)
                    elif actual == "=":
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.IGUAL)
                    elif actual == ' ':
                        self.columna +=1
                    elif actual == ")":
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.PARENTESIS_D)
                    elif actual == '}':
                        self.agregarToken(tipos.LLAVE_D)
                    elif actual == ' ':
                        self.columna += 1
                    elif actual == '\n':
                        self.fila +=1
                        self.columna = 0
                    elif actual == '$':
                        self.lexema = actual
                        self.columna += 1
                        self.agregarToken(tipos.FIN_DOCUMENTO)

            #Estado para las cadenas temporales
            elif self.estado == 4:
                if actual.isalpha() and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                if actual.isdigit() and habilitar_cadena:
                    self.esatado = 4
                    self.columna += 1
                    self.lexema += actual

                elif actual =='_' and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                
                
                elif actual == '*' and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                
                elif actual == '/' and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
                
                elif actual == "\\" and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual

                
                elif actual == ' ' and habilitar_cadena:
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual

                elif actual == '"':
                    temporal = actual
                    self.agregarToken(tipos.CADENA)
                    self.lexema = temporal
                    self.columna += 1
                    self.agregarToken(tipos.COMILLAS_DOBLE)
                      

            #Estado para los comentarios de una linea
            elif self.estado ==5:
                if actual!= '#':
                    if actual == ' ':
                        self.columna +=1
                        self.estado = 5
                        self.lexema += actual
                    elif actual == '\t':
                        self.columna +=5
                        self.estado = 5
                        self.lexema += actual
                    elif actual.isalpha():
                        self.columna +=1
                        self.lexema += actual
                        self.estado = 5
                    elif actual.isdigit():
                        self.columna += 1
                        self.lexema += actual
                        self.estado = 5
                    elif actual == '\n':
                        self.agregarToken(tipos.COMENTARIO_UNA_LINEA)
                        self.columna = 1
                        self.fila += 1
                    elif actual == '$':
                        self.agregarToken(tipos.COMENTARIO_UNA_LINEA)
                    
            
            #Estado para comentarios de multilinea
            elif self.estado == 6:
                
                if actual == "'" :
                    temp += actual
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                    if temp == "'''":
                        self.agregarToken(tipos.COMENTARIO_MULTILINEA)
                        temp = ''


                elif actual == '\n' :
                    self.columna = 1
                    self.fila += 1
                    self.columna = 1
                    self.lexema += actual
                    
                
                elif actual.isalpha() :
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                elif actual.isdigit() :
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                
                elif actual == ' ':
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6


            elif self.estado == 7:
                if actual == "'":
                    self.lexema += actual
                    self.columna += 1
                    self.estado = 7
                    if self.lexema == "'''":
                        self.estado = 6                 

                    
                


    #Funcion para ir agregando nuestros tokens
    def agregarToken(self,tipo):
        self.tokens.append(Token(self.lexema, tipo, self.fila, self.columna))
        self.lexema = ""
        self.estado = 1


    
    #Funcion para verificar si tenemos palabras reservadas
    def palabra_reservada(self, entrada = ''):
        entrada = entrada.lower()
        reservada = False
        reservadas = ['claves','registros', 'imprimir', 'imprimirln', 'conteo', 'promedio', 'contarsi', 'datos', 'sumar', 'max','min','exportarreporte']

        if entrada in reservadas:
            reservada = True
        return reservada
    
    def imprimirTokens(self):
        for i in self.tokens:
            if i.tipo != tipos.DESCONOCIDO:
                print('Lexema: ',i.getLexema(), " | Fila: ", i.getFila(), ' | Columna: ', i.getColumna(), ' | Tipo: ',i.getTipo() )
            
            else:
                 print('Lexema: ',i.getLexema(), " | Fila: ", i.getFila(), ' | Columna: ', i.getColumna(), ' | Tipo: ',i.getTipo() )
    
    def imprimirErrores(self):
        for j in self.tokens:
            if j.tipo == tipos.DESCONOCIDO:
                print('Lexema: ',j.getLexema(), " | Fila: ", j.getFila(), ' | Columna: ', j.getColumna(), ' | Tipo: ',j.getTipo() )




#--------------------------------------------------------------Analizador sintáctico------------------------------------------------------

    def Claves(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolclave = False

        if self.generarErrores == False:
            while cont != contadorTemp:
                if self.tokens[cont].getLexema().lower() == "claves":
                    if self.tokens[cont+1].tipo == tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_IGUAL, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.generarErrores = True
                
                    elif self.tokens[cont+1].tipo == tipos.IGUAL and self.tokens[cont+2].tipo != tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+2))
                        self.generarErrores = True

                    elif self.tokens[cont+1].tipo != tipos.IGUAL and self.tokens[cont+2].tipo != tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_IGUAL, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+1))
                        self.generarErrores = True

                    else:
                     Boolclave = True

                elif self.tokens[cont].tipo == tipos.CADENA and Boolclave:
                   
                    if self.tokens[cont-2].tipo == tipos.COMA:  
                        self.claves.append(self.tokens[cont].getLexema())
                    
                    elif self.tokens[cont-2].tipo == tipos.CORCHETE_I:
                        self.claves.append(self.tokens[cont].getLexema())
                    
                    elif self.tokens[cont-3].tipo == tipos.PALABRA_RESERVADA:
                        cont = contadorTemp - 1

                    else :
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_COMA, self.tokens[cont-2].getFila(), self.tokens[cont-2].getColumna()))
                        self.generarErrores= True
                    

                elif self.tokens[cont].getLexema().lower() == 'registros':
                    if self.tokens[cont-1].tipo != tipos.CORCHETE_D:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_D, self.tokens[cont-1].getFila(), self.tokens[cont-1].getColumna()))
                    Boolclave = False
                    cont = contadorTemp-1
                cont+=1
        
        else:
            print("Hay errores de lexema o sintáctico")



        if self.generarErrores == False:
            for j in self.claves:
                print("claves: ", j)
            
            
            

    def Registros(self):
        Boolregistros = False
        cont = 0
        contClave = 0
        contadorTemp = len(self.tokens)-1
        tiposError = ErrorSintactico(0,0, 0)

        if self.generarErrores== False:
            while cont != contadorTemp:
            
                if self.tokens[cont].getLexema().lower() == 'registros':
                    if self.tokens[cont+1].tipo == tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_IGUAL, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.generarErrores = True
                
                    elif self.tokens[cont+1].tipo == tipos.IGUAL and self.tokens[cont+2].tipo != tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+2))
                        self.generarErrores = True

                    elif self.tokens[cont+1].tipo != tipos.IGUAL and self.tokens[cont+2].tipo != tipos.CORCHETE_I:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_IGUAL, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+1))
                        self.generarErrores = True

                    else:
                        Boolregistros = True
            
                elif self.tokens[cont].tipo == tipos.NUMERO or self.tokens[cont].tipo == tipos.CADENA:
                    if Boolregistros:
                        if self.tokens[cont-1].tipo == tipos.LLAVE_I or self.tokens[cont-2].tipo == tipos.COMA or self.tokens[cont-1].tipo == tipos.COMA:
                            self.registros.append(Registros(self.claves[contClave], self.tokens[cont].getLexema()))
                            contClave += 1
                    
                        elif self.tokens[cont].tipo == tipos.NUMERO:
                            if self.tokens[cont-1].tipo != tipos.CORCHETE_D:
                                self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_LLAVE_I, self.tokens[cont-1].getFila()+1, 1))
                                self.generarErrores = True
                        
                            elif self.tokens[cont-1].tipo != tipos.COMA:
                                self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_COMA, self.tokens[cont-1].getFila(), self.tokens[cont-1].getColumna()))
                                self.generarErrores = True

                        elif self.tokens[cont].tipo == tipos.CADENA:
                            if self.tokens[cont-2].tipo != tipos.COMA:
                                self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_COMA, self.tokens[cont-2].getFila(), self.tokens[cont-2].getColumna()))
                                self.generarErrores = True
                    
                elif self.tokens[cont].tipo == tipos.LLAVE_D and Boolregistros:
                    if self.tokens[cont+1].tipo == tipos.LLAVE_I: 
                        contClave = 0
                    elif self.tokens[cont+1].tipo == tipos.CORCHETE_D:
                        Boolregistros = False
                        cont = contadorTemp-1
                    else:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_CORCHETE_D, self.tokens[cont].getFila()+1, 1))
                        self.generarErrores = True
                        Boolregistros = False
                        cont = contadorTemp-1
                        
                cont += 1
        else:
            print("Hay errores de lexema o sintáctico")


        if self.generarErrores == False:
            for i in self.registros:
                    print("Clave: ", i.getClave(), " Registro: ", i.getRegistro())
            


    def SintacticoImprimirReporte(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolimprimir = False
        

        while cont != contadorTemp:
            if self.tokens[cont].getLexema().lower() == 'imprimir' or self.tokens[cont].getLexema().lower() == 'imprimirln'or self.tokens[cont].getLexema().lower() == 'exportarreporte' :
                if self.tokens[cont+1].tipo != tipos.PARENTESIS_I:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                    
                else:
                    Boolimprimir = True
                    

            elif self.tokens[cont].tipo == tipos.CADENA and Boolimprimir :
                if self.tokens[cont+2].tipo != tipos.PARENTESIS_D:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                
            
            elif self.tokens[cont].tipo == tipos.PARENTESIS_D and Boolimprimir:

                if self.tokens[cont+1].tipo != tipos.PUNTO_COMA:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                    Boolimprimir = False
                else: 
                    Boolimprimir = False

            cont+= 1


    def sintacticoConteoDatos(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolconteo = False

        while cont != contadorTemp :
            if self.tokens[cont].getLexema().lower() == 'conteo' or self.tokens[cont].getLexema().lower() == 'datos':
                if self.tokens[cont+1].tipo == tipos.PARENTESIS_D: 
                    if  self.tokens[cont+2].tipo == tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.generarErrores = True

                    
                    else:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()))
                        self.generarErrores = True
    

                elif self.tokens[cont+1].tipo == tipos.PARENTESIS_I:
                    if self.tokens[cont+2].tipo == tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()))
                        self.generarErrores = True

                    elif self.tokens[cont+2].tipo != tipos.PARENTESIS_D and self.tokens[cont+3].tipo != tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()+1))
                        self.generarErrores = True
                    
                    elif self.tokens[cont+2].tipo == tipos.PARENTESIS_D and self.tokens[cont+3].tipo != tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+2].getFila(), self.tokens[cont+1].getColumna()+1))
                        self.generarErrores = True
                    

                elif self.tokens[cont+1].tipo == tipos.PUNTO_COMA:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+1))
                    self.generarErrores = True
                
                #
                elif self.tokens[cont+1].tipo != tipos.PARENTESIS_I and self.tokens[cont+1].tipo != tipos.PARENTESIS_D and self.tokens[cont+1].tipo != tipos.PUNTO_COMA:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+1))
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+2))
                    self.generarErrores = True

                elif self.tokens[cont+1].tipo == tipos.FIN_DOCUMENTO:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+1))
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+2))
                    self.generarErrores = True

            cont+= 1

    def sintacticoPromMaxMinSum(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolimprimir = False
        

        while cont != contadorTemp:
            if self.tokens[cont].getLexema().lower() == 'promedio' or self.tokens[cont].getLexema().lower() == 'sumar' or self.tokens[cont].getLexema().lower() == 'max' or self.tokens[cont].getLexema().lower() == 'min':
                if self.tokens[cont+1].tipo != tipos.PARENTESIS_I:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                    
                else:
                    Boolimprimir = True
                    

            elif self.tokens[cont].tipo == tipos.CADENA and Boolimprimir :
                if self.tokens[cont+2].tipo != tipos.PARENTESIS_D:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                
            
            elif self.tokens[cont].tipo == tipos.PARENTESIS_D and Boolimprimir:

                if self.tokens[cont+1].tipo != tipos.PUNTO_COMA:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                    Boolimprimir = False
                else: 
                    Boolimprimir = False

            cont+= 1

    def sintacticoContarSi(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolconteo = False

        while cont != contadorTemp :
            if self.tokens[cont].getLexema().lower() == 'contarsi':

                if self.tokens[cont+1].tipo == tipos.COMILLAS_DOBLE:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_I, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
    

                elif self.tokens[cont+1].tipo == tipos.PARENTESIS_I:

                    if  self.tokens[cont+5].tipo == tipos.NUMERO:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()+4))
                        self.generarErrores = True

                    elif self.tokens[cont+6].tipo == tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()))
                        self.generarErrores = True

                    elif self.tokens[cont+7].tipo != tipos.PARENTESIS_D and self.tokens[cont+8].tipo != tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+1].getFila(), self.tokens[cont+1].getColumna()+1))
                        self.generarErrores = True
                    
                    elif self.tokens[cont+6].tipo == tipos.PARENTESIS_D and self.tokens[cont+7].tipo != tipos.PUNTO_COMA:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+2].getFila(), self.tokens[cont+1].getColumna()+1))
                        self.generarErrores = True

                    elif self.tokens[cont+6].tipo == tipos.FIN_DOCUMENTO:
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PARENTESIS_D, self.tokens[cont+6].getFila(), self.tokens[cont+6].getColumna()+1))
                        self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont+6].getFila(), self.tokens[cont+6].getColumna()+2))
                        self.generarErrores = True
   

                

            cont+= 1

#------------------------------------------FUNCIONES------------------------------------------

    def Promedio(self,clave):
        suma = 0
        total = 0
        promedio = 0
        for i in self.registros:
            if i.getClave() == clave:
                suma += float(i.getRegistro())
                total += 1
        
        promedio = suma / total
        
        return str(promedio)
    
    def Sumar(self,clave):
        suma = 0
        for i in self.registros:
            if i.getClave() == clave:
                suma += float(i.getRegistro())
        
        return str(suma)
        
    
    def Maximo(self,clave):
        temp = []
        for i in self.registros:
            if i.getClave() == clave:
                temp.append(i.getRegistro())
        
        maxNum = max(temp, key= float)

        return str(maxNum)
    
    def Minimo(self,clave):
        temp = []
        for i in self.registros:
            if i.getClave() == clave:
                temp.append(i.getRegistro())
        
        minNum = min(temp, key= float)

        return str(minNum)
    
    def ContarSi(self,clave,valor):
        suma = 0
        for i in self.registros:
            if i.getClave() == clave and i.getRegistro() == valor:
                suma +=1

        return str(suma)


#-------------------------------------REPORETES----------------------------------------
    def exportarReporte(self, nombre):
        docHTML = open(nombre+'.html', 'w')
        docHTML.write('\n<!DOCTYPE html>')
        docHTML.write('\n<html lang="es">')
        docHTML.write('\n<meta charset="utf-8">')
        docHTML.write('\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
        docHTML.write('\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
        docHTML.write('\n<title>Reporte de Tokens</title>')
        docHTML.write('\n</head>')
        docHTML.write('\n<body>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n <h4 class= "text-center"> '+nombre+' </h4>')
        docHTML.write('\n<div>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n<table class="table" border="1">')    
        docHTML.write('\n\t <thead class="thead-dark">')
        docHTML.write('\n\t\t <tr>')
        
        for i in self.claves:
            docHTML.write('\n\t\t\t<th scope = "col">'+i+'</th>')

        docHTML.write('\n\t\t </tr>')
        docHTML.write('\n\t </thead>')
        docHTML.write('\n\t <tbody>')

        cont = 0
        
        rango = int(len(self.registros) / len(self.claves))


        for j in range(rango):
            docHTML.write('\n\t\t </tr>')
            for k in range(len(self.claves)):
                docHTML.write('\n\t\t\t<td>'+str(self.registros[cont].getRegistro()))
                docHTML.write('</td>')
                cont+=1
            docHTML.write('\n\t\t </tr>')
            

        docHTML.write('\n\t </tbody>')
        docHTML.write('\n</table>')
        docHTML.write('\n</div>')  
        docHTML.write('\n</body')
        docHTML.write('\n</html>')
        
        docHTML.close()


    def reporteTokensValidos(self):
        docHTML = open('reporteTokensValidos.html', 'w')
        docHTML.write('\n<!DOCTYPE html>')
        docHTML.write('\n<html lang="es">')
        docHTML.write('\n<meta charset="utf-8">')
        docHTML.write('\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
        docHTML.write('\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
        docHTML.write('\n<title>Reporte de Tokens</title>')
        docHTML.write('\n</head>')
        docHTML.write('\n<body>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n <h4 class= "text-center"> Lista de Tokens Validos </h4>')
        docHTML.write('\n<div>')
        docHTML.write('\n<div class="container">')
        docHTML.write('\n<table class="table" border="1">')    
        docHTML.write('\n\t <thead class="thead-dark">')
        docHTML.write('\n\t\t <tr>')
        docHTML.write('\n\t\t\t<th scope = "col">Token</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Lexema</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Fila</th>')
        docHTML.write('\n\t\t\t<th scope = "col">Columna</th>')
        docHTML.write('\n\t\t </tr>')
        docHTML.write('\n\t </thead>')
        docHTML.write('\n\t <tbody>')
        
        for i in self.tokens:
            if i.tipo != tipos.DESCONOCIDO:
                docHTML.write('\n\t\t <tr class="table-success">')
                docHTML.write('\n\t\t\t<th scope = "row">'+str(i.getTipo()))
                docHTML.write('</th>')
                docHTML.write('\n\t\t\t<td>'+str(i.getLexema()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t\t<td>'+ str(i.getFila()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t\t<td>'+ str(i.getColumna()))
                docHTML.write('</td>')
                docHTML.write('\n\t\t </tr>')

        docHTML.write('\n\t </tbody>')
        docHTML.write('\n</table>')
        docHTML.write('\n</div>')  
        docHTML.write('\n</body')
        docHTML.write('\n</html>')
        
        docHTML.close()

        webbrowser.open_new_tab('reporteTokensValidos.html')
    
    def reportesErrores(self):
            docHTML = open('reporteErrores.html', 'w')
            docHTML.write('\n<!DOCTYPE html>')
            docHTML.write('\n<html lang="es">')
            docHTML.write('\n<meta charset="utf-8">')
            docHTML.write('\n<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
            docHTML.write('\n<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">')
            docHTML.write('\n<title>Reporte de Tokens</title>')
            docHTML.write('\n</head>')
            docHTML.write('\n<body>')
            docHTML.write('\n<div class="container">')
            docHTML.write('\n <h4 class= "text-center"> Lista de Tokens con Errores </h4>')
            docHTML.write('\n<div>')
            docHTML.write('\n<div class="container">')
            docHTML.write('\n<table class="table" border="1">')    
            docHTML.write('\n\t <thead class="thead-dark">')
            docHTML.write('\n\t\t <tr>')
            docHTML.write('\n\t\t\t<th scope = "col">Token</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Lexema</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Fila</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Columna</th>')
            docHTML.write('\n\t\t </tr>')
            docHTML.write('\n\t </thead>')
            docHTML.write('\n\t <tbody>')
        
            for i in self.tokens:
                if i.tipo == tipos.DESCONOCIDO:
                    docHTML.write('\n\t\t <tr class="table-danger">')
                    docHTML.write('\n\t\t\t<th scope = "row">'+'DESCONOCIDO')
                    docHTML.write('</th>')
                    docHTML.write('\n\t\t\t<td>'+str(i.getLexema()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(i.getFila()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(i.getColumna()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t </tr>')

            docHTML.write('\n\t </tbody>')
            docHTML.write('\n</table>')
            docHTML.write('\n</div>') 

            docHTML.write('\n<div class="container">')
            docHTML.write('\n <h4 class= "text-center"> Lista Errores Sintacticos</h4>')
            docHTML.write('\n<div>')
            docHTML.write('\n<div class="container">')
            docHTML.write('\n<table class="table" border="1">')    
            docHTML.write('\n\t <thead class="thead-dark">')
            docHTML.write('\n\t\t <tr>')
            docHTML.write('\n\t\t\t<th scope = "col">Error</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Fila</th>')
            docHTML.write('\n\t\t\t<th scope = "col">Columna</th>')
            docHTML.write('\n\t\t </tr>')
            docHTML.write('\n\t </thead>')
            docHTML.write('\n\t <tbody>')
        
            for j in self.erroresSintacticos:
    
                    docHTML.write('\n\t\t <tr class="table-danger">')
                    docHTML.write('\n\t\t\t<td>'+str(j.getError()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(j.getFila()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t\t<td>'+ str(j.getColumna()))
                    docHTML.write('</td>')
                    docHTML.write('\n\t\t </tr>')

            docHTML.write('\n\t </tbody>')
            docHTML.write('\n</table>')
            docHTML.write('\n</div>')  


            docHTML.write('\n</body')
            docHTML.write('\n</html>')


        
            docHTML.close()

            webbrowser.open_new_tab('reporteErrores.html')
    

    def imprimirErroresSintacticos(self):
        for i in self.erroresSintacticos:
            print("Error: ", i.getError(), " Fila: ", i.getFila(), " Columna: ", i.getColumna())



            

    def limpiarDatos(self):
        self.claves.clear()
        self.registros.clear()
        
    
    def generarArbol(self):

        boolClaves = False
        boolRegistros = False
        boolImprimir = False
        boolImprimirln = False
        boolConteo = False
        boolPromedio = False
        boolContarsi = False
        boolDatos = False
        boolSumar = False
        boolMax = False
        boolMin = False
        boolReporte = False

        n = 0
        
        arbol = '''
        digraph L{
            
            NodoInicio[label="INICIO"];
            NodoInstruccion[label="INSTRUCCIONES"];
            NodoClave[label="CLAVES"];
            NodoRegistro[label="REGISTROS"];
            
            

            NodoInicio -> NodoInstruccion;
            NodoInicio -> NodoClave;
            NodoInicio -> NodoRegistro;\n
        '''
        for i in self.tokens:
            #Empezamos con las claves
            if i.getLexema().lower() == 'claves':
                arbol+='NodoClave1[label="tk_claves"];\n'
                arbol+='NodoClave->NodoClave1;\n'
                boolClaves = True
                n += 1
            elif i.tipo == tipos.CORCHETE_I and boolClaves:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoClave1->Nodo'+str(n)+';\n'
                n+=1
            
            elif i.tipo == tipos.CADENA and boolClaves:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoClave1->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.COMA and boolClaves:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoClave1->Nodo'+str(n)+';\n'
                n+=1

            elif i.tipo == tipos.CORCHETE_D and boolClaves:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoClave1->Nodo'+str(n)+';\n'
                n+=1
                boolClaves = False


            #Continuamos con los registros
            elif i.getLexema().lower() == 'registros':
                arbol+='NodoRegistro1[label="tk_registros"];\n'
                arbol+='NodoRegistro->NodoRegistro1;\n'
                boolRegistros = True
                n += 1

            elif i.tipo == tipos.CORCHETE_I and boolRegistros:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->Nodo'+str(n)+';\n'
                n+=1

            elif i.tipo == tipos.LLAVE_I and boolRegistros:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->Nodo'+str(n)+';\n'
                n+=1

            elif i.tipo == tipos.CADENA and boolRegistros:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            
            elif i.tipo == tipos.NUMERO and boolRegistros:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_numero"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1

            elif i.tipo == tipos.COMA and boolRegistros:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->Nodo'+str(n)+';\n'
                n+=1
            
            elif i.tipo == tipos.LLAVE_D and boolRegistros:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->Nodo'+str(n)+';\n'
                n+=1

            elif i.tipo == tipos.CORCHETE_D and boolRegistros:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoRegistro1->Nodo'+str(n)+';\n'
                n+=1
                boolRegistros = False

            #Instrucciones -> imprimir
            elif i.getLexema().lower() == 'imprimir':
                arbol+='NodoInstruccion1[label="tk_imprimir"];\n'
                arbol+='NodoInstruccion->NodoInstruccion1;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion1->'+'Nodo'+str(n)+';\n'
                boolImprimir = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolImprimir:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion1->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolImprimir:
                if i.getLexema().find('\\') >= 0:
                    arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                    arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'\ "];\n'
                    arbol += 'NodoInstruccion1->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                    n+=1
                else:
                    arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                    arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'\ "];\n'
                    arbol += 'NodoInstruccion1->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                    n+=1


                
            elif i.tipo == tipos.PARENTESIS_D and boolImprimir:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion1->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolImprimir:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion1->Nodo'+str(n)+';\n'
                n+=1
                boolImprimir = False

            
            #Instrucciones -> imprimirln
            elif i.getLexema().lower() == 'imprimirln':
                arbol+='NodoInstruccion2[label="tk_imprimirln"];\n'
                arbol+='NodoInstruccion->NodoInstruccion2;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion2->'+'Nodo'+str(n)+';\n'
                boolImprimirln = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolImprimirln:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion2->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolImprimirln:
                if i.getLexema().find('\\') >= 0:
                    arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                    arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'\ "];\n'
                    arbol += 'NodoInstruccion2->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                    n+=1
                else:
                    arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                    arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'\ "];\n'
                    arbol += 'NodoInstruccion2->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                    n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolImprimirln:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion2->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolImprimirln:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion2->Nodo'+str(n)+';\n'
                n+=1
                boolImprimirln = False


            #Instrucciones -> conteo
            elif i.getLexema().lower() == 'conteo':
                arbol+='NodoInstruccion3[label="tk_conteo"];\n'
                arbol+='NodoInstruccion->NodoInstruccion3;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion3->'+'Nodo'+str(n)+';\n'
                boolConteo = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolConteo:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion3->Nodo'+str(n)+';\n'
                n+=1
    
            elif i.tipo == tipos.PARENTESIS_D and boolConteo:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion3->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolConteo:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion3->Nodo'+str(n)+';\n'
                n+=1
                boolConteo = False
            
            #Instruciones -> Promedio

            #Instrucciones -> imprimirln
            elif i.getLexema().lower() == 'promedio':
                arbol+='NodoInstruccion4[label="tk_promedio"];\n'
                arbol+='NodoInstruccion->NodoInstruccion4;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion4->'+'Nodo'+str(n)+';\n'
                boolPromedio = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolPromedio:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion4->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolPromedio:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion4->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolPromedio:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion4->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolPromedio:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion4->Nodo'+str(n)+';\n'
                n+=1
                boolPromedio = False

            #Instrucciones -> contarsi
            elif i.getLexema().lower() == 'contarsi':
                arbol+='NodoInstruccion5[label="tk_contarsi"];\n'
                arbol+='NodoInstruccion->NodoInstruccion5;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion5->'+'Nodo'+str(n)+';\n'
                boolContarsi = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolContarsi:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolContarsi:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.COMA and boolContarsi:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.NUMERO and boolContarsi:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_numero"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1    
            elif i.tipo == tipos.PARENTESIS_D and boolContarsi:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolContarsi:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion5->Nodo'+str(n)+';\n'
                n+=1
                boolContarsi = False
            
            #Instrucciones -> datos
            elif i.getLexema().lower() == 'datos':
                arbol+='NodoInstruccion6[label="tk_datos"];\n'
                arbol+='NodoInstruccion->NodoInstruccion6;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion6->'+'Nodo'+str(n)+';\n'
                boolDatos = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolDatos:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion6->Nodo'+str(n)+';\n'
                n+=1
    
            elif i.tipo == tipos.PARENTESIS_D and boolDatos:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion6->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolDatos:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion6->Nodo'+str(n)+';\n'
                n+=1
                boolDatos= False

            #Instrucciones -> Sumar
            elif i.getLexema().lower() == 'sumar':
                arbol+='NodoInstruccion7[label="tk_sumar"];\n'
                arbol+='NodoInstruccion->NodoInstruccion7;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion7->'+'Nodo'+str(n)+';\n'
                boolSumar = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolSumar:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion7->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolSumar:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion7->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolSumar:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion7->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolSumar:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion7->Nodo'+str(n)+';\n'
                n+=1
                boolSumar = False

            #Instrucciones -> Max
            elif i.getLexema().lower() == 'max':
                arbol+='NodoInstruccion8[label="tk_max"];\n'
                arbol+='NodoInstruccion->NodoInstruccion8;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion8->'+'Nodo'+str(n)+';\n'
                boolMax = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolMax:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion8->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolMax:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion8->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolMax:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion8->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolMax:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion8->Nodo'+str(n)+';\n'
                n+=1
                boolMax = False
            
            #Instrucciones -> Min
            elif i.getLexema().lower() == 'min':
                arbol+='NodoInstruccion9[label="tk_min"];\n'
                arbol+='NodoInstruccion->NodoInstruccion9;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion9->'+'Nodo'+str(n)+';\n'
                boolMin = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolMin:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion9->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolMin:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion9->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolMin:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion9->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolMin:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion9->Nodo'+str(n)+';\n'
                n+=1
                boolMin = False
            
            #Instrucciones -> ExportarReporte
            elif i.getLexema().lower() == 'exportarreporte':
                arbol+='NodoInstruccion10[label="tk_exportarReporte"];\n'
                arbol+='NodoInstruccion->NodoInstruccion10;\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol+='NodoInstruccion10->'+'Nodo'+str(n)+';\n'
                boolReporte = True
                n += 1
            
            elif i.tipo == tipos.PARENTESIS_I and boolReporte:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion10->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.CADENA and boolReporte:
                arbol+='NodoExpresion'+str(n+1)+'[label="tk_cadena"];\n'
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion10->NodoExpresion'+str(n+1)+'->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PARENTESIS_D and boolReporte:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion10->Nodo'+str(n)+';\n'
                n+=1
            elif i.tipo == tipos.PUNTO_COMA and boolReporte:
                arbol +='Nodo'+str(n)+'[label="'+i.getLexema()+'"];\n'
                arbol += 'NodoInstruccion10->Nodo'+str(n)+';\n'
                n+=1
                boolReporte = False

        arbol += '\n }'

        miArchivo = open('graphviz.dot', 'w')
        miArchivo.write(arbol)
        miArchivo.close()
    
        system('dot -Tpng graphviz.dot -o arbol_de_derivacion.png')


        startfile('arbol_de_derivacion.png')
        
