from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps

class FlaskLoginUser(UserMixin):
    def __init__(self, dicc_usuario:dict):
        self.id=dicc_usuario["id"]
        self.nombre = dicc_usuario["nombre"]
        self.email = dicc_usuario["email"]
        self.contraseña = dicc_usuario["contraseña"]

class GestorLogin:
    def __init__(self, gestor_usuarios, login_manager):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.cargar_usuario_actual)
        
    @property
    def mail(self):
        if current_user.is_authenticated:
            return current_user.email
        else:
            return "Invitado"

    @property
    def nombre_usuario_actual(self):
        if current_user.is_authenticated:
            return current_user.nombre  # Solo se accede si está autenticado
        else:
            return "Invitado"  # Valor por defecto para usuarios no autenticados

    @property
    def id_usuario_actual(self):
        if current_user.is_authenticated:
            return current_user.id
        else:
            return "Invitado"
    
    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated


    def cargar_usuario_actual(self, id_usuario):
        dicc_usuario = self.__gestor_usuarios.cargar_usuario(id_usuario)
        return FlaskLoginUser(dicc_usuario)
    
    def login_usuario(self, dicc_usuario):
        user = FlaskLoginUser(dicc_usuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")
    
    def se_requiere_login(self, func):
        return login_required(func)
    