"""
RSA de juguete (Ejercicio 2). SOLO CON FINES EDUCATIVOS: los primos usados
en un RSA real tienen cientos de digitos; aqui se usan primos pequenos para
poder seguir el calculo a mano.

Idea matematica:
  - Se eligen dos primos p, q y se define n = p*q.
  - phi(n) = (p-1)(q-1) es la cantidad de enteros en [1, n-1] coprimos con n
    (funcion totiente de Euler, para n producto de dos primos distintos).
  - Se elige un exponente publico e tal que gcd(e, phi(n)) = 1: eso garantiza
    que e tiene inverso multiplicativo modulo phi(n).
  - d = e^-1 mod phi(n) se calcula con el algoritmo de Euclides extendido,
    que ademas de gcd(a, b) entrega x, y tales que a*x + b*y = gcd(a, b).
  - Cifrado:   C = M^e mod n
  - Descifrado: M = C^d mod n
  Esto funciona por el teorema de Euler: como e*d = 1 (mod phi(n)),
  existe un entero t con e*d = 1 + t*phi(n), y entonces
  C^d = M^(e*d) = M^(1 + t*phi(n)) = M * (M^phi(n))^t = M (mod n),
  usando M^phi(n) = 1 (mod n) cuando gcd(M, n) = 1.
"""

from dataclasses import dataclass


def es_primo(n: int) -> bool:
    """Prueba de primalidad por division simple (suficiente para primos de juguete)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def euclides_extendido(a: int, b: int) -> tuple[int, int, int]:
    """
    Devuelve (g, x, y) tales que a*x + b*y = g = gcd(a, b).
    Version iterativa del algoritmo de Euclides extendido.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    # old_r = gcd, old_s / old_t son los coeficientes de Bezout para a y b
    return old_r, old_s, old_t


def inverso_modular(e: int, m: int) -> int:
    """Calcula e^-1 mod m usando Euclides extendido. Lanza ValueError si no existe."""
    g, x, _ = euclides_extendido(e, m)
    if g != 1:
        raise ValueError(f"gcd(e={e}, phi(n)={m}) = {g} != 1: e no tiene inverso modular")
    return x % m


@dataclass
class LlavesRSA:
    p: int
    q: int
    n: int
    phi: int
    e: int
    d: int


def generar_llaves(p: int, q: int, e: int) -> LlavesRSA:
    """Genera n, phi(n) y el exponente privado d a partir de p, q, e."""
    if not (es_primo(p) and es_primo(q)):
        raise ValueError("p y q deben ser primos")
    if p == q:
        raise ValueError("p y q deben ser primos distintos")

    n = p * q
    phi = (p - 1) * (q - 1)

    if not (1 < e < phi):
        raise ValueError(f"e debe cumplir 1 < e < phi(n)={phi}")

    g, _, _ = euclides_extendido(e, phi)
    if g != 1:
        raise ValueError(f"e={e} no es valido: gcd(e, phi(n)) = {g} != 1")

    d = inverso_modular(e, phi)
    return LlavesRSA(p=p, q=q, n=n, phi=phi, e=e, d=d)


def cifrar(m: int, e: int, n: int) -> int:
    if not (0 <= m < n):
        raise ValueError(f"El mensaje M debe cumplir 0 <= M < n={n}")
    return pow(m, e, n)


def descifrar(c: int, d: int, n: int) -> int:
    return pow(c, d, n)


def _demo():
    llaves = generar_llaves(p=61, q=53, e=17)
    print(f"n = {llaves.n} (esperado 3233)")
    print(f"phi(n) = {llaves.phi} (esperado 3120)")
    print(f"d = {llaves.d} (esperado 2753)")

    M = 65
    C = cifrar(M, llaves.e, llaves.n)
    print(f"C = {C} (esperado 2790)")

    M_recuperado = descifrar(C, llaves.d, llaves.n)
    print(f"M descifrado = {M_recuperado} (esperado 65)")


if __name__ == "__main__":
    _demo()
