import unittest
from unittest.mock import MagicMock
from modules.gestorEstadistico import GestorEstadistico
from modules.dominio import Reclamo
from datetime import datetime

class TestGestorEstadistico(unittest.TestCase):
    def setUp(self):
        # Creamos un mock para el repositorio de reclamos
        self.repo_mock = MagicMock()
        # Instanciamos GestorEstadistico con el mock
        self.gestor = GestorEstadistico(self.repo_mock)

    def test_obtenerDatosPieChart_sin_filtro(self):
        """Verifica que calcula correctamente los porcentajes sin filtro de departamento."""
        # Arrange
        reclamo1 = Reclamo(1,"Problema con PC","soporte informático","en proceso",datetime(2023, 1, 1),1,5,None)
        reclamo2 = Reclamo(2,"Falla de red","soporte informático","pendiente",datetime(2023, 1, 2),2,3,None)
        reclamo3 = Reclamo(3,"Limpieza necesaria","maestranza","resuelto",datetime(2023, 1, 3),3,2,2)
        reclamo4 = Reclamo(
            p_id_reclamo=4,
            pContenido="Reclamo inválido",
            pDepartamento="soporte",
            pEstado="inválido",
            pFechayHora=datetime(2023, 1, 4),
            pId_usuario=4,
            pTiempoEstimado=None,
            pTiempoOcupado=None
        )
        self.repo_mock.obtener_todos_los_registros.return_value = [reclamo1, reclamo2, reclamo3, reclamo4]

        # Act
        porcentajes = self.gestor.obtenerDatosPieChart()

        # Assert
        expected = [25.0, 25.0, 25.0, 25.0]  # en_proceso, inválidos, pendientes, resueltos
        self.assertEqual(porcentajes, expected)
        self.repo_mock.obtener_todos_los_registros.assert_called_once()
        
    def test_obtenerDatosPieChart_con_filtro_departamento(self):
        """Verifica que calcula correctamente los porcentajes filtrando por departamento."""
        # Arrange
        # Simulamos reclamos para el departamento "soporte"
        reclamo1 = Reclamo(1,"Problema con PC","soporte","en proceso",datetime(2023, 1, 1),1,5,None)
        reclamo2 = Reclamo(2,"Falla de red","soporte","pendiente",datetime(2023, 1, 2),2,3,None)
        # Simulamos un reclamo de otro departamento (no debería incluirse)
        reclamo3 = Reclamo(3,"Limpieza necesaria","maestranza","resuelto",datetime(2023, 1, 3),3,2,2)
        # Configuramos el mock para devolver solo los reclamos de "soporte"
        self.repo_mock.obtener_registros_por_filtro.return_value = [reclamo1, reclamo2]

        # Act
        porcentajes = self.gestor.obtenerDatosPieChart(departamento="soporte informático")

        # Assert
        # Total: 2 reclamos -> en proceso: 1 (50%), pendientes: 1 (50%), inválidos: 0 (0%), resueltos: 0 (0%)
        expected = [50.0, 0.0, 50.0, 0.0]  # [en_proceso, inválidos, pendientes, resueltos]
        self.assertEqual(porcentajes, expected)
        # Verificamos que se llamó al método correcto del repositorio
        self.repo_mock.obtener_registros_por_filtro.assert_called_once_with('clasificacion', 'soporte informático')
        # Aseguramos que no se usó obtener_todos_los_registros
        self.repo_mock.obtener_todos_los_registros.assert_not_called()

if __name__ == '__main__':
    unittest.main()