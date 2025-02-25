import unittest
import heapq
from modules.servicio import MonticuloDeMediana  # Asumimos que la clase está en este archivo

class TestMonticuloDeMediana(unittest.TestCase):

    def setUp(self):
        """
        Configuración previa a cada test.
        """
        self.monticulo = MonticuloDeMediana()

    def test_insertar(self):
        """
        Test para verificar la inserción en el Montículo de Mediana.
        """

        # Caso 1: Insertar un único elemento
        # Arrange
        valor = 5

        # Act
        self.monticulo.insertar(valor)

        # Assert
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__max_heap), 1)
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__min_heap), 0)

        # Caso 2: Insertar un segundo elemento
        # Arrange
        valor = 7

        # Act
        self.monticulo.insertar(valor)

        # Assert
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__max_heap), 1)
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__min_heap), 1)

        # Caso 3: Insertar más elementos
        valores = [1, 6]
        for valor in valores:
            self.monticulo.insertar(valor)

        # Assert
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__max_heap), 2)
        self.assertEqual(len(self.monticulo._MonticuloDeMediana__min_heap), 2)

    def test_obtener_mediana(self):
        """
        Test para verificar el cálculo de la mediana en diferentes casos.
        """

        # Caso 1: Insertar y obtener mediana de un solo elemento
        # Arrange
        valor = 5

        # Act
        self.monticulo.insertar(valor)
        mediana = self.monticulo.obtener_mediana()

        # Assert
        self.assertEqual(mediana, 5)

        # Caso 2: Insertar más elementos y verificar medianas
        # Arrange
        valores = [7, 1, 6, 3, 8, 9]
        resultados_esperados = [6.0, 5, 5.5, 5, 5.5, 6]

        for i, valor in enumerate(valores):
            # Act
            self.monticulo.insertar(valor)
            mediana = self.monticulo.obtener_mediana()

            # Assert
            self.assertEqual(mediana, resultados_esperados[i])

if __name__ == "__main__":
    unittest.main()
