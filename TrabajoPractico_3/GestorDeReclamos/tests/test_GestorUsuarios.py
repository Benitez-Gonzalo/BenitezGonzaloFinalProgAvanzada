import unittest
from unittest.mock import Mock
from werkzeug.security import check_password_hash
from modules.servicio import GestorUsuarios  # Asegúrate de importar la clase correctamente
from modules.dominio import Usuario  # La clase Usuario que se está utilizando en el método

class TestGestorUsuarios(unittest.TestCase):

    def setUp(self):
        # Creamos un Mock del repositorio
        self.repo_mock = Mock()
        self.gestor = GestorUsuarios(self.repo_mock)

    def test_registrar_nuevo_usuario_usuario_existente(self):
        """Debe lanzar ValueError si el usuario ya existe."""
        # Configuramos el Mock para simular que el usuario ya existe
        self.repo_mock.obtener_registro_por_filtro.return_value = True

        # Intentamos registrar un usuario ya existente
        with self.assertRaises(ValueError) as context:
            self.gestor.registrar_nuevo_usuario(
                nombre="José Rodríguez",
                nombreDeUsuario="JR",
                email="joserodriguez@ejemplo.com",
                claustro="estudiante",
                password="password123"
            )
        
        # Verificamos que se lanzó la excepción con el mensaje correcto
        self.assertEqual(str(context.exception), "El usuario ya está registrado")

        # Aseguramos que el método "guardar_registro" no fue llamado
        self.repo_mock.guardar_registro.assert_not_called()

    def test_registrar_nuevo_usuario_exitoso(self):
        """Debe registrar un nuevo usuario si no existe previamente."""
        # Configuramos el Mock para simular que el usuario no existe
        self.repo_mock.obtener_registro_por_filtro.return_value = None

        # Simulamos el método guardar_registro
        self.repo_mock.guardar_registro = Mock()

        # Datos del usuario
        nombre = "Juan Pérez"
        nombreDeUsuario = "jperez"
        email = "juan@example.com"
        claustro = "estudiante"
        password = "password123"

        # Llamamos al método
        self.gestor.registrar_nuevo_usuario(nombre, nombreDeUsuario, email, claustro, password)

        # Verificamos que "guardar_registro" fue llamado una vez
        self.repo_mock.guardar_registro.assert_called_once()

        # Verificamos que el usuario guardado tiene la contraseña encriptada
        usuario_guardado = self.repo_mock.guardar_registro.call_args[0][0]
        self.assertIsInstance(usuario_guardado, Usuario)
        self.assertNotEqual(usuario_guardado.contraseña, password)  # La contraseña no debe estar en texto plano
        self.assertTrue(check_password_hash(usuario_guardado.contraseña, password))  # Verificamos que la encriptación sea válida

    def test_registrar_nuevo_usuario_llamado_correctamente(self):
        """Verifica que los métodos del repositorio se llaman con los argumentos correctos."""
        # Configuramos el Mock para que el usuario no exista
        self.repo_mock.obtener_registro_por_filtro.return_value = None

        # Llamamos al método
        self.gestor.registrar_nuevo_usuario(
            nombre="Juan Pérez",
            nombreDeUsuario="jperez",
            email="juan@example.com",
            claustro="estudiante",
            password="password123"
        )

        # Verificamos que "obtener_registro_por_filtro" fue llamado con los argumentos correctos
        self.repo_mock.obtener_registro_por_filtro.assert_called_once_with("email", "juan@example.com")
        self.repo_mock.guardar_registro.assert_called_once()

if __name__ == '__main__':
    unittest.main()
