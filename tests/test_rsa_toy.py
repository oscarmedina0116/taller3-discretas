import unittest
from src.cripto.rsa_toy import (
    generar_llaves, cifrar, descifrar, euclides_extendido, inverso_modular, es_primo
)


class TestRSAJuguete(unittest.TestCase):
    def test_caso_obligatorio_del_enunciado(self):
        llaves = generar_llaves(p=61, q=53, e=17)
        self.assertEqual(llaves.n, 3233)
        self.assertEqual(llaves.phi, 3120)
        self.assertEqual(llaves.d, 2753)

        M = 65
        C = cifrar(M, llaves.e, llaves.n)
        self.assertEqual(C, 2790)
        self.assertEqual(descifrar(C, llaves.d, llaves.n), 65)

    def test_ciclo_cifrado_descifrado_con_otras_llaves(self):
        llaves = generar_llaves(p=13, q=17, e=7)
        for M in (0, 1, 42, 100, llaves.n - 1):
            C = cifrar(M, llaves.e, llaves.n)
            self.assertEqual(descifrar(C, llaves.d, llaves.n), M)

    def test_e_invalido_lanza_error(self):
        # phi(3*11)=20; e=4 comparte factor 2 con 20 => gcd != 1
        with self.assertRaises(ValueError):
            generar_llaves(p=3, q=11, e=4)

    def test_euclides_extendido_identidad_de_bezout(self):
        a, b = 240, 46
        g, x, y = euclides_extendido(a, b)
        self.assertEqual(g, 2)
        self.assertEqual(a * x + b * y, g)

    def test_inverso_modular_correcto(self):
        e, m = 17, 3120
        d = inverso_modular(e, m)
        self.assertEqual((e * d) % m, 1)

    def test_es_primo(self):
        self.assertTrue(es_primo(61))
        self.assertTrue(es_primo(53))
        self.assertFalse(es_primo(1))
        self.assertFalse(es_primo(51))  # 51 = 3*17


if __name__ == "__main__":
    unittest.main()
