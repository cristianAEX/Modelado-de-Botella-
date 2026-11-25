"""Coordenadas de la CÁMARA: mundo -> vista (matriz look-at)."""
from .vectores import restar, cruz, normalizar, punto
from .matrices import mult_mat_vec


def matriz_vista(ojo, objetivo, arriba=(0.0, 1.0, 0.0)):
    """Cámara en 'ojo' mirando a 'objetivo'. En el espacio de vista la cámara mira hacia -Z."""
    f = normalizar(restar(objetivo, ojo))   # hacia dónde mira
    s = normalizar(cruz(f, arriba))         # derecha
    u = cruz(s, f)                          # arriba real
    return [[s[0], s[1], s[2], -punto(s, ojo)],
            [u[0], u[1], u[2], -punto(u, ojo)],
            [-f[0], -f[1], -f[2], punto(f, ojo)],
            [0.0, 0.0, 0.0, 1.0]]


def a_camara(puntos_mundo, V):
    return [mult_mat_vec(V, (x, y, z, 1.0))[:3] for x, y, z in puntos_mundo]
