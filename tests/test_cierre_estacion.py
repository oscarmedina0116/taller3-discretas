import unittest
from src.grafos.grafo import Grafo, grafo_ciudad_prueba
from src.grafos.cierre_estacion import medir_impacto_cierre


class TestCierreEstacion(unittest.TestCase):
    def test_cierre_de_vertice_con_al_menos_cinco_pares(self):
        g = grafo_ciudad_prueba()
        pares = [
            ("Portal", "Terminal"),
            ("Portal", "Biblioteca"),
            ("Museo", "Terminal"),
            ("Calle26", "Hospital"),
            ("Parque", "Universidad"),
        ]
        resultados = medir_impacto_cierre(g, pares, vertice_a_cerrar="Centro")
        self.assertEqual(len(resultados), 5)
        for r in resultados:
            # despues del cierre, la distancia nunca puede ser menor que antes
            if r.distancia_despues != float("inf"):
                self.assertGreaterEqual(r.distancia_despues, r.distancia_antes)

    def test_detecta_desconexion_total(self):
        g = Grafo()
        g.agregar_arista("A", "B", 1)
        g.agregar_arista("B", "C", 1)
        # B es el unico puente entre A y C
        resultados = medir_impacto_cierre(g, [("A", "C")], vertice_a_cerrar="B")
        self.assertEqual(resultados[0].estado, "desconectado")
        self.assertEqual(resultados[0].distancia_despues, float("inf"))

    def test_sin_impacto_si_existe_ruta_alterna_igual_de_corta(self):
        g = Grafo()
        g.agregar_arista("A", "B", 1)
        g.agregar_arista("B", "C", 1)
        g.agregar_arista("A", "C", 2)  # ruta alterna con el mismo costo
        resultados = medir_impacto_cierre(g, [("A", "C")], vertice_a_cerrar="B")
        self.assertEqual(resultados[0].estado, "sin cambio")
        self.assertEqual(resultados[0].distancia_despues, 2)

    def test_cierre_de_arista_en_lugar_de_vertice(self):
        g = Grafo()
        g.agregar_arista("A", "B", 1)
        g.agregar_arista("B", "C", 1)
        resultados = medir_impacto_cierre(g, [("A", "C")], arista_a_cerrar=("A", "B"))
        # A sigue alcanzable por si sola pero ya no directamente hacia B
        self.assertEqual(resultados[0].distancia_despues, float("inf"))

    def test_error_si_no_se_indica_ningun_cierre_o_ambos(self):
        g = grafo_ciudad_prueba()
        with self.assertRaises(ValueError):
            medir_impacto_cierre(g, [("Portal", "Museo")])
        with self.assertRaises(ValueError):
            medir_impacto_cierre(
                g, [("Portal", "Museo")], vertice_a_cerrar="Centro", arista_a_cerrar=("Portal", "Museo")
            )


if __name__ == "__main__":
    unittest.main()
