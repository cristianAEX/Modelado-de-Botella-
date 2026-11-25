import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from graficacion import config as cfg
from graficacion.cargar_obj import cargar_obj
from graficacion.framebuffer import Framebuffer
from graficacion.matrices import traslacion, rotacion_y, mult_mat_vec
from graficacion.renderizar import renderizar

OBJ = os.path.join(os.path.dirname(__file__), "..", "assets", "botella.obj")


class TestMatrices(unittest.TestCase):
    def test_traslacion(self):
        self.assertEqual(mult_mat_vec(traslacion(1, 2, 3), (0, 0, 0, 1))[:3], (1, 2, 3))

    def test_rotacion_y_90(self):
        x, y, z, _ = mult_mat_vec(rotacion_y(math.pi / 2), (1, 0, 0, 1))
        self.assertAlmostEqual(x, 0, places=6)
        self.assertAlmostEqual(z, -1, places=6)


class TestObj(unittest.TestCase):
    def test_carga(self):
        m = cargar_obj(OBJ)
        self.assertGreater(len(m["vertices"]), 0)
        self.assertEqual(len(m["caras"]), len(m["grupos"]))
        self.assertEqual(set(m["grupos"]), {"Botella", "Tapa"})
        for i0, i1, i2 in m["caras"]:
            self.assertTrue(all(0 <= i < len(m["vertices"]) for i in (i0, i1, i2)))


class TestRender(unittest.TestCase):
    def test_cada_modo_dibuja_algo(self):
        m = cargar_obj(OBJ)
        for modo in cfg.MODOS:
            fb = Framebuffer(120, 90)
            est = {"modo": modo, "esc": 1.0, "ang_x": 0.0, "ang_y": 0.5, "pos": [0.0, 0.0, 0.0]}
            renderizar(m, est, fb)
            fondo = bytes(cfg.COLOR_FONDO) * (fb.ancho * fb.alto)
            self.assertNotEqual(bytes(fb.datos), fondo, modo)


if __name__ == "__main__":
    unittest.main()
