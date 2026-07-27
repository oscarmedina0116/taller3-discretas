import unittest
from src.boole.simplificacion import simplificar, verificar_equivalencia, tabla_desde_minterminos


class TestSimplificacionBooleana(unittest.TestCase):
    def test_caso_sugerido_del_enunciado(self):
        # minterminos {1,3,5,7} en 3 variables (A,B,C): todos tienen C=1,
        # asi que la funcion simplificada debe ser equivalente a "C".
        minterminos = [1, 3, 5, 7]
        simplificada = simplificar(minterminos, n_vars=3)
        self.assertTrue(verificar_equivalencia(minterminos, 3, simplificada))
        # con solo C en la expresion, se comporta igual para cualquier A,B
        self.assertIn("C", simplificada)
        self.assertNotIn("NOT C", simplificada)

    def test_funcion_de_cuatro_variables(self):
        minterminos = [0, 1, 2, 3, 8, 9, 10, 11]  # no depende de C
        simplificada = simplificar(minterminos, n_vars=4)
        self.assertTrue(verificar_equivalencia(minterminos, 4, simplificada))

    def test_funcion_constante_falsa(self):
        self.assertEqual(simplificar([], n_vars=3), "0")
        self.assertEqual(tabla_desde_minterminos([], 3), [False] * 8)

    def test_funcion_constante_verdadera(self):
        minterminos = list(range(8))  # los 8 minterminos de 3 variables
        simplificada = simplificar(minterminos, n_vars=3)
        self.assertTrue(verificar_equivalencia(minterminos, 3, simplificada))

    def test_un_solo_mintermino(self):
        minterminos = [5]  # 101 -> A AND (NOT B) AND C
        simplificada = simplificar(minterminos, n_vars=3)
        self.assertTrue(verificar_equivalencia(minterminos, 3, simplificada))


if __name__ == "__main__":
    unittest.main()
