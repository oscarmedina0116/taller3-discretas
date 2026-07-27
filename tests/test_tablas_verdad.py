import unittest
from src.boole.tablas_verdad import evaluar, tabla_de_verdad, variables_usadas


class TestTablasVerdad(unittest.TestCase):
    def test_variables_usadas_no_confunde_letras_de_and_con_variables(self):
        # "AND" contiene 'A' y 'D': el extractor de variables no debe
        # inventarse una variable D que no aparece de verdad.
        self.assertEqual(variables_usadas("(A AND B) OR (NOT C)"), ["A", "B", "C"])

    def test_expresion_1_todas_las_combinaciones(self):
        expr = "(A AND B) OR (NOT C)"
        for a in (False, True):
            for b in (False, True):
                for c in (False, True):
                    esperado = (a and b) or (not c)
                    self.assertEqual(evaluar(expr, {"A": a, "B": b, "C": c}), esperado)

    def test_expresion_2_xor_and(self):
        expr = "(A XOR B) AND C"
        casos = [
            ({"A": True, "B": False, "C": True}, True),
            ({"A": True, "B": True, "C": True}, False),
            ({"A": False, "B": False, "C": True}, False),
            ({"A": True, "B": False, "C": False}, False),
        ]
        for valores, esperado in casos:
            self.assertEqual(evaluar(expr, valores), esperado)

    def test_expresion_3_or_and_or(self):
        expr = "(A OR B) AND (NOT A OR C)"
        casos = [
            ({"A": False, "B": True, "C": False}, True),
            ({"A": True, "B": False, "C": False}, False),
            ({"A": True, "B": False, "C": True}, True),
            ({"A": False, "B": False, "C": False}, False),
        ]
        for valores, esperado in casos:
            self.assertEqual(evaluar(expr, valores), esperado)

    def test_tabla_de_verdad_tiene_2_a_la_n_filas(self):
        tabla = tabla_de_verdad("(A AND B) OR (NOT C)")
        self.assertEqual(len(tabla), 8)  # 2^3 combinaciones para A, B, C

    def test_expresion_con_caracter_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            evaluar("A AND E", {"A": True, "E": True})


if __name__ == "__main__":
    unittest.main()
