from tkinter.font import families
from Imprimir import imprimir
from Tokens import Token
from Registros import Registros
from Error_Sintactico import ErrorSintactico

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
                    else:
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
                    
                    elif actual == '}':
                        self.agregarToken(tipos.LLAVE_D)
                    elif actual == ' ':
                        self.columna += 1
                    elif actual == '\n':
                        self.fila +=1
                        self.columna = 0

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
            


    def SintacticoImprimir(self):
        tiposError = ErrorSintactico(0,0, 0)
        contadorTemp = len(self.tokens)-1
        cont = 0
        Boolimprimir = False
        

        while cont != contadorTemp:
            if self.tokens[cont].getLexema().lower() == 'imprimir' or self.tokens[cont].getLexema().lower() == 'imprimirln':
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

                if self.tokens[cont+1].tipo != tipos.PUNTO_COMA or self.tokens[cont+1] == None:
                    self.erroresSintacticos.append(ErrorSintactico(tiposError.FALTO_PUNTO_COMA, self.tokens[cont].getFila(), self.tokens[cont].getColumna()))
                    self.generarErrores = True
                    Boolimprimir = False
                else: 
                    Boolimprimir = False

            cont+= 1


    def imprimirErrores(self):
        if self.generarErrores:
            for i in self.erroresSintacticos:
                print("Error: ", i.getError(), " Fila: ", i.getFila(), " Columna: ", i.getColumna())
        else:
            self.erroresSintacticos = []