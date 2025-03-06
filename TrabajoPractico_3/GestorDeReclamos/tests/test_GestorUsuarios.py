import unittest
from unittest.mock import Mock, MagicMock, call, patch
from werkzeug.security import check_password_hash
from modules.gestorUsuarios import GestorUsuarios  # Asegúrate de importar la clase correctamente
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


    def test_registrar_nuevo_usuario_llamado_correctamente(self):
        """Verifica que los métodos del repositorio se llaman con los argumentos correctos."""
        # Arrange
        self.repo_mock.obtener_registro_por_filtro.return_value = None
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
        calls = [call('email', email), call('nombreDeUsuario', nombreDeUsuario)]
        self.repo_mock.obtener_registro_por_filtro.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.repo_mock.obtener_registro_por_filtro.call_count, 2)

        # Verificamos que guardar_registro fue llamado una vez y extraemos el argumento
        self.repo_mock.guardar_registro.assert_called_once()
        args, _ = self.repo_mock.guardar_registro.call_args
        usuario_guardado = args[0]

        # Comparamos los atributos relevantes
        self.assertIsInstance(usuario_guardado, Usuario)
        self.assertEqual(usuario_guardado.id, None)
        self.assertEqual(usuario_guardado.nombre, nombre)
        self.assertEqual(usuario_guardado.nombreDeUsuario, nombreDeUsuario)
        self.assertEqual(usuario_guardado.email, email)
        self.assertEqual(usuario_guardado.claustro, claustro)
        # No verificamos la contraseña exacta porque es encriptada, pero podemos asegurar que existe
        self.assertIsNotNone(usuario_guardado.contraseña)

        self.assertTrue(resultado)
        
    def test_autenticar_usuario_exitoso(self):
        """Verifica que se autentica correctamente un usuario con email y contraseña válidos."""
        # Arrange
        email = "juan@ejemplo.com"
        password = "password123"
        # Simulamos un usuario existente
        usuario_mock = MagicMock(spec=Usuario)
        usuario_mock.contraseña = "hashed_password"  # Contraseña encriptada simulada
        # Configuramos los atributos privados que usa to_dict()
        usuario_mock._Usuario__id = 1
        usuario_mock._Usuario__nombre = "Juan Pérez"
        usuario_mock._Usuario__nombreDeUsuario = "jperez"
        usuario_mock._Usuario__email = email
        usuario_mock._Usuario__claustro = "estudiante"
        usuario_mock._Usuario__contraseña = "hashed_password"
        # Configuramos to_dict() para que devuelva lo que generaría la implementación real
        usuario_mock.to_dict.return_value = {
            "id": 1,
            "nombre": "Juan Pérez",
            "nombreDeUsuario": "jperez",
            "email": email,
            "claustro": "estudiante",
            "contraseña": "hashed_password"
        }
        self.repo_mock.obtener_registro_por_filtro.return_value = usuario_mock
        # Simulamos check_password_hash para que devuelva True
        with patch('modules.gestorUsuarios.check_password_hash') as mock_check_password:
            mock_check_password.return_value = True

            # Act
            resultado = self.gestor.autenticar_usuario(email, password)

            # Assert
            self.repo_mock.obtener_registro_por_filtro.assert_called_once_with("email", email)
            mock_check_password.assert_called_once_with("hashed_password", password)
            self.assertEqual(resultado, usuario_mock.to_dict.return_value)

if __name__ == '__main__':
    unittest.main()
