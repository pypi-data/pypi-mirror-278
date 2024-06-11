import unittest
from DetectaMovCamara import DetectaMovCamara

class TestDetectaMovCamara(unittest.TestCase):
    def setUp(self):
        self.detector = DetectaMovCamara()
    def test_detectarMovimiento(self):
        # Ejecutar la función a probar
        try:
            resultados = []
            #self.detector.mostrarCamara()
            self.detector.detectarMovimiento(resultados)
        except Exception as e:
            self.fail(f'detectarMovimiento raised Exception unexpectedly: {e}')

if __name__ == '__main__':
    unittest.main()