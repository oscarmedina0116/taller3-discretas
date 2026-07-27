# Taller 3 - Programación discreta

Matemáticas Discretas I · Universidad Nacional de Colombia
Docente: Jhoan Sebastian Tenjo García

## Integrantes

- **Nombre:** _(completar)_ — correo: `oandradem@unal.edu.co`

> Si el taller se realiza en pareja, agregar aquí el nombre y correo de la segunda persona.

## Lenguaje usado

**Python 3.10+** (probado con Python 3.11 y 3.13), usando únicamente la biblioteca
estándar. No se requieren dependencias externas — ver [requirements.txt](requirements.txt).

## Estructura del repositorio

```
taller3/
├── README.md
├── requirements.txt
├── src/
│   ├── cripto/
│   │   ├── cesar.py            # Ejercicio 1: cifrado César
│   │   ├── rsa_toy.py          # Ejercicio 2: RSA de juguete
│   │   └── mpc_promedio.py     # Ejercicio 3: MPC básico (suma secreta)
│   ├── grafos/
│   │   ├── grafo.py            # Estructura de grafo compartida (ej. 4 y 5)
│   │   ├── dijkstra.py         # Ejercicio 4: ruta más corta
│   │   ├── cierre_estacion.py  # Ejercicio 5: impacto del cierre de un vértice
│   │   └── coloreo.py          # Ejercicio 6: coloreo de grafos (voraz)
│   ├── boole/
│   │   ├── tablas_verdad.py    # Ejercicio 7: tablas de verdad y evaluador propio
│   │   └── simplificacion.py   # Ejercicio 8: simplificación booleana (Quine-McCluskey)
│   ├── informacion/
│   │   └── shannon.py          # Ejercicio 9: entropía de Shannon
│   └── cuantica/
│       └── qubit_simulador.py  # Ejercicio 10: simulador de un qubit
├── tests/                      # Un archivo de pruebas por ejercicio (unittest)
└── docs/
    └── explicacion.md          # Documento de explicación matemática (también en PDF)
```

## Cómo ejecutar

No hay que instalar nada. Desde la raíz del repositorio:

**Ejecutar la demo de un ejercicio** (cada módulo tiene un bloque `if __name__ == "__main__":`
con un caso de ejemplo impreso en consola):

```bash
python -m src.cripto.cesar
python -m src.cripto.rsa_toy
python -m src.cripto.mpc_promedio
python -m src.grafos.dijkstra
python -m src.grafos.cierre_estacion
python -m src.grafos.coloreo
python -m src.boole.tablas_verdad
python -m src.boole.simplificacion
python -m src.informacion.shannon
python -m src.cuantica.qubit_simulador
```

**Ejecutar TODAS las pruebas** (59 pruebas en total, ≥3 por ejercicio):

```bash
python -m unittest discover -s tests -v
```

Se puede correr desde cualquier sistema con Python 3.10 o superior; no se usó ninguna
ruta absoluta ni dependencia del sistema operativo.

## Lista de ejercicios desarrollados

| # | Ejercicio | Módulo | Pruebas |
|---|-----------|--------|---------|
| 1 | Cifrado César | [src/cripto/cesar.py](src/cripto/cesar.py) | [tests/test_cesar.py](tests/test_cesar.py) |
| 2 | RSA de juguete | [src/cripto/rsa_toy.py](src/cripto/rsa_toy.py) | [tests/test_rsa_toy.py](tests/test_rsa_toy.py) |
| 3 | MPC básico (suma secreta) | [src/cripto/mpc_promedio.py](src/cripto/mpc_promedio.py) | [tests/test_mpc_promedio.py](tests/test_mpc_promedio.py) |
| 4 | Ruta más corta (Dijkstra) | [src/grafos/dijkstra.py](src/grafos/dijkstra.py) | [tests/test_dijkstra.py](tests/test_dijkstra.py) |
| 5 | Cierre de una estación | [src/grafos/cierre_estacion.py](src/grafos/cierre_estacion.py) | [tests/test_cierre_estacion.py](tests/test_cierre_estacion.py) |
| 6 | Coloreo de grafos | [src/grafos/coloreo.py](src/grafos/coloreo.py) | [tests/test_coloreo.py](tests/test_coloreo.py) |
| 7 | Tablas de verdad y circuitos lógicos | [src/boole/tablas_verdad.py](src/boole/tablas_verdad.py) | [tests/test_tablas_verdad.py](tests/test_tablas_verdad.py) |
| 8 | Simplificación booleana (Quine-McCluskey) | [src/boole/simplificacion.py](src/boole/simplificacion.py) | [tests/test_simplificacion.py](tests/test_simplificacion.py) |
| 9 | Entropía de Shannon | [src/informacion/shannon.py](src/informacion/shannon.py) | [tests/test_shannon.py](tests/test_shannon.py) |
| 10 | Simulador cuántico de un qubit | [src/cuantica/qubit_simulador.py](src/cuantica/qubit_simulador.py) | [tests/test_qubit_simulador.py](tests/test_qubit_simulador.py) |

La explicación matemática de cada punto (qué problema resuelve, qué idea matemática usa,
cómo se ejecuta, qué pruebas se hicieron y qué limitaciones tiene) está en
[docs/explicacion.md](docs/explicacion.md) (también entregado en PDF).

## Sobre el uso de librerías

No se usó ninguna librería externa. Todos los algoritmos centrales (Euclides extendido,
reparto de secretos, Dijkstra, coloreo voraz, Quine-McCluskey, entropía de Shannon,
álgebra lineal 2x2 para el qubit) están implementados desde cero con la biblioteca
estándar de Python, tal como lo pide el enunciado.

## Limitaciones generales

- El RSA del ejercicio 2 es "de juguete": usa primos pequeños solo para poder verificar
  el cálculo a mano y **no debe usarse como criptografía real**.
- El MPC del ejercicio 3 es una simulación educativa de reparto de secretos aditivo, no
  un protocolo de seguridad multipartita listo para producción.
- El simulador cuántico del ejercicio 10 trabaja con un solo qubit y aritmética clásica
  de punto flotante; no reproduce efectos de ruido de hardware real.
