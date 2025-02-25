import re
from collections import Counter
from nltk.corpus import stopwords

from modules.persistencia import RepositorioReclamosSQLAlchemy


class GestorEstadistico:
    def __init__(self,pRepoReclamos:RepositorioReclamosSQLAlchemy):
        self.__repoReclamos = pRepoReclamos
        

    def obtenerDatosPieChart(self):
        """Brinda los datos estadísticos para el graficador para el gráfico de torta

        Raises:
            ValueError: No hay reclamos

        Returns:
            list[float]: Porcentajes de cada estado de reclamo
        """
        reclamos = self.__repoReclamos.obtener_todos_los_registros()
        cantidad_pendientes,cantidad_en_proceso,cantidad_resueltos,cantidad_invalidos = 0,0,0,0
        for reclamo in reclamos:
            if reclamo.estado=='pendiente':cantidad_pendientes+=1
            elif reclamo.estado=='en proceso':cantidad_en_proceso+=1
            elif reclamo.estado=='resuelto':cantidad_resueltos+=1
            else: cantidad_invalidos+=1
        subgrupos = [cantidad_en_proceso,cantidad_invalidos,cantidad_pendientes,cantidad_resueltos]
        total = sum(subgrupos) 
        if total == 0:  
            raise ValueError("El total de elementos no puede ser cero")
        porcentajes = [(cantidad / total) * 100 for cantidad in subgrupos]
        return porcentajes
     
    def obtenerDatosParaWordcloud(self):
        """Brinda los datos para el gráfico WordCloud

        Returns:
            Counter: La frecuencia de cada una de las palabras.
        """
        # 1. Obtener el contenido de cada reclamo
        reclamos = self.__repoReclamos.obtener_todos_los_registros() #Todos los objetos "Reclamo"
        lista_contenido_reclamos=[]
        for reclamo in reclamos:
            lista_contenido_reclamos.append(reclamo.contenido)
            
        # 2. Procesar el contenido y calcular frecuencias de palabras clave
        texto_completo = " ".join(lista_contenido_reclamos)  # Unir todos los textos
        palabras = re.findall(r'\b\w+\b', texto_completo.lower())  # Tokenizar palabras
        
        # 3. Filtrar stopwords y contar frecuencia
        palabras_a_ignorar = set(stopwords.words('spanish'))
        palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_a_ignorar]
        frecuencia_palabras = Counter(palabras_filtradas)
        
        print("Datos procesados para Wordcloud:", frecuencia_palabras.most_common(10))
        return frecuencia_palabras
