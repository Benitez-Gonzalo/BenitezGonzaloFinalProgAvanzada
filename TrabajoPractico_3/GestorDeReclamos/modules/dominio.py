"""
La capa de dominio es la responsable de representar los conceptos específicos de la 
aplicación y sus reglas. Esta capa define cómo se deben manejar los datos y qué operaciones son validas
dentro del contexto específico de la aplicación.
La capa de dominio no debe depender de funciones y variables de flask como session, no debe depender 
de cual sea la interfaz de usuario ni de cómo se almacenan los datos.

"""

from datetime import datetime

class Usuario:
    """Simula un usuario, tanto final como jefe o secretario técnico
    """
    def __init__(self,pId:str,pNombre:str,pNombreDeUsuario:str,pEmail:str,pClaustro:str,pContraseña:str):
        self.__id = pId
        self.__nombre = pNombre
        self.__nombreDeUsuario = pNombreDeUsuario
        self.__email = pEmail
        self.__claustro = pClaustro
        self.__contraseña = pContraseña
          
    @property
    def nombreDeUsuario(self):
        return self.__nombreDeUsuario
    
    @property
    def claustro(self):
        return self.__claustro
        
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def id(self):
        return self.__id
    
    @property
    def email(self):
        return self.__email
    
    @property
    def contraseña(self):
        return self.__contraseña

    
    @nombreDeUsuario.setter
    def nombreDeUsuario(self, p_nombreDeUsuario:str):
        if not isinstance(p_nombreDeUsuario, str) or p_nombreDeUsuario.strip() == "":
            raise ValueError("El nombre del usuario debe ser un string y no debe estar vacío")
        self.__nombre = p_nombreDeUsuario.strip()
    
    @claustro.setter
    def claustro(self, p_claustro:str):
        if not isinstance(p_claustro, str) or p_claustro.strip() == "":
            raise ValueError("El claustro debe ser texto no vacío")
        self.__nombre = p_claustro.strip()
    
    @nombre.setter
    def nombre(self, p_nombre:str):
        if not isinstance(p_nombre, str) or p_nombre.strip() == "":
            raise ValueError("El nombre del usuario debe ser un string y no debe estar vacío")
        self.__nombre = p_nombre.strip()
        
    @email.setter
    def email(self, p_email:str):
        if not isinstance(p_email, str) or p_email.strip() == "":
            raise ValueError("El email de usuario debe ser un string y no debe estar vacío")
        self.__email = p_email.strip()
        
    @contraseña.setter
    def password(self, password:str):
        self.__contraseña = password
    
   
    
class Reclamo:
    def __init__(self,p_id_reclamo,pContenido:str, pDepartamento:str, pEstado:str, pFechayHora:datetime,pId_usuario:int,pTiempoEstimado:int,pTiempoOcupado:int):
        self.__id_reclamo = p_id_reclamo
        self.__contenido = pContenido
        self.__departamento = pDepartamento
        self.__estado = pEstado
        self.__fechaYhora = pFechayHora
        self.__id_usuario = pId_usuario
        self.__tiempo_estimado = pTiempoEstimado
        self.__tiempo_ocupado = pTiempoOcupado

    @property
    def tiempo_ocupado(self):
        return self.__tiempo_ocupado
    
    @property
    def tiempo_estimado(self):
        return self.__tiempo_estimado
    
    @property
    def id_reclamo(self):
        return self.__id_reclamo
    
    @property
    def contenido(self):
        return self.__contenido
    
    @property
    def departamento(self):
        return self.__departamento
    
    @property
    def usuariosAdheridos(self):
        return self.__usuariosAdheridos
    
    @property
    def estado(self):
        return self.__estado
    
    @property
    def id_usuario(self):
        return self.__id_usuario
    
    @property
    def fecha_y_hora(self):
        return self.__fechaYhora
    
    @tiempo_estimado.setter
    def tiempo_estimado(self,p_tiempo):
        self.__tiempo_estimado = p_tiempo
        
    @tiempo_ocupado.setter
    def tiempo_ocupado(self,p_tiempo):
        self.__tiempo_ocupado = p_tiempo
    
    @contenido.setter
    def content(self,p_content:str):
        if p_content != None:
            if not isinstance(p_content,str) or p_content == "":
                raise ValueError("El contenido del reclamo debe ser texto y no debe estar vacío")
            self.__contenido = p_content
            
    @departamento.setter
    def departamento(self,p_depto:str):
        if p_depto != None:
            if not isinstance(p_depto,str) or p_depto =="":
                raise ValueError("El nombre del departamento debe ser texto no vacío")
            self.__departamento = p_depto
            
    @usuariosAdheridos.setter
    def usuariosAdh(self,p_usuarios:list):
        if p_usuarios != None:
            if not isinstance(p_usuarios,list):
                raise ValueError("La lista de usuarios adheridos no es interpretable.")
            self.__usuariosAdheridos = p_usuarios

    @estado.setter
    def estado(self,p_estado:str):
        if p_estado != None:
            if not isinstance(p_estado,str) or p_estado=="":
                raise ValueError("El estado debe ser texto no vacío")
            self.__estado = p_estado
            
    

#La composición entre "claims classifier " y "clasificador" radica en que "claims_classifier está guardado en la variable clf"

    
    
    
       
    
   




    
        