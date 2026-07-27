"""
Cifrado Cesar (Ejercicio 1).

Idea matematica: el alfabeto A..Z se identifica con Z_26 = {0, 1, ..., 25}.
Cifrar una letra con desplazamiento k es la funcion f(x) = (x + k) mod 26.
Como f es una biyeccion de Z_26 en Z_26, existe una funcion inversa
f^-1(y) = (y - k) mod 26, que es exactamente el descifrado. Por eso
descifrar "deshace" el cifrado usando el desplazamiento contrario (-k).

Los caracteres que no son letras A-Z (espacios, numeros, puntuacion) se
dejan intactos: no pertenecen al alfabeto Z_26 sobre el que actua la
funcion, asi que no tiene sentido desplazarlos.
"""

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = len(ALFABETO)  # 26


def _desplazar_letra(letra: str, k: int) -> str:
    """Aplica f(x) = (x + k) mod 26 a una sola letra, conservando mayus/minus."""
    if letra.isupper():
        origen = ord("A")
    elif letra.islower():
        origen = ord("a")
    else:
        return letra  # no es una letra del alfabeto latino: se conserva igual

    x = ord(letra) - origen
    y = (x + k) % N
    return chr(y + origen)


def cifrar(texto: str, k: int) -> str:
    """Cifra `texto` desplazando cada letra k posiciones (k puede ser negativo)."""
    return "".join(_desplazar_letra(c, k) for c in texto)


def descifrar(texto: str, k: int) -> str:
    """Descifra usando el desplazamiento contrario: f^-1(y) = (y - k) mod 26."""
    return cifrar(texto, -k)


def fuerza_bruta(texto_cifrado: str) -> list[tuple[int, str]]:
    """
    Prueba los 26 posibles desplazamientos y devuelve la lista
    (k, texto_descifrado) para que una persona revise cual tiene sentido.

    Esto es posible porque el espacio de llaves de Cesar es minusculo
    (solo 26 valores), a diferencia de un cifrado con una llave grande.
    """
    return [(k, descifrar(texto_cifrado, k)) for k in range(N)]


def _demo():
    texto = "HOLA UNAL"
    k = 3
    c = cifrar(texto, k)
    print(f"Texto original:   {texto}")
    print(f"Cifrado (k={k}):    {c}")
    print(f"Descifrado:       {descifrar(c, k)}")
    print("\nFuerza bruta sobre el cifrado:")
    for despl, candidato in fuerza_bruta(c):
        print(f"  k={despl:2d}: {candidato}")


if __name__ == "__main__":
    _demo()
