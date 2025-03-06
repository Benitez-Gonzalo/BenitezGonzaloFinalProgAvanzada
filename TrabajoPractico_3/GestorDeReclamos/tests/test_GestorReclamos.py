import unittest
from unittest.mock import MagicMock,patch
from datetime import datetime
from modules.gestorReclamos import GestorDeReclamos, Reclamo 

class TestGestorDeReclamos(unittest.TestCase):
    
    def setUp(self):
        self.repo_mock = MagicMock()
        self.gestor = GestorDeReclamos(self.repo_mock)
    
    def test_obtener_tiempos_por_departamento_devuelve_tiempos_correctos(self):
        # Arrange
        # Creamos un mock para el repositorio
        self.repo_mock = MagicMock()
        
        # Creamos reclamos de prueba con tiempos
        reclamo1 = Reclamo(1, "Problema PC", "soporte informático", "en proceso", "2023-01-01", 1, 5, 4)
        reclamo2 = Reclamo(2, "Falla red", "soporte informático", "resuelto", "2023-01-02", 2, None, 6)
        reclamo3 = Reclamo(3, "Otro", "soporte informático", "pendiente", "2023-01-03", 3, 7, None)

        # Configuramos el mock para devolver una lista de reclamos específicos
        self.repo_mock.obtener_registros_por_filtro.return_value = [reclamo1, reclamo2, reclamo3]

        # Instanciamos el SUT con el mock
        gestor = GestorDeReclamos(self.repo_mock)

        # Act
        tiempos_estimados, tiempos_ocupados = gestor.obtener_tiempos_por_departamento("soporte informático")

        # Assert
        # Verificamos que las listas devueltas sean correctas según los datos simulados
        self.assertEqual(tiempos_estimados, [5, 7])  # Solo los tiempos no nulos
        self.assertEqual(tiempos_ocupados, [4, 6])   # Solo los tiempos no nulos
        # Verificamos que el método del mock fue llamado con los argumentos correctos
        self.repo_mock.obtener_registros_por_filtro.assert_called_once_with('clasificacion', 'soporte informático')
        
    def test_creación_reclamo_exitoso(self):
        """Verifica que se crea y guarda un reclamo correctamente, incrementando el contador."""
        # Arrange
        clasificador_mock = MagicMock()
        self.repo_mock.obtener_todos_los_registros.return_value = []
        self.gestor._GestorDeReclamos__clasificador = clasificador_mock
        contenido = "Problema con mi computadora"
        id_usuario = "1"
        clasificacion_simulada = ["soporte informático"]
        clasificador_mock.clasificar_reclamo.return_value = clasificacion_simulada

        # Mockeamos datetime.now() en el módulo correcto
        fecha_fija = datetime(2023, 10, 15, 12, 0, 0)
        with patch('modules.gestorReclamos.datetime') as mock_datetime:
            mock_datetime.now.return_value = fecha_fija
                
            # Act
            self.gestor.creación_reclamo(contenido, id_usuario)

            # Assert
            clasificador_mock.clasificar_reclamo.assert_called_once_with(contenido)
            self.repo_mock.guardar_registro.assert_called_once()
            args, _ = self.repo_mock.guardar_registro.call_args
            reclamo_guardado = args[0]

            self.assertIsInstance(reclamo_guardado, Reclamo)
            self.assertEqual(reclamo_guardado.contenido, contenido)
            self.assertEqual(reclamo_guardado.departamento, "soporte informático")
            self.assertEqual(reclamo_guardado.estado, "pendiente")
            self.assertEqual(reclamo_guardado.fecha_y_hora, fecha_fija)
            self.assertEqual(reclamo_guardado.id_usuario, "1")
            self.assertEqual(reclamo_guardado.tiempo_estimado, 0)
            self.assertEqual(reclamo_guardado.tiempo_ocupado, 0)

            self.assertEqual(self.gestor._GestorDeReclamos__numero_reclamos, 1)
    
    def test_obtener_tiempos_devuelve_listas_correctas(self):
        """Verifica que devuelve listas correctas de tiempos estimados y ocupados."""
        # Arrange
        # Simulamos reclamos con tiempos estimados y ocupados
        self.repo_mock.obtener_todos_los_registros.return_value = []
        reclamo1 = Reclamo(1,"Problema con PC","soporte informático","en proceso",datetime(2023, 1, 1),1,5,None)
        reclamo2 = Reclamo(2,"Falla de red","soporte informático","resuelto",datetime(2023, 1, 2),2,3,2)
        reclamo3 = Reclamo(3,"Limpieza","maestranza","pendiente",datetime(2023, 1, 3),3,4,None)
        # Configuramos el mock para devolver los reclamos simulados
        self.repo_mock.obtener_todos_los_registros.return_value = [reclamo1, reclamo2, reclamo3]

        # Act
        tiempos_estimados, tiempos_ocupados = self.gestor.obtener_tiempos()

        # Assert
        # Esperamos: tiempos estimados = [5, 3, 4], tiempos ocupados = [None, 2, None]
        self.assertEqual(tiempos_estimados, [5, 3, 4])
        self.assertEqual(tiempos_ocupados, [None, 2, None])
        # Verificamos que se llamó al método del repositorio
        self.assertEqual(self.repo_mock.obtener_todos_los_registros.call_count,2)

if __name__ == '__main__':
    unittest.main()