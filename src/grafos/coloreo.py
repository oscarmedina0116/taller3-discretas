"""
Coloreo de grafos: organizar examenes sin choques (Ejercicio 6).

Idea matematica: un grafo de conflictos G = (V, E) tiene un vertice por
curso y una arista {u, v} si u y v comparten estudiantes. Una coloracion
propia asigna a cada vertice un color (franja horaria) de forma que
vertices adyacentes reciban colores distintos: c(u) != c(v) para toda
arista {u, v}.

El algoritmo voraz (greedy) recorre los vertices en algun orden y le da
a cada uno el menor color que no este usado por sus vecinos ya
coloreados. Esto siempre produce una coloracion VALIDA (por construccion
nunca repite color con un vecino ya visto), pero no siempre usa el
numero minimo de colores (el numero cromatico): el resultado depende del
orden de los vertices, y el peor caso puede usar muchos mas colores de
los estrictamente necesarios.
"""

from collections import defaultdict


class GrafoConflictos:
    """Grafo no dirigido simple, pensado para coloreo (sin pesos)."""

    def __init__(self):
        self._adj: dict[str, set[str]] = defaultdict(set)

    def agregar_vertice(self, v: str) -> None:
        self._adj.setdefault(v, set())

    def agregar_arista(self, u: str, v: str) -> None:
        self._adj[u].add(v)
        self._adj[v].add(u)

    def vertices(self) -> list[str]:
        return list(self._adj.keys())

    def vecinos(self, v: str) -> set[str]:
        return self._adj[v]


def coloreo_voraz(grafo: GrafoConflictos, orden: list[str] | None = None) -> dict[str, int]:
    """
    Asigna colores 0, 1, 2, ... a cada vertice con la estrategia voraz.
    `orden` permite fijar el orden de recorrido (por defecto, el orden de
    insercion de los vertices en el grafo).
    """
    if orden is None:
        orden = grafo.vertices()

    color_de: dict[str, int] = {}
    for v in orden:
        colores_vecinos = {color_de[u] for u in grafo.vecinos(v) if u in color_de}
        color = 0
        while color in colores_vecinos:
            color += 1
        color_de[v] = color
    return color_de


def es_coloreo_valido(grafo: GrafoConflictos, color_de: dict[str, int]) -> bool:
    """Verifica que ningun par de vertices adyacentes comparta color."""
    for u in grafo.vertices():
        for v in grafo.vecinos(u):
            if color_de[u] == color_de[v]:
                return False
    return True


def agrupar_por_color(color_de: dict[str, int]) -> dict[int, list[str]]:
    grupos: dict[int, list[str]] = defaultdict(list)
    for v, c in color_de.items():
        grupos[c].append(v)
    return dict(sorted(grupos.items()))


def grafo_cursos_prueba() -> GrafoConflictos:
    """
    Grafo de prueba con 10 cursos (vertices). Una arista significa que
    los dos cursos comparten estudiantes y por lo tanto no pueden
    coincidir en la misma franja de examen.
    """
    g = GrafoConflictos()
    cursos = [
        "Calculo", "Algebra", "Fisica", "Programacion", "Discretas",
        "Estadistica", "Quimica", "Ingles", "Etica", "Economia",
    ]
    for c in cursos:
        g.agregar_vertice(c)

    conflictos = [
        ("Calculo", "Algebra"),
        ("Calculo", "Fisica"),
        ("Calculo", "Discretas"),
        ("Algebra", "Discretas"),
        ("Algebra", "Programacion"),
        ("Fisica", "Quimica"),
        ("Programacion", "Discretas"),
        ("Programacion", "Estadistica"),
        ("Estadistica", "Discretas"),
        ("Estadistica", "Economia"),
        ("Quimica", "Etica"),
        ("Ingles", "Etica"),
        ("Ingles", "Economia"),
        ("Etica", "Economia"),
    ]
    for u, v in conflictos:
        g.agregar_arista(u, v)
    return g


def _demo():
    g = grafo_cursos_prueba()
    color_de = coloreo_voraz(g)
    grupos = agrupar_por_color(color_de)

    print(f"Numero de colores (franjas horarias) usados: {len(grupos)}")
    for color, cursos in grupos.items():
        print(f"  Franja {color}: {cursos}")

    print(f"Coloreo valido: {es_coloreo_valido(g, color_de)}")


if __name__ == "__main__":
    _demo()
