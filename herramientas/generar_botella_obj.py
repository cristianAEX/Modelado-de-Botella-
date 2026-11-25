"""Genera assets/botella.obj con un sólido de revolución (mismo método que el Screw de Blender).

Sirve como botella de respaldo para probar el renderizador. Para la entrega final
reemplaza assets/botella.obj por el modelo exportado desde Blender.

Uso:  python herramientas/generar_botella_obj.py [segmentos]
"""
import math
import os
import sys

# Perfiles (radio, altura) con el origen en la base de la botella
PERFIL_BOTELLA = [(0.0, 0.0), (0.85, 0.0), (1.0, 0.12), (1.06, 0.45), (1.06, 2.15),
                  (1.0, 2.55), (0.78, 2.95), (0.52, 3.2), (0.42, 3.35), (0.42, 3.55)]
PERFIL_TAPA = [(0.0, 3.50), (0.52, 3.50), (0.52, 3.95), (0.46, 4.02), (0.0, 4.02)]


def revolucionar(perfil, segmentos, vertices, caras):
    """Agrega a 'vertices' y 'caras' la superficie de revolución del perfil (eje Y)."""
    base = len(vertices)
    idx = []  # idx[i][j] = índice (base 1 de .obj) del vértice del punto i del perfil, ángulo j
    for r, y in perfil:
        if r == 0.0:                       # punto sobre el eje: un solo vértice compartido
            vertices.append((0.0, y, 0.0))
            idx.append([len(vertices)] * segmentos)
        else:
            fila = []
            for j in range(segmentos):
                t = 2 * math.pi * j / segmentos
                vertices.append((r * math.cos(t), y, r * math.sin(t)))
                fila.append(len(vertices))
            idx.append(fila)
    for i in range(len(perfil) - 1):
        for j in range(segmentos):
            k = (j + 1) % segmentos
            a, b, c, d = idx[i][j], idx[i][k], idx[i + 1][k], idx[i + 1][j]
            for tri in ((a, c, b), (a, d, c)):        # orientación antihoraria vista desde fuera
                if len(set(tri)) == 3:                # descarta triángulos degenerados (polos)
                    caras.append(tri)


def main():
    segmentos = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    salida = os.path.join(os.path.dirname(__file__), "..", "assets", "botella.obj")
    with open(salida, "w", encoding="utf-8") as f:
        f.write("# Botella generada por herramientas/generar_botella_obj.py\n")
        base = 0
        for nombre, perfil in (("Botella", PERFIL_BOTELLA), ("Tapa", PERFIL_TAPA)):
            vertices, caras = [], []
            revolucionar(perfil, segmentos, vertices, caras)
            f.write(f"o {nombre}\n")
            for x, y, z in vertices:
                f.write(f"v {x:.5f} {y:.5f} {z:.5f}\n")
            for a, b, c in caras:
                f.write(f"f {a + base} {b + base} {c + base}\n")
            base += len(vertices)
    print("Generado", os.path.abspath(salida))


if __name__ == "__main__":
    main()
