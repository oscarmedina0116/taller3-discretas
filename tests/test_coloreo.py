import unittest
from src.grafos.coloreo import (
    GrafoConflictos, coloreo_voraz, es_coloreo_valido, agrupar_por_color, grafo_cursos_prueba
)


class TestColoreo(unittest.TestCase):
    def test_grafo_de_prueba_cumple_el_minimo_de_vertices(self):
        g = grafo_cursos_prueba()
        self.assertGreaterEqual(len(g.vertices()), 10)

    def test_coloreo_del_grafo_de_prueba_es_valido(self):
        g = grafo_cursos_prueba()
        color_de = coloreo_voraz(g)
        self.assertTrue(es_coloreo_valido(g, color_de))
        self.assertEqual(set(color_de.keys()), set(g.vertices()))

    def test_triangulo_necesita_exactamente_tres_colores(self):
        g = GrafoConflictos()
        g.agregar_arista("X", "Y")
        g.agregar_arista("Y", "Z")
        g.agregar_arista("X", "Z")
        color_de = coloreo_voraz(g)
        self.assertTrue(es_coloreo_valido(g, color_de))
        self.assertEqual(len(set(color_de.values())), 3)

    def test_grafo_vacio_de_aristas_usa_un_solo_color(self):
        g = GrafoConflictos()
        for v in ("Curso1", "Curso2", "Curso3"):
            g.agregar_vertice(v)
        color_de = coloreo_voraz(g)
        self.assertEqual(len(set(color_de.values())), 1)

    def test_deteccion_de_coloreo_invalido(self):
        g = GrafoConflictos()
        g.agregar_arista("A", "B")
        color_de_invalido = {"A": 0, "B": 0}  # adyacentes con el mismo color
        self.assertFalse(es_coloreo_valido(g, color_de_invalido))

    def test_agrupar_por_color(self):
        color_de = {"A": 0, "B": 1, "C": 0}
        grupos = agrupar_por_color(color_de)
        self.assertEqual(grupos[0], ["A", "C"])
        self.assertEqual(grupos[1], ["B"])


if __name__ == "__main__":
    unittest.main()
