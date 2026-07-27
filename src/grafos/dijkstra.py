"""
Ruta mas corta con el algoritmo de Dijkstra (Ejercicio 4).

Idea matematica: Dijkstra mantiene, para cada vertice v, la mejor
distancia conocida dist[v] desde el origen. En cada paso elige el
vertice NO visitado con menor dist[v] (una cola de prioridad) y relaja
sus aristas: si dist[u] + peso(u, v) < dist[v], se actualiza dist[v].

La correccion depende de que los pesos sean >= 0: el vertice elegido en
cada paso ya tiene la distancia minima posible, porque cualquier otro
camino hacia el tendria que pasar por un vertice aun no visitado, cuya
distancia parcial ya es >= dist[v] elegido (si los pesos fueran
negativos, un camino mas largo en numero de aristas podria terminar
siendo mas corto en peso total, y esta garantia se rompe).

Un camino es "optimo" cuando ningun otro camino entre los mismos dos
vertices tiene una suma de pesos menor.
"""

import heapq
from .grafo import Grafo


def dijkstra(grafo: Grafo, origen: str) -> tuple[dict[str, float], dict[str, str | None]]:
    """
    Calcula la distancia minima desde `origen` a todos los vertices
    alcanzables. Devuelve (distancias, predecesores) para poder
    reconstruir el camino con `reconstruir_camino`.
    """
    if origen not in grafo.vertices():
        raise ValueError(f"El vertice de origen '{origen}' no existe en el grafo")

    distancias = {v: float("inf") for v in grafo.vertices()}
    predecesores: dict[str, str | None] = {v: None for v in grafo.vertices()}
    distancias[origen] = 0

    visitados = set()
    cola = [(0, origen)]

    while cola:
        dist_u, u = heapq.heappop(cola)
        if u in visitados:
            continue
        visitados.add(u)

        for v, peso in grafo.vecinos(u).items():
            nueva_dist = dist_u + peso
            if nueva_dist < distancias[v]:
                distancias[v] = nueva_dist
                predecesores[v] = u
                heapq.heappush(cola, (nueva_dist, v))

    return distancias, predecesores


def reconstruir_camino(predecesores: dict[str, str | None], origen: str, destino: str) -> list[str]:
    """Reconstruye el camino origen -> destino recorriendo los predecesores hacia atras."""
    if destino not in predecesores:
        return []
    camino = []
    actual: str | None = destino
    while actual is not None:
        camino.append(actual)
        if actual == origen:
            break
        actual = predecesores[actual]
    camino.reverse()
    if not camino or camino[0] != origen:
        return []  # no hay camino de origen a destino
    return camino


def ruta_mas_corta(grafo: Grafo, origen: str, destino: str) -> tuple[float, list[str]]:
    """Atajo: devuelve (distancia_total, camino) entre origen y destino."""
    distancias, predecesores = dijkstra(grafo, origen)
    dist = distancias.get(destino, float("inf"))
    if dist == float("inf"):
        return float("inf"), []
    return dist, reconstruir_camino(predecesores, origen, destino)


def _demo():
    from .grafo import grafo_ciudad_prueba

    g = grafo_ciudad_prueba()
    origen, destino = "Portal", "Terminal"
    dist, camino = ruta_mas_corta(g, origen, destino)
    print(f"Distancia {origen} -> {destino}: {dist}")
    print(f"Ruta: {' -> '.join(camino)}")


if __name__ == "__main__":
    _demo()
