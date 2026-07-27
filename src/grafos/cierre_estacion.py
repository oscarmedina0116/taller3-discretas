"""
Cierre de una estacion: medir el impacto en la red (Ejercicio 5).

Idea matematica: cerrar un vertice v equivale a trabajar con el subgrafo
inducido G' = G - v (se eliminan v y todas las aristas incidentes en el).
Para cada par (origen, destino) se compara dist_G(origen, destino) con
dist_G'(origen, destino):

  - si destino queda inalcanzable en G', la distancia pasa a ser infinita
    (estado "desconectado");
  - si la distancia aumenta, el cierre obligo a usar un camino mas largo;
  - si la distancia no cambia, existia una ruta alterna igual de corta
    que no pasaba por v.
"""

from dataclasses import dataclass
from .grafo import Grafo, grafo_ciudad_prueba
from .dijkstra import ruta_mas_corta


@dataclass
class ImpactoPar:
    origen: str
    destino: str
    distancia_antes: float
    distancia_despues: float
    diferencia: float | None
    estado: str  # "sin cambio", "aumento", "desconectado"


def _clasificar(antes: float, despues: float) -> tuple[float | None, str]:
    if despues == float("inf"):
        return None, "desconectado"
    diferencia = despues - antes
    if diferencia > 0:
        return diferencia, "aumento"
    return 0, "sin cambio"


def medir_impacto_cierre(
    grafo: Grafo,
    pares: list[tuple[str, str]],
    vertice_a_cerrar: str | None = None,
    arista_a_cerrar: tuple[str, str] | None = None,
) -> list[ImpactoPar]:
    """
    Calcula, para cada par (origen, destino) en `pares`, la distancia
    antes y despues de cerrar `vertice_a_cerrar` (o `arista_a_cerrar`).
    Se debe indicar exactamente uno de los dos cierres.
    """
    if (vertice_a_cerrar is None) == (arista_a_cerrar is None):
        raise ValueError("Indique exactamente un cierre: vertice o arista")

    distancias_antes = {
        (o, d): ruta_mas_corta(grafo, o, d)[0] for o, d in pares
    }

    grafo_cerrado = grafo.copiar()
    if vertice_a_cerrar is not None:
        grafo_cerrado.eliminar_vertice(vertice_a_cerrar)
    else:
        u, v = arista_a_cerrar
        grafo_cerrado.eliminar_arista(u, v)

    resultados = []
    for o, d in pares:
        antes = distancias_antes[(o, d)]
        if o not in grafo_cerrado.vertices() or d not in grafo_cerrado.vertices():
            despues = float("inf")
        else:
            despues = ruta_mas_corta(grafo_cerrado, o, d)[0]
        diferencia, estado = _clasificar(antes, despues)
        resultados.append(ImpactoPar(o, d, antes, despues, diferencia, estado))
    return resultados


def imprimir_tabla(resultados: list[ImpactoPar]) -> None:
    encabezado = f"{'Origen':<12}{'Destino':<12}{'Antes':>8}{'Despues':>10}{'Dif':>8}  Estado"
    print(encabezado)
    print("-" * len(encabezado))
    for r in resultados:
        despues_str = "inf" if r.distancia_despues == float("inf") else f"{r.distancia_despues:.0f}"
        dif_str = "-" if r.diferencia is None else f"{r.diferencia:.0f}"
        print(
            f"{r.origen:<12}{r.destino:<12}{r.distancia_antes:>8.0f}"
            f"{despues_str:>10}{dif_str:>8}  {r.estado}"
        )


def _demo():
    g = grafo_ciudad_prueba()
    pares = [
        ("Portal", "Terminal"),
        ("Portal", "Biblioteca"),
        ("Museo", "Terminal"),
        ("Calle26", "Hospital"),
        ("Parque", "Universidad"),
    ]
    vertice_cerrado = "Centro"
    print(f"Cerrando el vertice '{vertice_cerrado}'\n")
    resultados = medir_impacto_cierre(g, pares, vertice_a_cerrar=vertice_cerrado)
    imprimir_tabla(resultados)


if __name__ == "__main__":
    _demo()
