"""
Simplificacion booleana con una version pequena de Quine-McCluskey
(Ejercicio 8).

Idea matematica: un mintermino de una funcion de n variables es una fila
de la tabla de verdad donde la funcion vale 1, escrita como el producto
(AND) de las n variables, cada una en su forma directa o negada segun el
bit que le corresponde (por ejemplo, con variables A,B,C el mintermino 5
= 101 en binario es A AND (NOT B) AND C).

Dos terminos que difieren en un UNICO bit se pueden combinar, porque

    (X AND V) OR (X AND NOT V) = X   (ley del complemento / consenso),

eliminando la variable V que cambia. Repitiendo esto hasta que ningun
par de terminos se pueda combinar mas se obtienen los "implicantes
primos". Finalmente se eligen implicantes primos (dando prioridad a los
esenciales, es decir, los unicos que cubren cierto mintermino) hasta
cubrir todos los minterminos originales; la OR de esos implicantes es la
expresion simplificada en forma suma de productos.

Dos expresiones son equivalentes si y solo si tienen la misma tabla de
verdad (mismo conjunto de minterminos en 1); por eso el programa
comprueba la simplificacion reconstruyendo la tabla de verdad de ambas
formas y comparandolas.
"""

import itertools
from .tablas_verdad import evaluar

NOMBRES_VARS_DEFECTO = ["A", "B", "C", "D"]


def _minterm_a_bits(m: int, n_vars: int) -> str:
    return format(m, f"0{n_vars}b")


def _combinar(a: str, b: str) -> str | None:
    """Combina dos terminos si difieren en exactamente un bit (no en un guion)."""
    diferencias = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    if len(diferencias) != 1:
        return None
    i = diferencias[0]
    if a[i] not in ("0", "1") or b[i] not in ("0", "1"):
        return None  # la diferencia cae en una posicion con guion: no combina
    return a[:i] + "-" + a[i + 1:]


def _implicantes_primos(minterminos: list[int], n_vars: int) -> dict[str, frozenset[int]]:
    """Aplica el algoritmo de combinacion de Quine-McCluskey."""
    actual = {_minterm_a_bits(m, n_vars): frozenset({m}) for m in minterminos}
    primos: dict[str, frozenset[int]] = {}

    while True:
        usados = set()
        nuevos: dict[str, frozenset[int]] = {}
        terminos = list(actual.keys())
        for a, b in itertools.combinations(terminos, 2):
            combinado = _combinar(a, b)
            if combinado is not None:
                usados.add(a)
                usados.add(b)
                cubiertos = actual[a] | actual[b]
                nuevos[combinado] = nuevos.get(combinado, frozenset()) | cubiertos

        for termino, cubiertos in actual.items():
            if termino not in usados:
                primos[termino] = primos.get(termino, frozenset()) | cubiertos

        if not nuevos:
            break
        actual = nuevos

    return primos


def _seleccionar_implicantes(
    primos: dict[str, frozenset[int]], minterminos: list[int]
) -> list[str]:
    """Elige implicantes primos esenciales primero, y luego voraz por cobertura."""
    objetivo = set(minterminos)
    cubiertos: set[int] = set()
    seleccionados: list[str] = []

    while cubiertos != objetivo:
        restantes = objetivo - cubiertos
        cobertura = {m: [t for t, c in primos.items() if m in c] for m in restantes}

        esencial = next((cs[0] for cs in cobertura.values() if len(cs) == 1), None)
        if esencial is not None and esencial not in seleccionados:
            seleccionados.append(esencial)
            cubiertos |= primos[esencial]
            continue

        mejor = max(primos.items(), key=lambda kv: len(kv[1] & restantes))
        if mejor[0] in seleccionados:
            break  # seguridad: evita bucle infinito si ya no hay progreso posible
        seleccionados.append(mejor[0])
        cubiertos |= mejor[1]

    return seleccionados


def _bits_a_termino(bits: str, nombres_vars: list[str]) -> str:
    partes = []
    for bit, var in zip(bits, nombres_vars):
        if bit == "1":
            partes.append(var)
        elif bit == "0":
            partes.append(f"NOT {var}")
    return " AND ".join(partes) if partes else "1"


def simplificar(minterminos: list[int], n_vars: int, nombres_vars: list[str] | None = None) -> str:
    """
    Simplifica una funcion booleana dada por sus minterminos y devuelve
    una expresion en forma suma de productos, compatible con el
    evaluador de `tablas_verdad`.
    """
    if nombres_vars is None:
        nombres_vars = NOMBRES_VARS_DEFECTO[:n_vars]
    if not minterminos:
        return "0"  # funcion identicamente falsa

    primos = _implicantes_primos(minterminos, n_vars)
    seleccionados = _seleccionar_implicantes(primos, minterminos)
    terminos = [_bits_a_termino(bits, nombres_vars) for bits in seleccionados]
    return " OR ".join(f"({t})" for t in terminos)


def tabla_desde_minterminos(minterminos: list[int], n_vars: int) -> list[bool]:
    """Tabla de verdad (2^n valores) donde la fila i vale True si i esta en minterminos."""
    return [i in minterminos for i in range(2 ** n_vars)]


def tabla_desde_expresion(expr: str, n_vars: int, nombres_vars: list[str] | None = None) -> list[bool]:
    if nombres_vars is None:
        nombres_vars = NOMBRES_VARS_DEFECTO[:n_vars]
    # "0" (funcion vacia) y "(1)" (implicante sin variables, funcion tautologica)
    # son casos especiales que el evaluador de tablas_verdad no conoce como constantes.
    if expr == "0":
        return [False] * (2 ** n_vars)
    if expr == "(1)":
        return [True] * (2 ** n_vars)

    filas = []
    for combinacion in itertools.product([False, True], repeat=n_vars):
        valores = dict(zip(nombres_vars, combinacion))
        filas.append(evaluar(expr, valores))
    return filas


def verificar_equivalencia(minterminos: list[int], n_vars: int, expr_simplificada: str) -> bool:
    """Confirma que la expresion simplificada tiene la misma tabla de verdad que el original."""
    return tabla_desde_minterminos(minterminos, n_vars) == tabla_desde_expresion(expr_simplificada, n_vars)


def _demo():
    minterminos = [1, 3, 5, 7]
    n_vars = 3
    simplificada = simplificar(minterminos, n_vars)
    print(f"Minterminos {minterminos} (n={n_vars} variables A,B,C)")
    print(f"Expresion simplificada: {simplificada}")
    print(f"Misma tabla de verdad que el original: {verificar_equivalencia(minterminos, n_vars, simplificada)}")


if __name__ == "__main__":
    _demo()
