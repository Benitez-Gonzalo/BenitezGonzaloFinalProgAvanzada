import unittest
from modules import CintaTransp as CT
from modules.Detector import DetectorAlimento as D
from modules import CajonDeAlimentos as CA

class TestCintaTransportadora(unittest.TestCase):

    def setUp(self):
        self.Cinta = CT.CintaTransportadora()
        self.cajon = CA.CajonDeAlimento()
    
    def test_getAlimentos(self):
        CantAlimentos = 8
        cont = 0 
        while (cont<CantAlimentos):
            alimento=self.Cinta.transportarAlimentos()
            if alimento != None : 
                self.cajon.agregar_alimento(alimento)
                cont+=1 
        self.assertEqual(len(self.cajon), CantAlimentos)

if __name__ == '__main__':
    unittest.main()