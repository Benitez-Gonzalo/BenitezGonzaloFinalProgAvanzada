# Archivo de test para realizar pruebas unitarias del modulo1
import unittest
import numpy as np
from modules import CajonDeAlimentos
from modules import Alimentos
from modules import Calculadora
from modules import factoria

class TestKiwi(unittest.TestCase):

    def test_AwKiwi(self):
        
        kiwi = Alimentos.Kiwi(0.40)
        ResultadoCorrecto =( 0.96 * (1 - np.exp(-18 * 0.40)))/ (1 + np.exp(-18 * 0.40))
        
        ResultadoFuncion = kiwi.calcular_aw()
        
        self.assertAlmostEqual(ResultadoFuncion, ResultadoCorrecto, places=2)

class TestManzana(unittest.TestCase):

    def test_aw_manzana(self):

        Manzana = Alimentos.Manzana(0.30)      
        ResultadoFuncion = Manzana.calcular_aw()
        
        ResultadoCorrecto = 0.97 * ((15 * 0.30)**2) / (1 + (15 * 0.30)**2)
        
        self.assertAlmostEqual(ResultadoFuncion, ResultadoCorrecto, places=2)

class TestPapa(unittest.TestCase):

    def test_aw_papa(self):

        Papa = Alimentos.Papa(0.25)      
        ResultadoFuncion = Papa.calcular_aw()
        
        ResultadoCorrecto = 0.66 * np.arctan(18 * 0.25)
        self.assertAlmostEqual(ResultadoFuncion, ResultadoCorrecto, places=2)

class TestZanahoria(unittest.TestCase):

    def test_aw_zanahoria(self):

        Zanahoria = Alimentos.Zanahoria(20)
        ResultadoFuncion = Zanahoria.calcular_aw()
        
        ResultadoCorrecto = 0.96 * (1 - np.exp(-10 * 20))
        self.assertAlmostEqual(ResultadoFuncion, ResultadoCorrecto, places=2)
   
class TestCalculadora(unittest.TestCase):
     
    def setUp(self):
        AlimentosConPeso = [{'alimento':'zanahoria', "peso": 0.5},{'alimento' :'manzana', "peso" : 0.12},
                        {'alimento':'kiwi', "peso" : 0.45},{'alimento' : 'papa',"peso" : 0.45}, {'alimento' : 'zanahoria', "peso" : 0.03}, 
                        {'alimento' : 'manzana', "peso" : 0.03},{'alimento' :'kiwi', "peso" :0.01},{'alimento' :'papa', "peso" :0.35}]
        
        self.calculadora= Calculadora.Calculadora()
        self.Cajon = CajonDeAlimentos.CajonDeAlimento()
        for dicc in AlimentosConPeso : 
            alimento = factoria.crear_alimento(dicc)
            self.Cajon.agregar_alimento(alimento)
   
    def test_aw_promedio(self):
       
        aw=self.calculadora.aw_alimentos(self.Cajon)
        self.assertAlmostEqual(aw["aw_manzanas"], 0.45,places=3)
        self.assertAlmostEqual(aw["aw_kiwis"], 0.52,places=3)
        self.assertAlmostEqual(aw["aw_papas"], 0.94,places=3)
        self.assertAlmostEqual(aw["aw_zanahorias"], 0.6,places=3)
        self.assertAlmostEqual(aw["aw_frutas"], 0.49,places=3)
        self.assertAlmostEqual(aw["aw_verduras"], 0.77,places=3)
        self.assertAlmostEqual(aw["aw_total"], 0.63,places=3)

    def test_AwNoEsAceptable(self):
        aw=self.calculadora.aw_alimentos(self.Cajon)

        for Alim, Peso in aw.items():
            if self.calculadora.awNoEsAceptable(Peso):
                self.assertTrue(self.calculadora.awNoEsAceptable(Peso))

if __name__ == '__main__':
    unittest.main()