from modules.Detector import DetectorAlimento 
from modules.factoria import crear_alimento

class CintaTransportadora:

    def __init__(self):
        """Inicializador del objeto
        CintaTransportadora
        """        
        self.__detector=DetectorAlimento() 
        
    def transportarAlimentos(self):
        """Funcion que agrega objetos alimento validos
        a la lista de alimentos de la cinta

        Args:
            CantidadAlimentosCajon (int):Cantidad de objetos
            alimento para meter en la lista de alimentos
        """        
       
        dict_alimento = self.__detector.detectar_alimento() #forma el diccionario con el alimento y el peso
        alimento= crear_alimento(dict_alimento)
        return alimento 
   