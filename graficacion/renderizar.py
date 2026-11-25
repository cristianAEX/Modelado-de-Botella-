"""Pipeline completo: objeto -> mundo -> cámara -> pantalla -> rasterizado + iluminación."""
from . import config as cfg
from .coordenadas_mundo import matriz_modelo, a_mundo, normales_a_mundo
from .coordenadas_camara import matriz_vista, a_camara
from .coordenadas_pantalla import matriz_proyeccion, a_pantalla
from .linea_bresenham import linea_bresenham
from .rasterizar_triangulo import rasterizar_triangulo
from .luz_ambiental import luz_ambiental
from .sombreado_plano import color_plano
from .sombreado_gouraud import colores_gouraud
from .vectores import restar, cruz, normalizar, punto


def renderizar(modelo, estado, fb):
    """Dibuja un cuadro. 'estado' trae: modo, esc, ang_x, ang_y, pos."""
    fb.limpiar(cfg.COLOR_FONDO)

    # 1) Objeto -> mundo
    M = matriz_modelo(estado["esc"], estado["ang_x"], estado["ang_y"], estado["pos"])
    mundo = a_mundo(modelo["vertices"], M)
    normales = normales_a_mundo(modelo["normales"], M)

    # 2) Mundo -> cámara   3) Cámara -> pantalla
    V = matriz_vista(cfg.CAMARA_POS, cfg.CAMARA_OBJETIVO)
    P = matriz_proyeccion(cfg.FOV, fb.ancho / fb.alto, cfg.CERCA, cfg.LEJOS)
    pantalla = a_pantalla(a_camara(mundo, V), P, fb.ancho, fb.alto, cfg.CERCA)

    modo = estado["modo"]
    for (i0, i1, i2), grupo in zip(modelo["caras"], modelo["grupos"]):
        p0, p1, p2 = pantalla[i0], pantalla[i1], pantalla[i2]
        if p0 is None or p1 is None or p2 is None:
            continue

        w0, w1, w2 = mundo[i0], mundo[i1], mundo[i2]
        n_cara = normalizar(cruz(restar(w1, w0), restar(w2, w0)))
        centro = ((w0[0] + w1[0] + w2[0]) / 3, (w0[1] + w1[1] + w2[1]) / 3, (w0[2] + w1[2] + w2[2]) / 3)
        if punto(n_cara, restar(cfg.CAMARA_POS, centro)) <= 0:
            continue                                   # descarte de caras traseras (back-face culling)

        base = cfg.color_de_grupo(grupo)
        if modo == "alambre":
            c = tuple(min(255, int(v * 1.1)) for v in base)
            linea_bresenham(fb, p0[0], p0[1], p1[0], p1[1], c)
            linea_bresenham(fb, p1[0], p1[1], p2[0], p2[1], c)
            linea_bresenham(fb, p2[0], p2[1], p0[0], p0[1], c)
        elif modo == "ambiental":
            c = tuple(int(v * luz_ambiental(cfg.KA)) for v in base)
            rasterizar_triangulo(fb, p0, p1, p2, c, c, c)
        elif modo == "plano":
            c = color_plano(base, n_cara, centro, cfg, cfg.CAMARA_POS)
            rasterizar_triangulo(fb, p0, p1, p2, c, c, c)
        else:  # gouraud
            c0, c1, c2 = colores_gouraud(base, (normales[i0], normales[i1], normales[i2]),
                                         (w0, w1, w2), cfg, cfg.CAMARA_POS)
            rasterizar_triangulo(fb, p0, p1, p2, c0, c1, c2)
