import unittest
import random
from src.cuantica.qubit_simulador import (
    aplicar_compuerta, probabilidades, simular_mediciones, X, Z, H, KET_0, KET_1
)


class TestQubitSimulador(unittest.TestCase):
    def test_x_sobre_ket0_da_ket1(self):
        resultado = aplicar_compuerta(X, KET_0)
        self.assertAlmostEqual(resultado[0].real, 0.0)
        self.assertAlmostEqual(resultado[1].real, 1.0)

    def test_h_sobre_ket0_da_probabilidades_50_50(self):
        estado = aplicar_compuerta(H, KET_0)
        p0, p1 = probabilidades(estado)
        self.assertAlmostEqual(p0, 0.5, places=6)
        self.assertAlmostEqual(p1, 0.5, places=6)

    def test_hh_sobre_ket0_regresa_a_ket0(self):
        estado = aplicar_compuerta(H, KET_0)
        estado_final = aplicar_compuerta(H, estado)
        self.assertAlmostEqual(estado_final[0].real, 1.0, places=6)
        self.assertAlmostEqual(estado_final[1].real, 0.0, places=6)

    def test_probabilidades_de_ket0_y_ket1_puros(self):
        p0, p1 = probabilidades(KET_0)
        self.assertEqual((p0, p1), (1.0, 0.0))
        p0, p1 = probabilidades(KET_1)
        self.assertEqual((p0, p1), (0.0, 1.0))

    def test_z_deja_ket0_intacto_pero_cambia_signo_de_ket1(self):
        self.assertEqual(aplicar_compuerta(Z, KET_0), KET_0)
        estado = aplicar_compuerta(Z, KET_1)
        self.assertAlmostEqual(estado[1].real, -1.0)

    def test_simulacion_de_1000_mediciones_de_ket1_da_siempre_1(self):
        conteos = simular_mediciones(KET_1, n=1000)
        self.assertEqual(conteos[1], 1000)
        self.assertEqual(conteos[0], 0)

    def test_simulacion_de_1000_mediciones_de_h_ket0_es_cercana_a_50_50(self):
        random.seed(42)
        estado = aplicar_compuerta(H, KET_0)
        conteos = simular_mediciones(estado, n=1000)
        self.assertEqual(conteos[0] + conteos[1], 1000)
        # margen amplio: con 1000 tiros la desviacion estandar es ~15.8
        self.assertTrue(400 <= conteos[0] <= 600)


if __name__ == "__main__":
    unittest.main()
