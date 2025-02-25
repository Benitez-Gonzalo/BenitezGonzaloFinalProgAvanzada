# módulo para organizar funciones o clases utilizadas en nuestro proyecto
from abc import ABC, abstractmethod
import numpy as np

class Alimento(ABC):
    """Clase abstracta que representa un alimento general"""   
    @abstractmethod
    def calcular_aw(self):
        pass

    @abstractmethod
    def getPeso(self):
        pass

class Fruta (Alimento, ABC): 
    """Clase abstracta que respresenta el tipo de alimento Fruta"""    
    @abstractmethod
    def calcular_aw(self):
        pass
    
    @abstractmethod
    def getPeso(self):
        pass

class Verdura(Alimento, ABC):
    """Clase abstracta que respresenta el tipo de alimento Verdura""" 
    @abstractmethod
    def calcular_aw(self):
        pass
    
    @abstractmethod
    def getPeso(self):
        pass

################################################################################################################################    

class Manzana (Fruta):
    """Clase que respresenta el tipo de Fruta Manzana""" 
    def __init__(self, peso):
        """Inicializador del objeto
        Manzana
        Args:
            peso (float): Atributo que
            nos da el peso del
            objeto manzana
        """        
        super().__init__()
        self.C = 15
        self.peso=peso
        
    def calcular_aw(self):
        """Funcion que calcula
        y devuelve el Aw del
        objeto Manzana

        Returns:
            float: Actividad
            acuosa del objeto
            Manzana
        """        
        return (0.97 * ((self.C * self.peso)**2)/(1 + (self.C * self.peso)**2))
    
    def getPeso(self):
        """Devuelve el
        atributo Peso
        del objeto

        Returns:
            float: Atributo
            peso del objeto
            Manzana
        """        
        return self.peso

class Kiwi (Fruta):
    """Clase que respresenta el tipo de Fruta Kiwi""" 
    def __init__(self, peso):
        """Inicializador del objeto
        Kiwi
        Args:
            peso (float): Atributo que
            nos da el peso del
            objeto Kiwi
        """  
        super().__init__() 
        self.C = 18
        self.peso=peso

    def calcular_aw(self):
        """Funcion que calcula
        y devuelve el Aw del
        objeto Kiwi

        Returns:
            float: Actividad
            acuosa del objeto
            Kiwi
        """ 
        
        return 0.96 * (1-(np.exp(-self.C * self.peso)))/(1 + (np.exp(-self.C * self.peso)))
    
    def getPeso(self):
        return self.peso
    
################################################################################################################################    

class Papa (Verdura):
    """Clase que respresenta el tipo de Vedura Papa""" 
    def __init__(self, peso):
        """Inicializador del objeto
        Papa
        Args:
            peso (float): Atributo que
            nos da el peso del
            objeto Papa
        """  
        super().__init__()
        self.C = 18
        self.peso=peso
        
        
    def calcular_aw(self):
        """Funcion que calcula
        y devuelve el Aw del
        objeto Papa

        Returns:
            float: Actividad
            acuosa del objeto
            Papa
        """ 
        return (0.66*(np.arctan(self.C * self.peso)))
    
    def getPeso(self):
        return self.peso

class Zanahoria(Verdura):       
    """Clase que respresenta el tipo de Vedura Zanahoria""" 

    def __init__(self, peso):
        """Inicializador del objeto
        Zanahoria
        Args:
            peso (float): Atributo que
            nos da el peso del
            objeto Zanahoria
        """  
        super().__init__()
        self.C = 10
        self.peso=peso
        
    def calcular_aw(self):
        """Funcion que calcula
        y devuelve el Aw del
        objeto Zanahoria

        Returns:
            float: Actividad
            acuosa del objeto
            Zanahoria
        """ 
        return (0.96*(1-np.exp(-self.C*self.peso)))
    
    def getPeso(self):
        return self.peso
    
    
