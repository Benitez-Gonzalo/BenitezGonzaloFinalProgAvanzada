from modules import Alimentos as A

class CajonDeAlimento():

    def __init__(self):
        """Inicializador del objeto
        CajonDeAlimento
        Args:
        """  
        self.__alimentos=[]
        
   
    def agregar_alimento(self, alimento): 
        """Funcion que agrega a una lista, objetos 
        alimento

        """        
        self.__alimentos.append(alimento)
       
#hago iterable el cajon para que pueda ser recorrido por el for en Calculadora
    def __iter__(self) : 
        return iter(self.__alimentos) 
    
    def __len__(self) : 
        return len(self.__alimentos)
      
     