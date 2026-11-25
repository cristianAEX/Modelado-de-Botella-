"""Luz difusa (Lambert): depende del ángulo entre la normal y la dirección a la luz."""
from .vectores import punto


def luz_difusa(normal, dir_luz, kd):
    return kd * max(0.0, punto(normal, dir_luz))
