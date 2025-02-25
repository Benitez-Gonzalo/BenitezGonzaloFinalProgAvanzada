from modules.Alimentos import Kiwi, Manzana, Papa, Zanahoria

def crear_alimento(dict_alimento): 
    if dict_alimento["alimento"] == "kiwi" : 
        alimento=Kiwi(dict_alimento["peso"])

    if dict_alimento["alimento"] == "manzana" : 
        alimento=Manzana(dict_alimento["peso"])
    
    if dict_alimento["alimento"] == "papa" : 
        alimento=Papa(dict_alimento["peso"])
 
    if dict_alimento["alimento"] == "zanahoria" : 
        alimento=Zanahoria(dict_alimento["peso"])

    if dict_alimento["alimento"] == "undefined": 
        return None 
   
    return alimento 


   