"""Sombreado de GOURAUD: se ilumina en cada vértice y el color se interpola en el triángulo."""
from .sombreado_plano import color_con_luz


def colores_gouraud(color_base, normales_vertice, posiciones, cfg, pos_camara):
    return [color_con_luz(color_base, n, p, cfg, pos_camara)
            for n, p in zip(normales_vertice, posiciones)]
