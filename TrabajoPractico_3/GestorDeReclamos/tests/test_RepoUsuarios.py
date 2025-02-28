import unittest
from unittest.mock import MagicMock
from modules.persistencia import RepositorioUsuariosSQLAlchemy
from modules.modelos import ModeloUsuario, ModeloReclamo, asociacion_usuarios_reclamos

class TestRepositorioUsuariosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.repo = RepositorioUsuariosSQLAlchemy(self.session_mock)

    def test_asociar_registro_exitoso(self):
        """Verifica que un usuario se asocia a un reclamo correctamente y devuelve True."""
        # Arrange
        id_usuario = 1
        id_reclamo = 2

        # Mock para la relación (no existe)
        relacion_query_mock = MagicMock()
        relacion_query_mock.filter_by.return_value.first.return_value = None

        # Mock para el usuario
        usuario_query_mock = MagicMock()
        usuario_mock = MagicMock(spec=ModeloUsuario)
        usuario_mock.id = id_usuario
        usuario_mock.reclamos_seguidos = MagicMock()  # Mockeamos reclamos_seguidos como un objeto rastreable
        usuario_query_mock.filter_by.return_value.first.return_value = usuario_mock

        # Mock para el reclamo
        reclamo_query_mock = MagicMock()
        reclamo_mock = MagicMock(spec=ModeloReclamo)
        reclamo_mock.id = id_reclamo
        reclamo_query_mock.filter_by.return_value.first.return_value = reclamo_mock

        # Configuramos las consultas con side_effect
        def query_side_effect(modelo):
            if modelo == asociacion_usuarios_reclamos:
                return relacion_query_mock
            elif modelo == ModeloUsuario:
                return usuario_query_mock
            elif modelo == ModeloReclamo:
                return reclamo_query_mock
            return MagicMock()

        self.session_mock.query.side_effect = query_side_effect

        # Act
        resultado = self.repo.asociar_registro(id_usuario, id_reclamo)

        # Assert
        self.session_mock.query.assert_any_call(asociacion_usuarios_reclamos)
        relacion_query_mock.filter_by.assert_called_once_with(user_id=1, claim_id=2)
        relacion_query_mock.filter_by.return_value.first.assert_called_once()

        self.session_mock.query.assert_any_call(ModeloUsuario)
        usuario_query_mock.filter_by.assert_called_once_with(id=1)
        usuario_query_mock.filter_by.return_value.first.assert_called_once()

        self.session_mock.query.assert_any_call(ModeloReclamo)
        reclamo_query_mock.filter_by.assert_called_once_with(id=2)
        reclamo_query_mock.filter_by.return_value.first.assert_called_once()

        # Verificamos la llamada a append en el mock de reclamos_seguidos
        usuario_mock.reclamos_seguidos.append.assert_called_once_with(reclamo_mock)

        self.session_mock.commit.assert_called_once()
        self.assertTrue(resultado)

if __name__ == '__main__':
    unittest.main()