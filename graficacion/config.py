"""Parámetros de escena, cámara e iluminación."""
from .vectores import normalizar

# Pantalla
COLOR_FONDO = (24, 26, 34)

# Cámara
CAMARA_POS = (0.0, 2.6, 9.5)
CAMARA_OBJETIVO = (0.0, 2.0, 0.0)
FOV = 45.0
CERCA, LEJOS = 0.5, 50.0

# Iluminación (la luz está fija en el mundo: al girar la botella cambia el sombreado)
DIR_LUZ = normalizar((0.6, 0.8, 0.7))   # dirección hacia la luz
KA, KD, KS, BRILLO = 0.30, 0.75, 0.40, 32

# Color base por grupo/objeto del .obj (se busca por coincidencia de texto en minúsculas)
COLORES = {"tapa": (220, 60, 60)}
COLOR_DEFECTO = (90, 170, 235)

MODOS = ("alambre", "ambiental", "plano", "gouraud")


def color_de_grupo(nombre):
    n = nombre.lower()
    for clave, color in COLORES.items():
        if clave in n:
            return color
    return COLOR_DEFECTO
