from werkzeug.security import generate_password_hash, check_password_hash
from modules.clasesAbstractas import RepositorioAbstracto

from modules.dominio import Usuario
  
class GestorUsuarios:
    def __init__(self,repo:RepositorioAbstracto):
        self.__repo = repo
        
    def registrar_nuevo_usuario(self,nombre:str,nombreDeUsuario:str,email:str,claustro:str,password:str):
        """Registra un nuevo usuario

        Args:
            nombre (str): Nombre de la persona que se está registrando.
            nombreDeUsuario (str): Nombre del usuario que está creando la persona.
            email (str): email
            claustro (str): Estudiante, docente o PAyS
            password (str): contraseña

        Raises:
            ValueError: En caso de que ya esté registrado el usuario

        Returns:
            True: En caso de que el registro sea exitoso
        """
        if self.__repo.obtener_registro_por_filtro("email",email) or self.__repo.obtener_registro_por_filtro('nombreDeUsuario', nombreDeUsuario):
            raise ValueError("El usuario ya está registrado")
        else:
            pass_encriptada=generate_password_hash(password=password,
                                                method= 'pbkdf2:sha256',
                                                salt_length=8)
            usuario = Usuario(None,nombre,nombreDeUsuario,email,claustro,pass_encriptada)
            self.__repo.guardar_registro(usuario)
            return True
        
    def obtener_reclamos_del_usuario(self, id_usuario): 
        print("El id del usuario dentro de la función es", id_usuario)
        modelo_usuario = self.__repo.obtener_modelo_por_filtro('id',id_usuario)
        if not modelo_usuario:
            print("Hay un error con el modelo usuario")  
            return []
        return [
            {
                "contenido": reclamo.contenido,  
                "estado": reclamo.estado,    
            }
            for reclamo in modelo_usuario.reclamos_seguidos
        ]
        
    def autenticar_usuario(self, email:str, password:str):
        """Se encarga del loguin de los usuarios

        Args:
            email (str): email del usuario
            password (str): contraseña del usuario

        Returns:
            dict : Diccionario con la información del usuario
            False: Si el loguin falló, ya sea porque no se encontró el usuario o falló la contraseña.
        """
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            return False
        elif not check_password_hash(usuario.contraseña, password):
            return False
        return usuario.to_dict()
    
    def cargar_usuario(self, id_usuario):
        return self.__repo.obtener_registro_por_filtro("id", id_usuario).to_dict()
    
    def registrar_reclamo_a_seguir(self, id_usuario, id_reclamo):
        resultado = self.__repo.asociar_registro(id_usuario, id_reclamo)
        if resultado:
            return True
        else:
            return False