from modules.dominio import Reclamo

from datetime import datetime
from modules.clasesAbstractas import RepositorioAbstracto
from modules.persistencia import Clasificador
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class GestorDeReclamos:
    def __init__(self,repo:RepositorioAbstracto):
        self.__repo = repo
        self.__clasificador = Clasificador()
        self.__numero_reclamos = len(self.__repo.obtener_todos_los_registros())
             
    def obtener_reclamo_similar(self, filtro, valor):
        """Chequea la existencia de reclamos similares o idénticos al ingresado

        Args:
            filtro (str): Categoría "contenido" del reclamo
            valor (str): Contenido del reclamo

        Returns:
            tuple: (reclamo_identico, reclamos_similares)
                - reclamo_identico: Objeto Reclamo si hay uno idéntico, None si no
                - reclamos_similares: Lista de reclamos similares si no hay idéntico, vacía si no hay similares
        """
        reclamos = self.__repo.obtener_todos_los_registros()
        
        # Buscar reclamo idéntico
        reclamo_identico = self.__repo.obtener_registro_por_filtro(filtro, valor)
        if reclamo_identico and reclamo_identico.estado != 'resuelto':
            print("El reclamo idéntico es: ", reclamo_identico.contenido)
            print("El estado del reclamo idéntico es: ", reclamo_identico.estado)
            return reclamo_identico, []  # Hay idéntico, no buscamos similares
        
        # Si no hay idéntico y hay reclamos, buscamos similares
        if reclamos:
            vectorizer = TfidfVectorizer(stop_words='english')
            textos = [r.contenido for r in reclamos] + [valor]
            tfidf_matrix = vectorizer.fit_transform(textos)
            similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            umbral_similitud = 0.5  # Ajustable según necesidad
            
            reclamos_similares = [reclamos[idx] for idx, sim in enumerate(similitudes[0]) if sim > umbral_similitud]
            if reclamos_similares:
                for reclamo in reclamos_similares:
                    print("Reclamos similares: ", reclamo.contenido)
                return None, reclamos_similares
            return None, []  # No hay ni idéntico ni similares
        
        return None, []  # No hay reclamos en la base
            
    def brindar_usuarios_adheridos_por_reclamo(self):
        return self.__repo.obtener_usuarios_adheridos_por_reclamo()    
        
    def devolver_reclamos_segun_departamento(self, departamento):
        if departamento:
            registros = self.__repo.obtener_registros_por_filtro('clasificacion', departamento)
            if not registros:
                return []
            return [reclamo for reclamo in registros] #lista de diccionarios con entidades
        else:
            return self.__repo.obtener_todos_los_registros()
    
    def obtener_tiempos_por_departamento(self, departamento):
        """Devuelve listas de tiempos estimados y ocupados solo para los reclamos de un departamento específico.

        Args:
            departamento (str): El departamento por el cual filtrar los reclamos.

        Returns:
            tuple: (lista_tiempos_estimados, lista_tiempos_ocupados)
        """
        reclamos = self.__repo.obtener_registros_por_filtro('clasificacion', departamento)
        lista_tiempos_estimados = [reclamo.tiempo_estimado for reclamo in reclamos if reclamo.tiempo_estimado is not None]
        lista_tiempos_ocupados = [reclamo.tiempo_ocupado for reclamo in reclamos if reclamo.tiempo_ocupado is not None]
        return lista_tiempos_estimados, lista_tiempos_ocupados
    
    def obtener_tiempos(self):
        """Devuelve una lista con los tiempo que se estima que va a
        tardar en resolverse cada reclamo y otra lista con el tiempo
        que llevó resolverlo.

        Returns:
            list[int]:tiempos estimados,list[int]:tiempos_ocupados
        """
        reclamos = self.__repo.obtener_todos_los_registros() 
        lista_tiempos_estimados=[]
        lista_tiempos_ocupados=[]
        for reclamo in reclamos:
            lista_tiempos_estimados.append(reclamo.tiempo_estimado)
            lista_tiempos_ocupados.append(reclamo.tiempo_ocupado)
        return lista_tiempos_estimados,lista_tiempos_ocupados

    def creación_reclamo(self,contenido: str, id_usuario: str):
        """Crea un nuevo reclamo y lo guarda en la base de datos.
        
        Args:
            contenido (str): El texto del reclamo que será clasificado y almacenado.
            id_usuario (str): El identificador del usuario que crea el reclamo.

        Returns:
            None: La función no devuelve un valor explícito.
        """
        clasificacion = self.__clasificador.clasificar_reclamo(contenido)[0]
        fecha_de_creacion= datetime.now()
        tiempo_estimado = 0
        tiempo_ocupado = 0
        nuevo_reclamo = Reclamo(None, contenido, clasificacion,"pendiente", fecha_de_creacion, id_usuario, tiempo_estimado,tiempo_ocupado)
        self.__repo.guardar_registro(nuevo_reclamo)
        self.__numero_reclamos += 1
            
        
    def modificar_reclamo(self, id_reclamo, **kwargs):
        """Función que modifica un reclamo en la base de datos

        Args:
            id_reclamo (int): id del reclamo a modificar en la base de datos

        Returns:
            Reclamo: el reclamo modificado
        """
        # Obtener el reclamo actual de la base de datos
        reclamo = self.__repo.obtener_registro_por_filtro('id', id_reclamo)
        if not reclamo:
            return False  # Reclamo no encontrado

        # Actualizar solo los campos proporcionados en kwargs
        if 'departamento' in kwargs:
            reclamo.departamento = kwargs['departamento']
        if 'estado' in kwargs:
            reclamo.estado = kwargs['estado']
        if 'tiempo_estimado' in kwargs:
            reclamo.tiempo_estimado = kwargs['tiempo_estimado']
        if 'tiempo_ocupado' in kwargs:
            reclamo.tiempo_ocupado = kwargs['tiempo_ocupado']

        # Guardar los cambios en la base de datos
        return self.__repo.modificar_registro(reclamo)
        