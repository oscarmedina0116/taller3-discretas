"""
MPC basico: suma secreta con tres servidores (Ejercicio 3).

Idea matematica: para ocultar una nota x se usa un esquema de reparto
aditivo modulo M (una version simple de Secret Sharing). Se escogen al
azar s1, s2 en Z_M = {0, ..., M-1} y se define

    s3 = (x - s1 - s2) mod M

de modo que

    x = (s1 + s2 + s3) mod M.

Cada servidor recibe unicamente una de las tres partes de cada nota.
Como s1 y s2 son uniformemente aleatorias en Z_M, cada parte individual
(vista por separado) no da ninguna informacion sobre x: para cualquier
valor posible de x existe una eleccion de las otras dos partes que lo
explica igual de bien. Solo cuando se suman las TRES partes se recupera
el valor original.

Para agregar varias notas basta con sumar las partes componente a
componente (suma de shares = share de la suma), y al final cada servidor
revela solo su total parcial; la suma de esos tres totales parciales
(mod M) es la suma real de las notas.
"""

import random

MODULO_DEFECTO = 1_000_003


def repartir_nota(nota: int, M: int = MODULO_DEFECTO) -> tuple[int, int, int]:
    """Reparte una nota en 3 partes aleatorias modulo M tales que suman `nota` mod M."""
    if not (0 <= nota <= 50):
        raise ValueError("La nota debe estar entre 0 y 50")
    s1 = random.randrange(M)
    s2 = random.randrange(M)
    s3 = (nota - s1 - s2) % M
    return s1, s2, s3


def repartir_notas(notas: list[int], M: int = MODULO_DEFECTO):
    """
    Reparte una lista de notas entre 3 servidores.

    Devuelve una lista de 3 listas: partes_por_servidor[i] contiene la
    parte que le corresponde al servidor i de cada nota, en el mismo
    orden que `notas`. Ningun servidor ve la lista `notas` original.
    """
    partes_por_servidor = [[], [], []]
    for nota in notas:
        s1, s2, s3 = repartir_nota(nota, M)
        partes_por_servidor[0].append(s1)
        partes_por_servidor[1].append(s2)
        partes_por_servidor[2].append(s3)
    return partes_por_servidor


def suma_parcial_servidor(partes_servidor: list[int], M: int = MODULO_DEFECTO) -> int:
    """Cada servidor solo puede calcular la suma de las partes que recibio."""
    return sum(partes_servidor) % M


def reconstruir_suma(sumas_parciales: list[int], M: int = MODULO_DEFECTO) -> int:
    """Combina las 3 sumas parciales (una por servidor) para obtener la suma real."""
    return sum(sumas_parciales) % M


def simular_protocolo(notas: list[int], M: int = MODULO_DEFECTO) -> tuple[int, float]:
    """
    Corre el protocolo completo: reparte, calcula sumas parciales en cada
    servidor y reconstruye la suma y el promedio total.
    """
    partes_por_servidor = repartir_notas(notas, M)
    sumas_parciales = [suma_parcial_servidor(p, M) for p in partes_por_servidor]
    suma_total = reconstruir_suma(sumas_parciales, M)
    promedio = suma_total / len(notas)
    return suma_total, promedio


def _demo():
    notas = [40, 35, 50, 25]
    partes = repartir_notas(notas)
    print("Partes que ve cada servidor (no revelan las notas individuales):")
    for i, p in enumerate(partes, start=1):
        print(f"  Servidor {i}: {p}")

    sumas_parciales = [suma_parcial_servidor(p) for p in partes]
    print(f"Sumas parciales por servidor: {sumas_parciales}")

    suma_total = reconstruir_suma(sumas_parciales)
    promedio = suma_total / len(notas)
    print(f"Suma reconstruida = {suma_total} (esperado 150)")
    print(f"Promedio = {promedio} (esperado 37.5)")


if __name__ == "__main__":
    _demo()
