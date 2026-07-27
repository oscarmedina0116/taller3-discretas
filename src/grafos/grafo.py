"""
Representacion comun de grafos ponderados no dirigidos, usada por los
ejercicios 4 (Dijkstra) y 5 (cierre de una estacion).

Un grafo se representa como un diccionario de adyacencia:

    {
        "Portal": {"Centro": 5, "Museo": 2},
        "Centro": {"Portal": 5, ...},
        ...
    }

donde grafo[u][v] = peso (>= 0) de la arista {u, v}. Al ser no dirigido,
cada arista se guarda en ambos sentidos.
"""

from __future__ import annotations
import json


class Grafo:
    def __init__(self):
        self._adj: dict[str, dict[str, float]] = {}

    def agregar_vertice(self, v: str) -> None:
        self._adj.setdefault(v, {})

    def agregar_arista(self, u: str, v: str, peso: float) -> None:
        if peso < 0:
            raise ValueError("Dijkstra requiere pesos no negativos")
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self._adj[u][v] = peso
        self._adj[v][u] = peso

    def eliminar_vertice(self, v: str) -> None:
        """Elimina un vertice y todas las aristas que lo tocan (simula un cierre)."""
        if v not in self._adj:
            return
        for vecino in list(self._adj[v]):
            del self._adj[vecino][v]
        del self._adj[v]

    def eliminar_arista(self, u: str, v: str) -> None:
        self._adj[u].pop(v, None)
        self._adj[v].pop(u, None)

    def vertices(self) -> list[str]:
        return list(self._adj.keys())

    def vecinos(self, v: str) -> dict[str, float]:
        return self._adj.get(v, {})

    def num_aristas(self) -> int:
        return sum(len(vs) for vs in self._adj.values()) // 2

    def copiar(self) -> "Grafo":
        g = Grafo()
        for u, vecinos in self._adj.items():
            g.agregar_vertice(u)
            for v, peso in vecinos.items():
                g._adj[u][v] = peso
        return g

    @staticmethod
    def desde_diccionario(d: dict[str, dict[str, float]]) -> "Grafo":
        g = Grafo()
        for u, vecinos in d.items():
            for v, peso in vecinos.items():
                g.agregar_arista(u, v, peso)
        return g

    @staticmethod
    def desde_archivo(ruta: str) -> "Grafo":
        with open(ruta, encoding="utf-8") as f:
            return Grafo.desde_diccionario(json.load(f))

    def guardar_archivo(self, ruta: str) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self._adj, f, ensure_ascii=False, indent=2)


def grafo_ciudad_prueba() -> Grafo:
    """
    Grafo de prueba: una mini-red de transporte con 9 vertices y 13 aristas
    (cumple el minimo de 8 vertices y 12 aristas pedido en el enunciado).
    Los pesos representan minutos de viaje entre puntos de la ciudad.
    """
    aristas = [
        ("Portal", "Calle26", 5),
        ("Portal", "Museo", 8),
        ("Calle26", "Centro", 4),
        ("Calle26", "Universidad", 7),
        ("Museo", "Centro", 3),
        ("Museo", "Parque", 6),
        ("Centro", "Universidad", 2),
        ("Centro", "Hospital", 9),
        ("Universidad", "Biblioteca", 3),
        ("Parque", "Hospital", 4),
        ("Hospital", "Biblioteca", 5),
        ("Biblioteca", "Terminal", 6),
        ("Terminal", "Hospital", 8),
    ]
    g = Grafo()
    for u, v, peso in aristas:
        g.agregar_arista(u, v, peso)
    return g
