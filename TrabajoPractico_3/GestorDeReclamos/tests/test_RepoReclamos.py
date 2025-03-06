import unittest
from unittest.mock import MagicMock
from modules.persistencia import RepositorioReclamosSQLAlchemy 
from modules.dominio import Reclamo
from modules.modelos import ModeloReclamo,ModeloUsuario
from datetime import datetime

class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):
    def setUp(self):
        # Configuramos la sesión mockeada
        self.session_mock = MagicMock()
        self.repo = RepositorioReclamosSQLAlchemy(self.session_mock)

    def test_modificar_registro_exitoso(self):
        """Verifica que un reclamo existente se actualiza correctamente y devuelve True."""
        # Arrange
        # Creamos un objeto Reclamo para simular el reclamo modificado
        reclamo_modificado = Reclamo(1,"Problema con PC","soporte informático","en proceso","2023-01-01",2,5,None)

        # Creamos un mock para simular el registro existente en la base de datos
        registro_mock = MagicMock(spec=ModeloReclamo)
        registro_mock.id = 1  # Simulamos que coincide con el id_reclamo

        # Configuramos el mock de la sesión para devolver el registro simulado
        query_mock = MagicMock()
        query_mock.filter_by.return_value.first.return_value = registro_mock
        self.session_mock.query.return_value = query_mock

        # Act
        resultado = self.repo.modificar_registro(reclamo_modificado)

        # Assert
        # Verificamos que se buscó el registro por ID
        self.session_mock.query.assert_called_once_with(ModeloReclamo)
        query_mock.filter_by.assert_called_once_with(id=1)
        query_mock.filter_by.return_value.first.assert_called_once()

        # Verificamos que los atributos del registro se actualizaron correctamente
        self.assertEqual(registro_mock.clasificacion, "soporte informático")
        self.assertEqual(registro_mock.id_usuario, 2)
        self.assertEqual(registro_mock.fecha_de_creacion, "2023-01-01")
        self.assertEqual(registro_mock.estado, "en proceso")
        self.assertEqual(registro_mock.tiempo_estimado, 5)
        self.assertEqual(registro_mock.tiempo_ocupado, None)

        # Verificamos que se llamó a commit
        self.session_mock.commit.assert_called_once()

        # Verificamos que el método devuelve True
        self.assertTrue(resultado)
        
    def test_guardar_registro_exitoso(self):
        """Verifica que guarda un reclamo válido y asocia al usuario creador."""
        # Arrange
        # Creamos un objeto Reclamo válido
        reclamo = Reclamo(1,"Problema con PC","soporte informática","pendiente",datetime(2023, 1, 1),2,5,None)

        # Mock para el modelo_reclamo devuelto por __map_entidad_a_modelo
        modelo_reclamo_mock = MagicMock(spec=ModeloReclamo)
        self.repo._RepositorioReclamosSQLAlchemy__map_entidad_a_modelo = MagicMock(return_value=modelo_reclamo_mock)

        # Mock para el usuario encontrado
        usuario_mock = MagicMock(spec=ModeloUsuario)
        usuario_mock.reclamos_seguidos = MagicMock()  # Simulamos la lista de reclamos seguidos
        query_mock = MagicMock()
        query_mock.filter_by.return_value.first.return_value = usuario_mock
        self.session_mock.query.return_value = query_mock

        # Act
        self.repo.guardar_registro(reclamo)

        # Assert
        # Verificamos que se llamó a __map_entidad_a_modelo con el reclamo correcto
        self.repo._RepositorioReclamosSQLAlchemy__map_entidad_a_modelo.assert_called_once_with(reclamo)
        
        # Verificamos que se agregó el modelo_reclamo a la sesión
        self.session_mock.add.assert_called_once_with(modelo_reclamo_mock)

        # Verificamos la consulta para buscar al usuario
        self.session_mock.query.assert_called_once_with(ModeloUsuario)
        query_mock.filter_by.assert_called_once_with(id=2)
        query_mock.filter_by.return_value.first.assert_called_once()

        # Verificamos que el reclamo se asoció al usuario
        usuario_mock.reclamos_seguidos.append.assert_called_once_with(modelo_reclamo_mock)

        # Verificamos que se llamó a commit
        self.session_mock.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()