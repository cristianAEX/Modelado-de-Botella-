"""Rasterizado de triángulos con coordenadas baricéntricas y z-buffer.

El color de cada píxel es la mezcla de los colores de los 3 vértices.
 - Con 3 colores iguales  -> sombreado plano.
 - Con 3 colores distintos -> sombreado de Gouraud.
"""
import math


def rasterizar_triangulo(fb, p0, p1, p2, c0, c1, c2):
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    if area == 0:
        return
    inv = 1.0 / area

    min_x = max(0, int(math.floor(min(x0, x1, x2))))
    max_x = min(fb.ancho - 1, int(math.ceil(max(x0, x1, x2))))
    min_y = max(0, int(math.floor(min(y0, y1, y2))))
    max_y = min(fb.alto - 1, int(math.ceil(max(y0, y1, y2))))

    zbuf, datos, ancho = fb.zbuf, fb.datos, fb.ancho
    for y in range(min_y, max_y + 1):
        py = y + 0.5
        for x in range(min_x, max_x + 1):
            px = x + 0.5
            # Coordenadas baricéntricas = áreas de sub-triángulos / área total
            w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) * inv
            w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) * inv
            w2 = 1.0 - w0 - w1
            if w0 < -1e-6 or w1 < -1e-6 or w2 < -1e-6:
                continue                      # el píxel está fuera del triángulo
            z = w0 * z0 + w1 * z1 + w2 * z2
            i = y * ancho + x
            if z < zbuf[i]:                   # prueba de profundidad
                zbuf[i] = z
                j = i * 3
                datos[j] = int(w0 * c0[0] + w1 * c1[0] + w2 * c2[0])
                datos[j + 1] = int(w0 * c0[1] + w1 * c1[1] + w2 * c2[1])
                datos[j + 2] = int(w0 * c0[2] + w1 * c1[2] + w2 * c2[2])
