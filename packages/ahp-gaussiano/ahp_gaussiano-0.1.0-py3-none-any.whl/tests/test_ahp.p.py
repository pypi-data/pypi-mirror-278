import unittest
import pandas as pd
from ahp_gaussiano import calcular_ahp_gaussiano

class TestAHPGaussiano(unittest.TestCase):
    def test_ahp_gaussiano(self):
        positivos = pd.DataFrame({
            'Jogos': [10, 15],
            'Passe certo': [80, 90],
            'Finalização certa': [5, 10]
        })

        negativos = pd.DataFrame({
            'Falta cometida': [3, 2],
            'Perda da posse de bola': [5, 8],
            'Finalização errada': [1, 3]
        })

        resultado = calcular_ahp_gaussiano(positivos, negativos)
        self.assertEqual(len(resultado), 2)

if __name__ == '__main__':
    unittest.main()
