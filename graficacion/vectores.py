"""Operaciones básicas con vectores 3D representados como tuplas (x, y, z)."""
import math


def sumar(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def restar(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def escalar(v, k):
    return (v[0] * k, v[1] * k, v[2] * k)


def punto(a, b):
    """Producto punto."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cruz(a, b):
    """Producto cruz."""
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def longitud(v):
    return math.sqrt(punto(v, v))


def normalizar(v):
    n = longitud(v)
    if n == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / n, v[1] / n, v[2] / n)
