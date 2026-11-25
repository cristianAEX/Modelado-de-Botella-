"""Brillo especular (Blinn-Phong) usando el vector medio entre luz y vista."""
from .vectores import punto, sumar, normalizar


def luz_especular(normal, dir_luz, dir_vista, ks, brillo):
    medio = normalizar(sumar(dir_luz, dir_vista))
    return ks * max(0.0, punto(normal, medio)) ** brillo
