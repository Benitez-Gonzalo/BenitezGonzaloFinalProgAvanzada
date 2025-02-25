import unittest
from unittest.mock import Mock, ANY, MagicMock
from sqlalchemy.orm import Session
from modules.persistencia import RepositorioReclamosSQLAlchemy
from modules.persistencia import ModeloReclamo, ModeloUsuario, asociacion_usuarios_reclamos  
from modules.dominio import Reclamo
from datetime import datetime


class TestRepositorioReclamosSQLAlchemy(unittest.TestCase):

    def setUp(self):
        # Crear un Mock de la sesión SQLAlchemy
        self.mock_session = MagicMock(spec=Session)
        self.mock_session.bind = Mock
        ModeloReclamo.metadata.create_all = Mock
        self.repositorio = RepositorioReclamosSQLAlchemy(self.mock_session)
        
    def test_obtener_reclamo_similar_sin_similares(self):
        # Arrange
        reclamo1 = ModeloReclamo(id=1, contenido='Se rompió una ventana del aula 7', clasificacion='secretaría técnica', id_usuario=1, fecha_de_creacion='2024-12-16 21:41:03.682176', estado='pendiente', tiempo_estimado=2, tiempo_ocupado=2)
        reclamo2 = ModeloReclamo(id=2, contenido='No anda el WiFi', clasificacion='secretaría técnica', id_usuario=1, fecha_de_creacion='2024-12-16 21:41:03.682178', estado='pendiente', tiempo_estimado=2, tiempo_ocupado=2)
        self.mock_session.query.return_value.all.return_value = [reclamo1, reclamo2]

        # Act
        resultado = self.repositorio.obtener_reclamo_similar('contenido', 'nuevo reclamo')

        # Assert
        self.assertEqual(resultado,[])

    def test_obtener_reclamo_similar_con_similares(self):
        # Arrange
        reclamo1 = ModeloReclamo(id=1, contenido='reclamo similar', clasificacion='A', id_usuario=1, fecha_de_creacion='2023-01-01', estado='abierto', tiempo_estimado=2, tiempo_ocupado=2)
        reclamo2 = ModeloReclamo(id=2, contenido='otro reclamo', clasificacion='B', id_usuario=2, fecha_de_creacion='2023-01-02', estado='cerrado', tiempo_estimado=2, tiempo_ocupado=2)
        self.mock_session.query.return_value.all.return_value = [reclamo1, reclamo2]

        # Act
        resultado = self.repositorio.obtener_reclamo_similar('contenido', 'reclamo similar')

        # Assert
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].contenido, 'reclamo similar')
    

    def test_contar_adheridos_por_reclamo(self):
        """Prueba que contar_adheridos_por_reclamo retorna el conteo correcto."""

        # Crear un mock para la query
        mock_query = self.mock_session.query.return_value
        mock_join = mock_query.join.return_value
        mock_group_by = mock_join.group_by.return_value

        # Simular el resultado de 'all' después de encadenar los métodos
        mock_group_by.all.return_value = [
            (1, 3),  # Reclamo con ID 1 tiene 3 adheridos
            (2, 5),  # Reclamo con ID 2 tiene 5 adheridos
        ]

        # Llamar al método
        resultado = self.repositorio.contar_adheridos_por_reclamo()

        # Verificar el resultado esperado
        self.assertEqual(resultado, {1: 3, 2: 5})

        # Verificar que los métodos encadenados se llamaron correctamente
        self.mock_session.query.assert_called_once_with(ModeloReclamo.id, ANY)
        mock_query.join.assert_called_once_with(asociacion_usuarios_reclamos, ANY)
        mock_join.group_by.assert_called_once_with(ModeloReclamo.id)


    def test_guardar_reclamo(self):
        """Prueba que guardar_reclamo agrega un reclamo y actualiza al usuario."""

        # Configurar mocks
        mock_usuario = Mock(spec=ModeloUsuario)
        mock_usuario.reclamos_seguidos = []  # Simular la lista reclamos_seguidos

        mock_reclamo_entidad = Reclamo(
            p_id_reclamo=None,
            pContenido="Test Reclamo",
            pDepartamento="Soporte",
            pEstado="Pendiente",
            pFechayHora=datetime.now(),
            pId_usuario=1,
            pTiempoEstimado=2,
            pTiempoOcupado=2
        )

        # Simular la sesión para el query
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = mock_usuario

        # Simular el mapeo de entidad a modelo
        self.repositorio._RepositorioReclamosSQLAlchemy__map_entidad_a_modelo = Mock()
        mock_modelo_reclamo = Mock(spec=ModeloReclamo)
        self.repositorio._RepositorioReclamosSQLAlchemy__map_entidad_a_modelo.return_value = mock_modelo_reclamo

        # Llamar al método
        self.repositorio.guardar_reclamo(mock_reclamo_entidad)

        # Verificar que se llamó a `add` con el modelo de reclamo
        self.mock_session.add.assert_called_once_with(mock_modelo_reclamo)

        # Verificar que se llamó a `commit`
        self.mock_session.commit.assert_called_once()

        # Verificar que el usuario sigue el reclamo
        self.assertIn(mock_modelo_reclamo, mock_usuario.reclamos_seguidos)

        # Verificar que el método privado de mapeo se llamó correctamente
        self.repositorio._RepositorioReclamosSQLAlchemy__map_entidad_a_modelo.assert_called_once_with(mock_reclamo_entidad)
        




if __name__ == '__main__':
    unittest.main()
