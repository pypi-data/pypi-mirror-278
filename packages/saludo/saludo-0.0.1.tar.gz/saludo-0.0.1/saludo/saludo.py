class Saludo:
    def __init__(self,nombre=str):
        self.__nombre = nombre

    def saludo_alexis(self):
        return f'Hola {self.__nombre}'
    
    