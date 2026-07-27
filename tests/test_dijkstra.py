import unittest
from src.grafos.grafo import Grafo, grafo_ciudad_prueba
from src.grafos.dijkstra import dijkstra, ruta_mas_corta


class TestDijkstra(unittest.TestCase):
    def test_grafo_de_prueba_cumple_el_minimo_pedido(self):
        g = grafo_ciudad_prueba()
        self.assertGreaterEqual(len(g.vertices()), 8)
        self.assertGreaterEqual(g.num_aristas(), 12)

    def test_distancia_a_si_mismo_es_cero(self):
        g = grafo_ciudad_prueba()
        distancias, _ = dijkstra(g, "Portal")
        self.assertEqual(distancias["Portal"], 0)

    def test_ruta_mas_corta_es_consistente_con_la_suma_de_pesos(self):
        g = grafo_ciudad_prueba()
        distancia, camino = ruta_mas_corta(g, "Portal", "Terminal")
        self.assertEqual(camino[0], "Portal")
        self.assertEqual(camino[-1], "Terminal")
        peso_acumulado = sum(
            g.vecinos(camino[i])[camino[i + 1]] for i in range(len(camino) - 1)
        )
        self.assertEqual(peso_acumulado, distancia)

    def test_grafo_pequeno_con_solucion_conocida_a_mano(self):
        g = Grafo()
        g.agregar_arista("A", "B", 1)
        g.agregar_arista("B", "C", 2)
        g.agregar_arista("A", "C", 10)
        distancia, camino = ruta_mas_corta(g, "A", "C")
        self.assertEqual(distancia, 3)  # A->B->C (1+2) es mejor que A->C directo (10)
        self.assertEqual(camino, ["A", "B", "C"])

    def test_vertice_inalcanzable_da_distancia_infinita(self):
        g = Grafo()
        g.agregar_arista("A", "B", 1)
        g.agregar_vertice("Z")  # sin conexiones
        distancia, camino = ruta_mas_corta(g, "A", "Z")
        self.assertEqual(distancia, float("inf"))
        self.assertEqual(camino, [])

    def test_pesos_negativos_no_permitidos(self):
        g = Grafo()
        with self.assertRaises(ValueError):
            g.agregar_arista("A", "B", -5)


if __name__ == "__main__":
    unittest.main()
