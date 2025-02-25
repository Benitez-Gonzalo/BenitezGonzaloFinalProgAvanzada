import matplotlib.pyplot as plt
from wordcloud import WordCloud

from modules.gestorEstadistico import GestorEstadistico

class Graficador:
    def __init__(self,pGestor:GestorEstadistico):
        self.__gestor = pGestor
    
    def mostrarGraficas(self,ruta_img:str,mediana_reclamos_en_proceso,mediana_reclamos_resueltos):
        fig, axis = plt.subplots(1, 2, figsize=(10, 5))
        # Gráfico WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(self.__gestor.obtenerDatosParaWordcloud())
        axis[0].imshow(wordcloud, interpolation="bilinear")
        axis[0].axis("off")  # Ocultar ejes
        axis[0].set_title("Wordcloud - Palabras Clave en Reclamos")
        # Gráfico de torta
        axis[1].pie([self.__gestor.obtenerDatosPieChart()[0],self.__gestor.obtenerDatosPieChart()[1],
                     self.__gestor.obtenerDatosPieChart()[2],self.__gestor.obtenerDatosPieChart()[3]],
                    labels=['En proceso', 'Invalidos','Pendientes','Resueltos'],
                    autopct='%1.1f%%',colors=['green', 'red','blue','yellow'])
        axis[1].axis('equal')  # Para que la gráfica sea un círculo
        axis[1].set_title(f"Mediana reclamos en proceso:{mediana_reclamos_en_proceso}\nMediana reclamos resueltos:{mediana_reclamos_resueltos}")
        plt.tight_layout()   
        plt.savefig(ruta_img)

        
    