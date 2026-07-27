"""
Entropia de Shannon (Ejercicio 9).

Idea matematica: si una fuente emite el simbolo i con probabilidad p_i,
la entropia de Shannon

    H = - sum_i p_i * log2(p_i)

mide la incertidumbre promedio (en bits) de esa fuente. Intuitivamente:

  - si un simbolo aparece siempre (p_i = 1), no hay sorpresa alguna y
    H = 0: el mensaje es completamente predecible.
  - si todos los simbolos son igual de probables, no hay forma de
    adivinar el siguiente mejor que al azar, y H alcanza su maximo
    (log2(numero de simbolos distintos)).

H no depende de la longitud del texto sino de la FORMA de la
distribucion de frecuencias: "AAAAAAAAAA" y "AAAAA" tienen la misma
entropia (0 bits) aunque tengan longitudes distintas, porque en ambos
casos el simbolo siguiente es siempre el mismo, es decir, no hay
incertidumbre que medir.
"""

import math
from collections import Counter


def frecuencias(texto: str) -> Counter:
    """Cuenta cuantas veces aparece cada simbolo (caracter) en el texto."""
    if not texto:
        raise ValueError("El texto no puede estar vacio")
    return Counter(texto)


def probabilidades(texto: str) -> dict[str, float]:
    """Convierte las frecuencias en probabilidades p_i = frecuencia_i / longitud."""
    frecs = frecuencias(texto)
    n = len(texto)
    return {simbolo: cuenta / n for simbolo, cuenta in frecs.items()}


def entropia(texto: str) -> float:
    """H = - sum p_i log2(p_i), en bits por simbolo."""
    probs = probabilidades(texto)
    # sumar 0.0 evita el "-0.0" de punto flotante cuando H es exactamente 0
    return -sum(p * math.log2(p) for p in probs.values()) + 0.0


def comparar(texto_a: str, texto_b: str) -> str:
    """Compara la entropia de dos textos y explica cual es mas incierto."""
    h_a, h_b = entropia(texto_a), entropia(texto_b)
    if h_a > h_b:
        mas_incierto, otro, h_mas, h_otro = "el primer texto", "el segundo", h_a, h_b
    elif h_b > h_a:
        mas_incierto, otro, h_mas, h_otro = "el segundo texto", "el primero", h_b, h_a
    else:
        return f"Ambos textos tienen la misma entropia ({h_a:.4f} bits/simbolo)."
    return (
        f"{mas_incierto.capitalize()} tiene mayor entropia ({h_mas:.4f} bits/simbolo) "
        f"que {otro} ({h_otro:.4f} bits/simbolo): su distribucion de simbolos "
        f"esta mas repartida, por lo que es mas dificil predecir el siguiente caracter."
    )


def _demo():
    repetitivo = "AAAAAAAAAAAAAAAA"
    variado = "el veloz murcielago hindu comia feliz cardillo y kiwi"

    for nombre, texto in [("repetitivo", repetitivo), ("variado", variado)]:
        print(f"Texto {nombre}: {texto!r}")
        print(f"  Frecuencias: {dict(frecuencias(texto))}")
        print(f"  Entropia: {entropia(texto):.4f} bits/simbolo\n")

    print(comparar(repetitivo, variado))


if __name__ == "__main__":
    _demo()
