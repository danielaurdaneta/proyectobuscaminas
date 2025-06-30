from abc import ABC, abstractmethod

class Casilla(ABC):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.revelada = False
        self.marca = None

    def revelar(self):
        if not self.revelada:
            self.revelada = True
            return self.es_mina()
        return False
    
    @abstractmethod #metodo abstracto que será implementado por subclases
    def mostrar (self):
        pass
    
    def marcar(self, marca):#quita o pone marca
        if not self.revelada:
            self.marca = marca
            return True
        return False


    def es_bandera(self):
        return self.marca == 'bandera'
    
    def quitar_marca(self):
        if self.marca != None:
            self.marca = None
            self.revelada = False
        else:
            return False

#clase hija de casilla
class CasillaVacia(Casilla):
    def __init__(self, fila, columna):
        super().__init__(fila, columna)
        self.minas_colindantes = 0

    def mostrar(self):#utilizando el metodo abstracto
        return str(self.minas_colindantes) if self.minas_colindantes > 0 else " "

    def es_mina(self):
        return False

#clase hija de casilla
class CasillaMina(Casilla):
    def mostrar(self):#utilizando el metodo abstracto
        return "*"

    def es_mina(self):
        return True