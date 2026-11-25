"""Coordenadas de PANTALLA: vista -> recorte (perspectiva) -> NDC -> píxeles."""
import math
from .matrices import mult_mat_vec


def matriz_proyeccion(fov_grados, aspecto, cerca, lejos):
    """Proyección en perspectiva (el w resultante es -z de la cámara)."""
    f = 1.0 / math.tan(math.radians(fov_grados) / 2.0)
    return [[f / aspecto, 0.0, 0.0, 0.0],
            [0.0, f, 0.0, 0.0],
            [0.0, 0.0, (lejos + cerca) / (cerca - lejos), 2.0 * lejos * cerca / (cerca - lejos)],
            [0.0, 0.0, -1.0, 0.0]]


def a_pantalla(puntos_camara, P, ancho, alto, cerca):
    """Devuelve (x, y, z) en píxeles por vértice, o None si queda detrás del plano cercano."""
    res = []
    for x, y, z in puntos_camara:
        cx, cy, cz, cw = mult_mat_vec(P, (x, y, z, 1.0))
        if cw <= cerca:
            res.append(None)
            continue
        nx, ny, nz = cx / cw, cy / cw, cz / cw          # división de perspectiva -> NDC [-1, 1]
        res.append(((nx + 1.0) * 0.5 * ancho,           # transformación de viewport
                    (1.0 - ny) * 0.5 * alto,            # el eje Y de pantalla crece hacia abajo
                    nz))
    return res
