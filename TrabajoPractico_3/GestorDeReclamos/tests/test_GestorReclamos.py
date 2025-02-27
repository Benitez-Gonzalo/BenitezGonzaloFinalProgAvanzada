import unittest
from unittest.mock import MagicMock
from modules.gestorReclamos import GestorDeReclamos, Reclamo  # Ajusta los nombres según tu proyecto

class TestGestorDeReclamos(unittest.TestCase):
    def test_obtener_tiempos_por_departamento_devuelve_tiempos_correctos(self):
        # Arrange
        # Creamos un mock para el repositorio
        repo_mock = MagicMock()
        
        # Creamos reclamos de prueba con tiempos
        reclamo1 = Reclamo(1, "Problema PC", "soporte informático", "en proceso", "2023-01-01", 1, 5, 4)
        reclamo2 = Reclamo(2, "Falla red", "soporte informático", "resuelto", "2023-01-02", 2, None, 6)
        reclamo3 = Reclamo(3, "Otro", "soporte informático", "pendiente", "2023-01-03", 3, 7, None)

        # Configuramos el mock para devolver una lista de reclamos específicos
        repo_mock.obtener_registros_por_filtro.return_value = [reclamo1, reclamo2, reclamo3]

        # Instanciamos el SUT con el mock
        gestor = GestorDeReclamos(repo_mock)

        # Act
        tiempos_estimados, tiempos_ocupados = gestor.obtener_tiempos_por_departamento("soporte informático")

        # Assert
        # Verificamos que las listas devueltas sean correctas según los datos simulados
        self.assertEqual(tiempos_estimados, [5, 7])  # Solo los tiempos no nulos
        self.assertEqual(tiempos_ocupados, [4, 6])   # Solo los tiempos no nulos
        # Verificamos que el método del mock fue llamado con los argumentos correctos
        repo_mock.obtener_registros_por_filtro.assert_called_once_with('clasificacion', 'soporte informático')

if __name__ == '__main__':
    unittest.main()