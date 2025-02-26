import matplotlib.pyplot as plt
from wordcloud import WordCloud

from modules.gestorEstadistico import GestorEstadistico

class Graficador:
    def __init__(self,pGestor:GestorEstadistico):
        self.__gestor = pGestor
    
    def mostrarGraficas(self, ruta_img: str, mediana_reclamos_en_proceso, mediana_reclamos_resueltos, departamento=None):
        fig, axis = plt.subplots(1, 2, figsize=(10, 5))
        # Gráfico WordCloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(self.__gestor.obtenerDatosParaWordcloud(departamento))
        axis[0].imshow(wordcloud, interpolation="bilinear")
        axis[0].axis("off")
        axis[0].set_title(f"Wordcloud - Palabras Clave en Reclamos ({departamento or 'Todos'})")
        # Gráfico de torta
        datos_pie = self.__gestor.obtenerDatosPieChart(departamento)
        axis[1].pie(datos_pie, labels=['En proceso', 'Invalidos', 'Pendientes', 'Resueltos'], autopct='%1.1f%%', colors=['green', 'red', 'blue', 'yellow'])
        axis[1].axis('equal')
        axis[1].set_title(f"Mediana reclamos en proceso: {mediana_reclamos_en_proceso}\nMediana reclamos resueltos: {mediana_reclamos_resueltos}\n({departamento or 'Todos'})")
        plt.tight_layout()
        plt.savefig(ruta_img)

        
    