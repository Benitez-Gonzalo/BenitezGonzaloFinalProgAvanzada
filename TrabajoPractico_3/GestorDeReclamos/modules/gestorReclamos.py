from modules.dominio import Reclamo

from datetime import datetime
from sqlalchemy import func
from modules.persistencia import RepositorioReclamosSQLAlchemy
from modules.persistencia import Clasificador
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.modelos import ModeloReclamo,ModeloUsuario,asociacion_usuarios_reclamos


class GestorDeReclamos:
    def __init__(self,repo:RepositorioReclamosSQLAlchemy):
        self.__repo = repo
        self.clasificador = Clasificador()
        self.__numero_reclamos = len(self.__repo.obtener_todos_los_registros())
        
    def brindar_usuarios_adheridos_por_reclamo(self):
        return self.__repo.obtener_usuarios_adheridos_por_reclamo()
        
    def obtener_reclamo_similar(self, filtro, valor):
        """Chequea la existencia de reclamos similares al ingresado

        Args:
            filtro (str): categoría "contenido" del reclamo
            valor (str): contenido del reclamo

        Returns:
            list[Reclamos]
        """
        # Recuperar todos los reclamos de la base de datos (sin aplicar filtro)
        # modelos_reclamos es una lista de objetos
        #modelos_reclamos = self.__repo.sesion().query(ModeloReclamo).all()
        reclamos = self.__repo.obtener_todos_los_registros()
        
        # Si hay reclamos existentes, evaluamos la similitud
        if reclamos:
            print(f"Los datos del reclamo son", filtro, valor, "Y los reclamos son", {r.contenido for r in reclamos})
            # Usamos TF-IDF para convertir los textos en vectores numéricos
            vectorizer = TfidfVectorizer(stop_words='english')
            textos = [r.contenido for r in reclamos] + [valor]  # Todos los reclamos + el nuevo
            
            # Vectorizamos los textos
            tfidf_matrix = vectorizer.fit_transform(textos)
            
            # Calculamos la similitud de coseno entre el nuevo reclamo y los existentes
            similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

            # Definir un umbral de similitud para considerar un reclamo como "similar"
            umbral_similitud = 0.5  # Este valor se puede ajustar según tu criterio

            reclamos_similares = []
            for idx, sim in enumerate(similitudes[0]):
                if sim > umbral_similitud:  # Si la similitud es mayor que el umbral
                    reclamos_similares.append(reclamos[idx])

            # Si se encontraron reclamos similares, devolverlos
            if reclamos_similares:
                return reclamos_similares
            else:
                return []
        
        else:
            # Busca un reclamo que sea identico al valor para asegurarse que el reclamo no exista previamente
            return self.__repo.obtener_registro_por_filtro(filtro, valor)
        
        
    def devolver_reclamos_segun_departamento(self, departamento):
        if departamento:
            registros = self.__repo.obtener_registros_por_filtro('clasificacion', departamento)
            if not registros:
                return []
            return [reclamo for reclamo in registros] #lista de diccionarios con entidades
        else:
            return self.__repo.obtener_todos_los_registros()
    
    def obtener_tiempos(self):
        """Devuelve una lista con el tiempo que se estima que va a
        tardar en resolverse cada reclamo

        Returns:
            list[int]:tiempos estimados
        """
        modelo_reclamos = self.__repo.obtener_todos_los_registros()
        lista_tiempos_estimados=[]
        lista_tiempos_ocupados=[]
        for reclamo in modelo_reclamos:
            lista_tiempos_estimados.append(reclamo.tiempo_estimado)
            lista_tiempos_ocupados.append(reclamo.tiempo_ocupado)
        return lista_tiempos_estimados,lista_tiempos_ocupados

    def creación_reclamo(self,contenido: str, id_usuario: str):
        """funcion que crea el reclamo y lo despacha para ser guardado en la base de datos"""
        clasificacion = self.clasificador.clasificar_reclamo(contenido)[0]
        fecha_de_creacion= datetime.now()
        tiempo_estimado = 0
        tiempo_ocupado = 0
        nuevo_reclamo = Reclamo(None, contenido, clasificacion,"pendiente", fecha_de_creacion, id_usuario, tiempo_estimado,tiempo_ocupado)
        self.__repo.guardar_registro(nuevo_reclamo)
        self.__numero_reclamos += 1
            
        
    def modificar_reclamo(self, id_reclamo, **kwargs):
        """
        Modifica un reclamo en función de los valores proporcionados en kwargs.
        Solo actualiza los campos que se pasan explícitamente.
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
        
    def clasificar(self,pClasificador:Clasificador,contenido):
        clasificacion = pClasificador.clasificar_reclamo(contenido)
        return clasificacion #La clasificación es el departamento al cual pertenece el reclamo