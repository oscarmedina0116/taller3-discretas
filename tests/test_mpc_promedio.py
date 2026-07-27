import unittest
from src.cripto.mpc_promedio import (
    repartir_nota, repartir_notas, suma_parcial_servidor, reconstruir_suma, simular_protocolo
)


class TestMPCPromedio(unittest.TestCase):
    def test_ejemplo_del_enunciado(self):
        notas = [40, 35, 50, 25]
        suma, promedio = simular_protocolo(notas)
        self.assertEqual(suma, 150)
        self.assertEqual(promedio, 37.5)

    def test_una_nota_se_reconstruye_bien_muchas_veces(self):
        # se repite para confirmar que funciona con distintas partes aleatorias
        for nota in (0, 1, 25, 50):
            for _ in range(20):
                s1, s2, s3 = repartir_nota(nota, M=1000)
                self.assertEqual((s1 + s2 + s3) % 1000, nota)

    def test_lista_de_cualquier_tamano(self):
        notas = [10, 20, 30, 40, 50, 5, 15]
        suma, promedio = simular_protocolo(notas)
        self.assertEqual(suma, sum(notas))
        self.assertAlmostEqual(promedio, sum(notas) / len(notas))

    def test_partes_individuales_no_revelan_la_nota(self):
        # una parte sola, vista de forma aislada, debe poder tomar
        # practicamente cualquier valor en Z_M sin importar la nota real
        M = 1000003
        valores_vistos = {repartir_nota(30, M)[0] for _ in range(50)}
        self.assertGreater(len(valores_vistos), 40)  # alta variabilidad = no hay patron fijo

    def test_suma_parcial_por_servidor_y_reconstruccion(self):
        notas = [12, 8, 20]
        partes = repartir_notas(notas, M=1000003)
        self.assertEqual(len(partes), 3)
        sumas_parciales = [suma_parcial_servidor(p, M=1000003) for p in partes]
        self.assertEqual(reconstruir_suma(sumas_parciales, M=1000003), sum(notas))

    def test_nota_fuera_de_rango_lanza_error(self):
        with self.assertRaises(ValueError):
            repartir_nota(51)
        with self.assertRaises(ValueError):
            repartir_nota(-1)


if __name__ == "__main__":
    unittest.main()
