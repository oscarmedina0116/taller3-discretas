import unittest
import math
from src.informacion.shannon import frecuencias, probabilidades, entropia, comparar


class TestShannon(unittest.TestCase):
    def test_texto_completamente_repetitivo_tiene_entropia_cero(self):
        self.assertEqual(entropia("AAAAAAAA"), 0.0)

    def test_dos_simbolos_equiprobables_da_entropia_uno(self):
        self.assertAlmostEqual(entropia("ABABABAB"), 1.0)

    def test_cuatro_simbolos_equiprobables_da_entropia_dos(self):
        self.assertAlmostEqual(entropia("ABCDABCD"), 2.0)

    def test_texto_variado_tiene_mayor_entropia_que_uno_repetitivo(self):
        repetitivo = "AAAAAAAAAAAAAAAA"
        variado = "el veloz murcielago hindu comia feliz cardillo y kiwi"
        self.assertGreater(entropia(variado), entropia(repetitivo))
        mensaje = comparar(repetitivo, variado)
        self.assertIn("segundo", mensaje)

    def test_probabilidades_suman_uno(self):
        probs = probabilidades("aabbbc")
        self.assertAlmostEqual(sum(probs.values()), 1.0)
        self.assertEqual(probs["b"], 0.5)

    def test_frecuencias_cuentan_bien(self):
        frecs = frecuencias("aabbbc")
        self.assertEqual(frecs["a"], 2)
        self.assertEqual(frecs["b"], 3)
        self.assertEqual(frecs["c"], 1)

    def test_texto_vacio_lanza_error(self):
        with self.assertRaises(ValueError):
            entropia("")


if __name__ == "__main__":
    unittest.main()
