"""Coordenadas del OBJETO: lectura de un archivo .obj (exportado desde Blender)."""
from .vectores import restar, cruz, sumar, normalizar


def calcular_normales(vertices, caras):
    """Normal suave por vértice: promedio de las normales de las caras que lo comparten."""
    acum = [(0.0, 0.0, 0.0)] * len(vertices)
    for i0, i1, i2 in caras:
        n = cruz(restar(vertices[i1], vertices[i0]), restar(vertices[i2], vertices[i0]))
        for i in (i0, i1, i2):
            acum[i] = sumar(acum[i], n)
    return [normalizar(n) for n in acum]


def cargar_obj(ruta):
    """Lee v / o / g / f de un .obj. Triangula las caras de más de 3 lados.

    Devuelve un diccionario con:
      vertices : lista de (x, y, z) en coordenadas del objeto
      normales : normal unitaria por vértice
      caras    : lista de triángulos (i0, i1, i2)
      grupos   : nombre del objeto (o/g) al que pertenece cada cara
    """
    vertices, caras, grupos = [], [], []
    grupo = "default"
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            partes = linea.split()
            if not partes or partes[0].startswith("#"):
                continue
            tipo = partes[0]
            if tipo == "v":
                vertices.append((float(partes[1]), float(partes[2]), float(partes[3])))
            elif tipo in ("o", "g"):
                grupo = partes[1] if len(partes) > 1 else "default"
            elif tipo == "f":
                idx = []
                for p in partes[1:]:
                    i = int(p.split("/")[0])
                    idx.append(i - 1 if i > 0 else len(vertices) + i)  # soporta índices negativos
                for k in range(1, len(idx) - 1):  # triangulación en abanico
                    caras.append((idx[0], idx[k], idx[k + 1]))
                    grupos.append(grupo)
    return {"vertices": vertices,
            "normales": calcular_normales(vertices, caras),
            "caras": caras,
            "grupos": grupos}
