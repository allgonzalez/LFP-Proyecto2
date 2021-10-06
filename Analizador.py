from Tokens import Token

class Analizador:
    #Variable que guardará lo que vaya recorriendo poco a poco
    lexema = ''
    #Arreglo de tokens
    tokens = []
    #EStados para ir distribuyendo los distintos símbolos encontrados
    estado = 1
    #Fila en la que estoy
    fila = 1
    #Columna en la que estoy 
    columna = 1
    #Ayuda a ver si generamos un reporte de errores por si hay símbolos que son desconocidos
    generarErrores = False

    

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
        terminar_comentario = False
        inicio_comentario = True

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
                    self.estado = 4 
                    self.columna += 1
                    self.lexema += actual
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
                        self.agregarToken(tipos.CORCHETE_D)

            #Estado para las cadenas temporales
            elif self.estado == 4:
                if actual != '"':
                    self.estado = 4
                    self.columna += 1
                    self.lexema += actual
        
                elif actual == '"':
                    self.lexema += actual
                    self.columna += 1
                    self.agregarToken(tipos.CADENA)  

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
                
                if actual == "'" and inicio_comentario:
                    self.columna += 1
                    self.lexema += actual
                    self.estado = 6

                elif actual == '\n' and self.lexema == "'''":
                    self.columna = 1
                    self.fila += 1
                    habilitar_comentario = True
                    inicio_comentario = False
                
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

                
                elif actual == "'" and habilitar_comentario:
                    self.columna += 1
                    self.lexema += actual
                    temp += actual
                    if temp == "'''":
                        self.estado = 1
                        self.lexema += actual
                        self.agregarToken(tipos.COMENTARIO_MULTILINEA)
                        
                        habilitar_comentario = False
                        inicio_comentario = True

                    
                


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


