import unittest
from unittest.mock import Mock
from werkzeug.security import check_password_hash
from modules.servicio import GestorUsuarios  # Asegúrate de importar la clase correctamente
from modules.dominio import Usuario  # La clase Usuario que se está utilizando en el método

class TestGestorUsuarios(unittest.TestCase):

    #Usé un método "setUp" porque más de un test mockea un repo y usa un objeto GestorUsuarios.
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
        # Arrange
        # Configuramos el mock para que no haya usuarios existentes
        self.repo_mock.obtener_registro_por_filtro.return_value = None

        # Datos de prueba
        nombre = "Juan Pérez"
        nombreDeUsuario = "jperez"
        email = "juan@ejemplo.com"
        claustro = "estudiante"
        password = "password123"

        # Act
        resultado = self.gestor.registrar_nuevo_usuario(
            nombre=nombre,
            nombreDeUsuario=nombreDeUsuario,
            email=email,
            claustro=claustro,
            password=password
        )

        # Assert
        # Verificamos que obtener_registro_por_filtro fue llamado dos veces con los argumentos correctos
        calls = [call('email', email), call('nombreDeUsuario', nombreDeUsuario)]
        self.repo_mock.obtener_registro_por_filtro.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.repo_mock.obtener_registro_por_filtro.call_count, 2)

        # Verificamos que guardar_registro fue llamado con un objeto Usuario correcto
        usuario_esperado = Usuario(None, nombre, nombreDeUsuario, email, claustro, ANY)  # ANY para la contraseña encriptada
        self.repo_mock.guardar_registro.assert_called_once()
        args, _ = self.repo_mock.guardar_registro.call_args
        usuario_guardado = args[0]
        self.assertIsInstance(usuario_guardado, Usuario)
        self.assertEqual(usuario_guardado.nombre, nombre)
        self.assertEqual(usuario_guardado.nombreDeUsuario, nombreDeUsuario)
        self.assertEqual(usuario_guardado.email, email)
        self.assertEqual(usuario_guardado.claustro, claustro)

        # Verificamos que el método devuelve True
        self.assertTrue(resultado)

if __name__ == '__main__':
    unittest.main()
