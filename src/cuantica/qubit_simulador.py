"""
Primer simulador cuantico: bits, qubits y mediciones (Ejercicio 10).

Idea matematica: un bit clasico vale 0 o 1. Un qubit se representa como
un vector columna de amplitudes complejas

    |psi> = alpha |0> + beta |1> = (alpha, beta)^T,   |alpha|^2 + |beta|^2 = 1.

|alpha|^2 es la probabilidad de medir 0 y |beta|^2 la probabilidad de
medir 1 (regla de Born). Las compuertas cuanticas de un qubit son
matrices unitarias 2x2 que actuan sobre el vector por multiplicacion:

    X = [[0, 1], [1, 0]]                 (negacion: intercambia |0> y |1>)
    Z = [[1, 0], [0, -1]]                (cambia el signo de la amplitud de |1>)
    H = (1/sqrt(2)) [[1, 1], [1, -1]]    (crea superposicion 50/50)

Este modulo NO usa un computador cuantico real: solo hace algebra lineal
con vectores de 2 entradas (numeros complejos) y simula mediciones
muestreando de la distribucion de probabilidad que la regla de Born
predice.
"""

import cmath
import random

X = [[0, 1], [1, 0]]
Z = [[1, 0], [0, -1]]
RAIZ2_INV = 1 / cmath.sqrt(2).real
H = [[RAIZ2_INV, RAIZ2_INV], [RAIZ2_INV, -RAIZ2_INV]]

KET_0 = (1 + 0j, 0 + 0j)
KET_1 = (0 + 0j, 1 + 0j)


def aplicar_compuerta(matriz: list[list[complex]], estado: tuple[complex, complex]) -> tuple[complex, complex]:
    """Multiplica la matriz 2x2 de la compuerta por el vector de estado."""
    a, b = estado
    fila0 = matriz[0][0] * a + matriz[0][1] * b
    fila1 = matriz[1][0] * a + matriz[1][1] * b
    return (fila0, fila1)


def probabilidades(estado: tuple[complex, complex]) -> tuple[float, float]:
    """Regla de Born: P(0) = |alpha|^2, P(1) = |beta|^2."""
    alpha, beta = estado
    p0 = abs(alpha) ** 2
    p1 = abs(beta) ** 2
    return p0, p1


def medir(estado: tuple[complex, complex]) -> int:
    """Simula UNA medicion: devuelve 0 o 1 con probabilidad segun Born."""
    p0, _ = probabilidades(estado)
    return 0 if random.random() < p0 else 1


def simular_mediciones(estado: tuple[complex, complex], n: int = 1000) -> dict[int, int]:
    """Repite la medicion n veces y cuenta cuantas veces salio 0 y cuantas 1."""
    conteos = {0: 0, 1: 0}
    for _ in range(n):
        conteos[medir(estado)] += 1
    return conteos


def _fmt(estado: tuple[complex, complex]) -> str:
    return f"({estado[0]:.3f}, {estado[1]:.3f})"


def _demo():
    print("Caso 1: X|0> = |1>")
    resultado = aplicar_compuerta(X, KET_0)
    print(f"  X|0> = {_fmt(resultado)} (esperado (0, 1))\n")

    print("Caso 2: H|0> produce ~50%/50%")
    estado_h = aplicar_compuerta(H, KET_0)
    p0, p1 = probabilidades(estado_h)
    print(f"  H|0> = {_fmt(estado_h)}  ->  P(0)={p0:.3f}, P(1)={p1:.3f}")
    conteos = simular_mediciones(estado_h, 1000)
    print(f"  1000 mediciones: {conteos}\n")

    print("Caso 3: HH|0> = |0>")
    estado_hh = aplicar_compuerta(H, estado_h)
    print(f"  HH|0> = {_fmt(estado_hh)} (esperado ~(1, 0))\n")

    print("Extra: Z sobre H|0>")
    estado_z = aplicar_compuerta(Z, estado_h)
    print(f"  Z H|0> = {_fmt(estado_z)}")


if __name__ == "__main__":
    _demo()
