class Token():

    #Identificar por el número de tipo 
    NUMERO = 1
    PALABRA_RESERVADA = 2
    IGUAL = 3
    LLAVE_I = 4
    LLAVE_D = 5
    CORCHETE_I = 6
    CORCHETE_D = 7
    COMA = 8
    PUNTO_COMA = 9
    COMENTARIO_MULTILINEA = 10
    COMENTARIO_UNA_LINEA = 11
    HASH = 12
    PARENTESIS_I = 13
    PARENTESIS_D = 14
    CADENA = 15
    COMILLAS_DOBLE = 16
    FIN_DOCUMENTO = 17
    DESCONOCIDO = 18
    DOS_PUNTOS = 19   
    PUNTO = 20

    #Método constructor

    def __init__(self, lexema, tipo, fila, columna):
        self.lexema_valido = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def getLexema(self):
        return self.lexema_valido

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna
    
    def getTipo(self):
        if self.tipo == self.PALABRA_RESERVADA:
            return 'PALABRA RESERVADA'
        elif self.tipo == self.NUMERO:
            return 'NUMERO'
        elif self.tipo == self.IGUAL:
            return 'IGUAL'
        elif self.tipo == self.LLAVE_I:
            return 'LLAVE IZQUIERDA'
        elif self.tipo == self.LLAVE_D:
            return 'LLAVE DERECHA'
        elif self.tipo == self.CORCHETE_I:
            return 'CORCHETE IZQUIERDO'
        elif self.tipo == self.CORCHETE_D:
            return 'CORCHETE DERECHO'
        elif self.tipo == self.COMA:
            return 'COMA'
        elif self.tipo == self.PUNTO_COMA:
            return 'PUNTO Y COMA'
        elif self.tipo == self.COMENTARIO_MULTILINEA:
            return 'COMENTARIO MULTILINEA'

        elif self.tipo == self.COMENTARIO_UNA_LINEA:
            return 'COMENTARIO DE UNA LINEA'
        elif self.tipo == self.PARENTESIS_I:
            return 'PARENTESIS IZQUIERDO'
        elif self.tipo == self.PARENTESIS_D:
            return 'PARENTESIS DERECHO'
        elif self.tipo == self.CADENA:
            return 'CADENA'
        elif self.tipo == self.DESCONOCIDO:
            return 'DESCONOCIDO'
        elif self.tipo == self.COMILLAS_DOBLE:
            return 'COMILLAS DOBLE'
        elif self.tipo == self.FIN_DOCUMENTO:
            return 'FIN DEL DOCUMENTO'
        elif self.tipo == self.DOS_PUNTOS:
            return 'DOS PUNTOS'
        elif self.tipo == self.PUNTO:
            return 'PUNTO'
