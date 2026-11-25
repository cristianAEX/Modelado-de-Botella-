"""Sombreado PLANO: un solo color por triángulo (se ilumina con la normal de la cara)."""
from .luz_ambiental import luz_ambiental
from .luz_difusa import luz_difusa
from .luz_especular import luz_especular
from .vectores import normalizar, restar


def color_con_luz(color_base, normal, posicion, cfg, pos_camara):
    """Ambiental + difusa + especular evaluadas en un punto con su normal."""
    dir_vista = normalizar(restar(pos_camara, posicion))
    dif = luz_ambiental(cfg.KA) + luz_difusa(normal, cfg.DIR_LUZ, cfg.KD)
    esp = luz_especular(normal, cfg.DIR_LUZ, dir_vista, cfg.KS, cfg.BRILLO)
    return tuple(min(255, int(c * dif + 255 * esp)) for c in color_base)


def color_plano(color_base, normal_cara, centro, cfg, pos_camara):
    return color_con_luz(color_base, normal_cara, centro, cfg, pos_camara)
