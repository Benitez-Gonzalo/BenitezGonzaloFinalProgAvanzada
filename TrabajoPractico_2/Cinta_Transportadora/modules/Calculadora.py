#Clase que modela una calculadora para la aw de cada fruta, la aw_promedio, y si es aceptable o no la aw de algún alimento
from modules import Alimentos as A
from modules.CajonDeAlimentos import CajonDeAlimento

class Calculadora():
    
    def __init__(self):
        self.alimentos = [] 

    def aw_promedio(self, tipoAlimento,cajon:CajonDeAlimento): 
            """Funcion que devuelve la
            atividad acuosa promedio de
            un alimento particular

            Args:
                TipoAlimento (Alimento): Clase
                de alimento que se buscara en el
                cajon, de encontrarse, se le calcula
                su Aw promedio

            Returns:
                float: Aw promedio del alimento
                que se le pasó (si existe un 
                elemento de ese tipo de alimento
                en la lista del cajon)
            """        
            aw = 0
            cantAlim = 0
            for alimento in cajon: 
                if isinstance(alimento, tipoAlimento): 
                    aw += alimento.calcular_aw()
                    cantAlim +=1
            if cantAlim > 0:
                return (round(aw/cantAlim,2)) 
            
            else :
                return 0
       

    def aw_alimentos(self,cajon):
        """Funcion que crea y
        devuelve un diccionario
        con las Aw promedio de 
        cada alimento, junto con
        la Aw total de los alimentos
        del cajon

        Returns:
            dict: diccionario
        con las Aw promedio de 
        cada alimento, junto con
        la Aw total de los alimentos
        del cajon
        """
         

        return{
        "aw_manzanas":self.aw_promedio(A.Manzana,cajon),
        "aw_kiwis" : self.aw_promedio(A.Kiwi,cajon),
        "aw_papas" :self.aw_promedio(A.Papa,cajon),
        "aw_zanahorias" :self.aw_promedio(A.Zanahoria,cajon),
        "aw_frutas" : self.aw_promedio(A.Fruta,cajon),
        "aw_verduras" : self.aw_promedio(A.Verdura,cajon),
        "aw_total" :self.aw_promedio(A.Alimento,cajon)
        }
 
    
    def awNoEsAceptable(self, aw_promedio):
        """Funcion que evalua si la
        aw promedio de cierto alimento
        es aceptable

        Args:
            aw_promedio (float):Aw a evaluar

        Returns:
            bool: Devuelve true si la aw
            no es aceptable y false si lo es
        """        
        if aw_promedio > 0.90:
            return True
        
   