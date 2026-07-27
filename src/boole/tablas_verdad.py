"""
Tablas de verdad y circuitos logicos (Ejercicio 7).

Idea matematica: una expresion booleana con n variables define una
funcion f: {0,1}^n -> {0,1}. La tabla de verdad enumera EXHAUSTIVAMENTE
las 2^n combinaciones de entrada y el valor de f en cada una. Cada fila
de la tabla corresponde a una posible configuracion de interruptores
(compuertas) en un circuito digital: AND es una compuerta "Y", OR una
compuerta "O", NOT un inversor y XOR una compuerta "o exclusivo". Por
eso una tabla de verdad es exactamente la especificacion funcional de un
circuito logico.

Este modulo implementa un evaluador propio (parser recursivo) para
expresiones escritas con las palabras AND, OR, NOT, XOR y parentesis,
sobre variables A, B, C, D.
"""

import re
import itertools

TOKEN_RE = re.compile(r"\(|\)|AND|OR|NOT|XOR|[A-D]", re.IGNORECASE)


def _tokenizar(expr: str) -> list[str]:
    tokens = TOKEN_RE.findall(expr)
    reconstruido = "".join(t for t in tokens)
    sin_espacios = re.sub(r"\s+", "", expr)
    if reconstruido.upper() != sin_espacios.upper():
        raise ValueError(f"Expresion con caracteres no reconocidos: {expr!r}")
    return [t.upper() if t.upper() in ("AND", "OR", "NOT", "XOR") else t for t in tokens]


class _Parser:
    """
    Precedencia (de menor a mayor): OR, XOR, AND, NOT.
    Gramatica:
        expr      := xor_expr ( 'OR' xor_expr )*
        xor_expr  := and_expr ( 'XOR' and_expr )*
        and_expr  := not_expr ( 'AND' not_expr )*
        not_expr  := 'NOT' not_expr | atomo
        atomo     := VARIABLE | '(' expr ')'
    """

    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consumir(self, esperado=None):
        tok = self._peek()
        if esperado is not None and tok != esperado:
            raise ValueError(f"Se esperaba '{esperado}' pero se encontro '{tok}'")
        self.pos += 1
        return tok

    def parse(self, valores: dict[str, bool]) -> bool:
        resultado = self._expr(valores)
        if self.pos != len(self.tokens):
            raise ValueError("Tokens sobrantes al final de la expresion")
        return resultado

    def _expr(self, valores):
        # OJO: no usar `or` de Python para combinar aqui. Su cortocircuito
        # se saltaria la LECTURA (no solo el valor) del lado derecho
        # cuando el izquierdo ya es True, dejando tokens sin consumir.
        resultado = self._xor_expr(valores)
        while self._peek() == "OR":
            self._consumir("OR")
            derecho = self._xor_expr(valores)
            resultado = resultado or derecho
        return resultado

    def _xor_expr(self, valores):
        resultado = self._and_expr(valores)
        while self._peek() == "XOR":
            self._consumir("XOR")
            resultado = resultado ^ self._and_expr(valores)
        return resultado

    def _and_expr(self, valores):
        # Mismo cuidado que en _expr: `and` cortocircuitaria la lectura
        # del lado derecho cuando el izquierdo ya es False.
        resultado = self._not_expr(valores)
        while self._peek() == "AND":
            self._consumir("AND")
            derecho = self._not_expr(valores)
            resultado = resultado and derecho
        return resultado

    def _not_expr(self, valores):
        if self._peek() == "NOT":
            self._consumir("NOT")
            return not self._not_expr(valores)
        return self._atomo(valores)

    def _atomo(self, valores):
        tok = self._peek()
        if tok == "(":
            self._consumir("(")
            resultado = self._expr(valores)
            self._consumir(")")
            return resultado
        if tok is not None and re.fullmatch("[A-D]", tok):
            self._consumir()
            if tok not in valores:
                raise ValueError(f"Falta el valor de la variable '{tok}'")
            return bool(valores[tok])
        raise ValueError(f"Token inesperado: {tok}")


def variables_usadas(expr: str) -> list[str]:
    """
    Devuelve, en orden alfabetico, las variables A-D presentes en la
    expresion. Se basa en los tokens (no en un regex sobre el texto
    crudo) para no confundir, por ejemplo, la "A" y la "D" que aparecen
    dentro de la palabra clave "AND" con variables reales.
    """
    tokens = _tokenizar(expr)
    return sorted({t for t in tokens if t not in ("(", ")", "AND", "OR", "NOT", "XOR")})


def evaluar(expr: str, valores: dict[str, bool]) -> bool:
    """Evalua `expr` (p.ej. "(A AND B) OR (NOT C)") con los valores dados."""
    tokens = _tokenizar(expr)
    return _Parser(tokens).parse(valores)


def tabla_de_verdad(expr: str) -> list[tuple[dict[str, bool], bool]]:
    """
    Genera la tabla de verdad completa de `expr`: una fila por cada una
    de las 2^n combinaciones de las n variables que aparecen en ella.
    """
    variables = variables_usadas(expr)
    filas = []
    for combinacion in itertools.product([False, True], repeat=len(variables)):
        valores = dict(zip(variables, combinacion))
        filas.append((valores, evaluar(expr, valores)))
    return filas


def imprimir_tabla(expr: str) -> None:
    variables = variables_usadas(expr)
    print(f"Tabla de verdad de: {expr}")
    print(" | ".join(variables) + " | Resultado")
    print("-" * (4 * len(variables) + 12))
    for valores, resultado in tabla_de_verdad(expr):
        fila = " | ".join(("1" if valores[v] else "0") for v in variables)
        print(f"{fila} | {'1' if resultado else '0'}")
    print()


EXPRESIONES_EJEMPLO = [
    "(A AND B) OR (NOT C)",
    "(A XOR B) AND C",
    "(A OR B) AND (NOT A OR C)",
]


def _demo():
    for expr in EXPRESIONES_EJEMPLO:
        imprimir_tabla(expr)

    entrada = {"A": True, "B": False, "C": True}
    print(f"Evaluacion puntual de '{EXPRESIONES_EJEMPLO[0]}' en {entrada}: "
          f"{evaluar(EXPRESIONES_EJEMPLO[0], entrada)}")


if __name__ == "__main__":
    _demo()
