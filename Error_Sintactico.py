class ErrorSintactico():
    FALTO_IGUAL = 1
    FALTO_CORCHETE_I = 2
    FALTO_CORCHETE_D = 3
    FALTO_COMILLA_DOBLE = 4
    FALTO_COMA = 5
    FALTO_PUNTO_COMA = 6
    FALTO_COMILLA_SIMPLE = 7
    FALTO_PARENTESIS_I = 8
    FALTO_PARENTESIS_D = 9
    FALTO_LLAVE_I = 10
    FALTO_LLAVE_D = 11


    def __init__(self, error, fila, columna):
        self.error = error
        self.fila = fila
        self.columna = columna
    
    def getError (self):
        if self.error == self.FALTO_IGUAL:
            return  "SE ESPERA SIGNO IGUAL"
        elif self.error == self.FALTO_CORCHETE_I:
            return "SE ESPERA CORCHETE IZQUIERDO"
        elif self.error == self.FALTO_CORCHETE_D:
            return "SE ESPERA CORCHETE DERECHO"
        elif self.error == self.FALTO_COMILLA_DOBLE:
            return "SE ESPERA COMILLA DOBLE"
        elif self.error == self.FALTO_COMA:
            return "SE ESPERA UNA COMA"
        elif self.error == self.FALTO_PUNTO_COMA:
            return "SE ESPERA UN PUNTO Y COMA"
        elif self.error == self.FALTO_COMILLA_SIMPLE:
            return "SE ESPERA COMILLA SIMPLE"
        elif self.error == self.FALTO_PARENTESIS_I:
            return "SE ESPERA UN PARENTESIS IZQUIERDO"
        elif self.error == self.FALTO_PARENTESIS_D:
            return "SE ESPERA UN PARENTESIS DERECHO"
        elif self.error == self.FALTO_LLAVE_I:
            return "SE ESPERA UNA LLAVE IZQUIERDA"
        elif self.error == self.FALTO_LLAVE_D:
            return "SE ESPRA UNA LLAVE DERECHA"

    def getFila(self):
        return self.fila
        
    def getColumna(self):
        return self.columna