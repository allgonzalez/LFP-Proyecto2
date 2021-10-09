from Tokens import Token
from Registros import Registros

class Analizador:
    #Variable que guardará lo que vaya recorriendo poco a poco
    lexema = ''
    #Arreglo de tokens
    tokens = []
    #Arrreglo de Claves
    claves = []
    #Arreglo de registros
    registros = []
    #EStados para ir distribuyendo los distintos símbolos encontrados
    estado = 1
    #Fila en la que estoy
    fila = 1
    #Columna en la que estoy 
    columna = 1
    #Ayuda a ver si generamos un reporte de errores por si hay símbolos que son desconocidos
    generarErrores = False
    

 #----------------------------------------------Analizador lexico----------------------------------------------   

    def scanner(self, entrada):
        #Manejo de tipos
        global tipos
        tipos = Token("random", 0, 0,0) #Llenamos de datos random
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
                    self.estado = 6
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
                    self.agregarToken(tipos.CORCHETE_I)
                
                elif actual == ')':
                    self.columna +=1
                    self.lexema += actual
                    self.agregarToken(tipos.CORCHETE_D)
                
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
                elif actual =='_' and habilitar_cadena:
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
                    
                    if habilitar_comentario:
                        self.columna += 1
                        self.lexema += actual
                        self.estado = 6
                        if actual == '\n':
                            self.agregarToken(tipos.COMENTARIO_MULTILINEA)
                            self.fila += 1
                            habilitar_comentario = False
                    else:
                        self.columna += 1
                        self.lexema += actual
                        self.estado = 6



                elif actual == '\n' and self.lexema == "'''":
                    self.columna = 1
                    self.fila += 1
                    self.lexema += actual
                    habilitar_comentario = True
                    
                
                elif actual.isalpha() and habilitar_comentario:
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                elif actual.isdigit() and habilitar_comentario:
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                
                elif actual == ' ' and habilitar_comentario:
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6
                
                elif actual == '\n' and habilitar_comentario:
                    self.columna = 1
                    self.fila += 1
                    self.lexema += actual
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

    #Función para llenar las claves
    def Claves(self):
        Boolclave = False
        for i in self.tokens:
            
            if i.getLexema().lower() == 'claves':
                Boolclave = True
            if i.tipo == tipos.CADENA and Boolclave:

                self.claves.append(str(i.getLexema()))

            elif i.tipo == tipos.CORCHETE_D and Boolclave:
                Boolclave = False
                break
        
        for j in self.claves:
            print('clave: ', j)
    
    #Función para llenar registros
    def Registros(self):
        Boolregistro = False
        llave_i = False
        cont = 0

        for i in self.tokens:
            if i.getLexema().lower() == 'registros':
                Boolregistro = True

            elif i.tipo == tipos.LLAVE_I:
                llave_i = True
            
            elif i.tipo == tipos.CADENA or i.tipo == tipos.NUMERO:
                if Boolregistro:
                    self.registros.append(Registros(self.claves[cont], i.getLexema()))
                    cont +=1

            elif i.tipo == tipos.LLAVE_D  and llave_i:
                cont = 0
                llave_i = False
            
            elif i.tipo == tipos.CORCHETE_D and Boolregistro:
                Boolregistro = False
                break

        for j in self.registros:
            print("Clave: ",j.getClave(), " Registro:",j.getRegistro())
