"""La capa de persistencia maneja el almacenamiento y recuperación de datos, por ejemplo,
usando archivos de texto. Esta capa es la que se debe modificar o reemplazar si cambio de tecnología
para almacenar los datos (por ejemplo con una base de datos). La capa de dominio no debe verse afectada
por este cambio.
"""

#El manejo de los repositorios se hizo utilizando polimorfismo.

import pickle
from modules.dominio import Usuario,Reclamo
from modules.modelos import ModeloReclamo,ModeloUsuario,asociacion_usuarios_reclamos
from modules.clasesAbstractas import RepositorioAbstracto


class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        self.__tabla_reclamo = ModeloReclamo()
        self.__tabla_reclamo.metadata.create_all(self.__session.bind)
    #el atributo metadata contiene informacion sobre el esquema de la base de datos(columnas,relaciones,etc)
    #bind referencia al motor que crea las tablas
    
    def obtener_usuarios_adheridos_por_reclamo(self):
        """
        Devuelve un diccionario donde las claves son los IDs de los reclamos
        y los valores son listas con los IDs de los usuarios adheridos.
        """
        # Obtener todos los reclamos
        reclamos = self.__session.query(ModeloReclamo).all()
        
        # Construir el diccionario
        usuarios_por_reclamo = {}
        for reclamo in reclamos:
            # Obtener los IDs de los usuarios adheridos al reclamo
            usuarios_adheridos = [usuario.id for usuario in reclamo.usuarios_seguidores]
            # Agregar al diccionario
            usuarios_por_reclamo[reclamo.id] = usuarios_adheridos
        
        return usuarios_por_reclamo
    
    def guardar_registro(self,reclamo):
        """Método que hereda de la clase 'RepositorioAbstracto' y que guarda un reclamo

        Args:
            reclamo (_type_): reclamo del usuario, debe ser de la instancia 'Reclamo'

        Raises:
            ValueError: Se ejecuta en caso de que el reclamo no sea del tipo 'Reclamo'
        """
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El reclamo no es una instancia de la clase Reclamo")
        modelo_reclamo = self.__map_entidad_a_modelo(reclamo)
        self.__session.add(modelo_reclamo)
        #Las siguientes dos líneas se encargan de que el usuario creador siga automáticamente al reclamo
        usuario = self.__session.query(ModeloUsuario).filter_by(id=reclamo.id_usuario).first()
        usuario.reclamos_seguidos.append(modelo_reclamo) 
        self.__session.commit()
        
    def obtener_todos_los_registros(self):
        """Devuelve todos los reclamos existentes
    
        Returns:
            list[Reclamo]
        """
        modelo_reclamo = self.__session.query(ModeloReclamo).all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamo] 
    
    def modificar_registro(self, reclamo_modificado):
        """
        Actualiza un reclamo en la base de datos.
        """
        
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parámetro no es una instancia de ModeloReclamo")
        
        registro = self.__session.query(ModeloReclamo).filter_by(id=reclamo_modificado.id_reclamo).first()
        registro.clasificacion = reclamo_modificado.departamento
        registro.id_usuario = reclamo_modificado.id_usuario
        registro.fecha_de_creacion = reclamo_modificado.fecha_y_hora
        registro.estado = reclamo_modificado.estado
        if reclamo_modificado.estado == 'en proceso':
            registro.tiempo_estimado = reclamo_modificado.tiempo_estimado
            registro.tiempo_ocupado = None
        elif reclamo_modificado.estado == 'resuelto':
            registro.tiempo_ocupado = reclamo_modificado.tiempo_ocupado
        else:
            registro.tiempo_ocupado = None
            registro.tiempo_estimado = None
            
        self.__session.commit()
        return True  # Confirmación de éxito                                                                                                                             
    
    def obtener_registros_por_filtro(self, filtro, valor):
        modelos_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro:valor}).all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelos_reclamo] if modelos_reclamo else None 
    
    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_reclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None
        
    def __map_entidad_a_modelo(self, entidad: Reclamo):
        return ModeloReclamo(
            id = entidad.id_reclamo,
            contenido = entidad.contenido,
            clasificacion = entidad.departamento,
            id_usuario = entidad.id_usuario,
            fecha_de_creacion = entidad.fecha_y_hora,
            estado = entidad.estado,
            tiempo_estimado=entidad.tiempo_estimado,
            tiempo_ocupado = entidad.tiempo_ocupado
        )
    
    def __map_modelo_a_entidad(self, modelo: ModeloReclamo):
        return Reclamo(
            modelo.id,
            modelo.contenido,
            modelo.clasificacion,
            modelo.estado,
            modelo.fecha_de_creacion,
            modelo.id_usuario,
            modelo.tiempo_estimado,
            modelo.tiempo_ocupado   
        )
        


class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self,session):
        self.__session = session
        self.__tablaUsuario = ModeloUsuario()
        self.__tablaUsuario.metadata.create_all(self.__session.bind)
        
    #Esta función se encarga de la asociación de usuarios y seguidores cuando el usuario decide adherirse a un reclamo
    #----------------------------------------------------------------------------------------------------------------------------       
    def asociar_registro(self, id_usuario, id_reclamo):
        """Se encarga de cuando un usuario quiere adherirse a un reclamo

        Args:
            id_usuario (int): ForeignKey del usuario en la base de datos
            id_reclamo (int): ForeignKey del reclamo en la base de datos

        Raises:
            ValueError: Error si el usuario no existe

        Returns:
            bool: La operación fue exitosa
        """
        # Verificar si ya existe la relación en la tabla de asociación
        existe_relacion = self.__session.query(asociacion_usuarios_reclamos).filter_by(
            user_id=id_usuario,
            claim_id=id_reclamo
        ).first()

        if existe_relacion:
            return False  # Ya está adherido, no hacer nada

        # Si no existe, asociar el usuario con el reclamo
        usuario = self.__session.query(ModeloUsuario).filter_by(id=id_usuario).first()
        reclamo = self.__session.query(ModeloReclamo).filter_by(id=id_reclamo).first()

        if not usuario or not reclamo:
            raise ValueError("Usuario o reclamo no encontrados.") #Esto es para mí, no para el usuario

        usuario.reclamos_seguidos.append(reclamo)
        self.__session.commit()
        return True  # Indicar que se realizó la adhesión
    #----------------------------------------------------------------------------------------------------------------------------
    
    def modificar_registro(self,id_usuario,id_reclamo):
        pass
    
    def obtener_todos_los_registros(self):
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]  
        
    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None
    
    def obtener_modelo_por_filtro(self, filtro, valor):
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro:valor}).first()
        return modelo_usuario if modelo_usuario else None
    
    def guardar_registro(self, usuario):
        """Almacena el usuario en la base de datos

        Args:
            usuario (Usuario): usuario registrado

        Raises:
            ValueError: Por si ocurre un error raro y el usuario no es de su tipo.
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        self.__session.commit()
        
    def __map_entidad_a_modelo(self, entidad: Usuario):
        return ModeloUsuario(
            id=entidad.id,
            nombre=entidad.nombre,
            nombreDeUsuario=entidad.nombreDeUsuario,
            email=entidad.email,
            claustro=entidad.claustro,
            contraseña=entidad.contraseña,
        )
    
    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
            modelo.id,
            modelo.nombre,
            modelo.nombreDeUsuario,
            modelo.email,
            modelo.claustro,
            modelo.contraseña,
        )

class Clasificador:
    
    def __init__(self):
       pass
    
    def clasificar_reclamo(self,contenido:str):
        with open('./data/claims_clf.pkl', 'rb') as archivo:
            clf  = pickle.load(archivo) #La composición entre "claims classifier " y "clasificador" radica en que "claims_classifier está guardado en la variable clf"    
        
            lista_reclamos = [contenido]
            clasificacion = clf.clasificar(lista_reclamos)

            """ Las etiquetas que devuelve este clasificador son: soporte informático, secretaría técnica y maestranza."""
        return clasificacion                
        