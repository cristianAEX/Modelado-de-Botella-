"""Matrices 4x4 en coordenadas homogéneas (listas de listas, orden por filas)."""
import math


def identidad():
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def multiplicar(a, b):
    """Devuelve A * B (se aplica primero B y luego A sobre un vector columna)."""
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]


def mult_mat_vec(m, v):
    """Multiplica una matriz 4x4 por un vector homogéneo (x, y, z, w)."""
    return tuple(sum(m[i][k] * v[k] for k in range(4)) for i in range(4))


def traslacion(tx, ty, tz):
    m = identidad()
    m[0][3], m[1][3], m[2][3] = tx, ty, tz
    return m


def escala(sx, sy, sz):
    m = identidad()
    m[0][0], m[1][1], m[2][2] = sx, sy, sz
    return m


def rotacion_x(ang):
    c, s = math.cos(ang), math.sin(ang)
    return [[1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotacion_y(ang):
    c, s = math.cos(ang), math.sin(ang)
    return [[c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0]]


def rotacion_z(ang):
    c, s = math.cos(ang), math.sin(ang)
    return [[c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]]
