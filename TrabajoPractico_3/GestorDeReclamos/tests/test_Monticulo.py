import unittest
from unittest.mock import MagicMock
from modules.monticuloMediana import MonticuloMediana, MonticuloMax, MonticuloMin  

class TestMonticuloMediana(unittest.TestCase):
    def test_insertar_primer_valor_actualiza_mediana(self):
        # Arrange
        # Creamos mocks para los montículos internos
        max_heap_mock = MagicMock(spec=MonticuloMax)
        min_heap_mock = MagicMock(spec=MonticuloMin)

        # Configuramos el comportamiento inicial de los mocks
        max_heap_mock.tamano.return_value = 0
        min_heap_mock.tamano.return_value = 0
        max_heap_mock.raiz.return_value = 5  # Para cuando se necesite la raíz después

        # Instanciamos MonticuloMediana con los mocks
        monticulo = MonticuloMediana()
        monticulo._MonticuloMediana__max_heap = max_heap_mock  # Acceso privado para inyectar mock
        monticulo._MonticuloMediana__min_heap = min_heap_mock

        # Act
        monticulo.insertar(5)

        # Assert
        # Verificamos que se llamó a insertar en max_heap con el valor correcto
        max_heap_mock.insertar.assert_called_once_with(5)
        # Verificamos que no se llamó a min_heap (primer valor va a max_heap)
        min_heap_mock.insertar.assert_not_called()
        # Verificamos que la mediana se actualizó correctamente
        self.assertEqual(monticulo._MonticuloMediana__mediana, 5)
        # Verificamos que no se intentó balancear (solo un elemento)
        max_heap_mock.extraer_raiz.assert_not_called()
        min_heap_mock.extraer_raiz.assert_not_called()

    def test_insertar_balancea_monticulos(self):
        # Arrange
        max_heap_mock = MagicMock(spec=MonticuloMax)
        min_heap_mock = MagicMock(spec=MonticuloMin)

        # Configuración comportamiento para tamano
        max_heap_mock.tamano.side_effect = [1, 2, 1]  # Tamaños: 1 (inicio), 2 (tras insertar), 1 (tras balanceo)
        min_heap_mock.tamano.side_effect = [0, 1]     # Tamaños: 0 (inicio), 1 (tras balanceo)

        # Configuración extraer_raiz y raiz
        max_heap_mock.extraer_raiz.return_value = 5   # Extraemos 5 de max_heap
        max_heap_mock.raiz.return_value = 3           # Raíz final de max_heap
        min_heap_mock.raiz.return_value = 5           # Raíz final de min_heap

        monticulo = MonticuloMediana()
        monticulo._MonticuloMediana__max_heap = max_heap_mock
        monticulo._MonticuloMediana__min_heap = min_heap_mock
        monticulo._MonticuloMediana__mediana = 5      # Estado inicial

        # Act
        monticulo.insertar(3)  # Insertamos 3

        # Assert
        max_heap_mock.insertar.assert_called_once_with(3)  # Se inserta 3 en max_heap (por ser menor que la mediana, que es 5, se inserta en max_heap)
        max_heap_mock.extraer_raiz.assert_called_once()    # Se extrae 5 (por ser mayor a uno la diferencia entre números de elementos en los montículos)
        min_heap_mock.insertar.assert_called_once_with(5)  # Se inserta 5 en min_heap
        self.assertEqual(monticulo._MonticuloMediana__mediana, 4)  # Mediana: (3 + 5) / 2 (la mediana es el promedio porque los dos montículos tienen la misma cantidad de elementos)
        
    def test_obtener_mediana_devuelve_no_hay_datos_cuando_vacio(self):
        # Arrange
        max_heap_mock = MagicMock(spec=MonticuloMax)
        min_heap_mock = MagicMock(spec=MonticuloMin)

        # Simulamos montículos vacíos
        max_heap_mock.tamano.return_value = 0
        min_heap_mock.tamano.return_value = 0

        monticulo = MonticuloMediana()
        monticulo._MonticuloMediana__max_heap = max_heap_mock
        monticulo._MonticuloMediana__min_heap = min_heap_mock

        # Act
        resultado = monticulo.obtener_mediana()

        # Assert
        self.assertEqual(resultado,"No hay datos")
        max_heap_mock.tamano.assert_called_once()
        min_heap_mock.tamano.assert_called_once()

    def test_obtener_mediana_devuelve_valor_correcto(self):
        # Arrange
        max_heap_mock = MagicMock(spec=MonticuloMax)
        min_heap_mock = MagicMock(spec=MonticuloMin)

        # Simulamos un estado con elementos
        max_heap_mock.tamano.return_value = 1
        min_heap_mock.tamano.return_value = 0  # No se usa
        monticulo = MonticuloMediana()
        monticulo._MonticuloMediana__max_heap = max_heap_mock
        monticulo._MonticuloMediana__min_heap = min_heap_mock
        monticulo._MonticuloMediana__mediana = 5  # Simulamos una mediana previa

        # Act
        resultado = monticulo.obtener_mediana()

        # Assert
        self.assertEqual(resultado, 5)  # La mediana sigue siendo 5
        max_heap_mock.tamano.assert_called_once()  # Se llama porque se evalúa primero
        min_heap_mock.tamano.assert_not_called()  # No se llama

if __name__ == '__main__':
    unittest.main()