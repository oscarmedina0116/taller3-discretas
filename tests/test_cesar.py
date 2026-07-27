import unittest
from src.cripto.cesar import cifrar, descifrar, fuerza_bruta


class TestCesar(unittest.TestCase):
    def test_ejemplo_del_enunciado(self):
        self.assertEqual(cifrar("HOLA UNAL", 3), "KROD XQDO")

    def test_cifrar_y_descifrar_son_inversos(self):
        texto = "Matematicas Discretas 2026, taller #3!"
        for k in (0, 1, 5, 13, 25):
            self.assertEqual(descifrar(cifrar(texto, k), k), texto)

    def test_conserva_espacios_puntuacion_y_numeros(self):
        texto = "Hola, mundo 123!"
        cifrado = cifrar(texto, 4)
        # los caracteres que no son letras deben quedar identicos y en la misma posicion
        for original, c in zip(texto, cifrado):
            if not original.isalpha():
                self.assertEqual(original, c)

    def test_respeta_mayusculas_y_minusculas(self):
        cifrado = cifrar("AbC", 1)
        self.assertEqual(cifrado, "BcD")

    def test_fuerza_bruta_encuentra_el_desplazamiento_correcto(self):
        original = "ATAQUE AL AMANECER"
        k_real = 11
        cifrado = cifrar(original, k_real)
        candidatos = fuerza_bruta(cifrado)
        self.assertIn((k_real, original), candidatos)
        self.assertEqual(len(candidatos), 26)


if __name__ == "__main__":
    unittest.main()
