"""Coordenadas del MUNDO: objeto -> mundo mediante la matriz de modelo."""
from .matrices import multiplicar, traslacion, escala, rotacion_x, rotacion_y, mult_mat_vec
from .vectores import normalizar


def matriz_modelo(esc, ang_x, ang_y, pos):
    """M = T * Ry * Rx * S  (primero escala, luego rota, al final traslada)."""
    S = escala(esc, esc, esc)
    R = multiplicar(rotacion_y(ang_y), rotacion_x(ang_x))
    T = traslacion(*pos)
    return multiplicar(T, multiplicar(R, S))


def a_mundo(vertices, M):
    """Aplica M a cada vértice (x, y, z, 1)."""
    return [mult_mat_vec(M, (x, y, z, 1.0))[:3] for x, y, z in vertices]


def normales_a_mundo(normales, M):
    """Las normales son direcciones (w = 0): solo les afecta la rotación."""
    return [normalizar(mult_mat_vec(M, (x, y, z, 0.0))[:3]) for x, y, z in normales]
