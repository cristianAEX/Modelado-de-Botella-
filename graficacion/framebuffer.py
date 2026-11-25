"""Búfer de imagen (RGB) y búfer de profundidad (z-buffer)."""
import struct
import zlib


class Framebuffer:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.datos = bytearray(ancho * alto * 3)
        self.zbuf = [float("inf")] * (ancho * alto)

    def limpiar(self, color):
        self.datos[:] = bytes(color) * (self.ancho * self.alto)
        self.zbuf = [float("inf")] * (self.ancho * self.alto)

    def poner_pixel(self, x, y, color):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            i = (y * self.ancho + x) * 3
            self.datos[i:i + 3] = bytes(color)

    def guardar_png(self, ruta):
        """Escribe un PNG sin usar librerías externas (zlib + struct)."""
        filas = b"".join(b"\x00" + bytes(self.datos[y * self.ancho * 3:(y + 1) * self.ancho * 3])
                         for y in range(self.alto))

        def chunk(tipo, datos):
            c = struct.pack(">I", len(datos)) + tipo + datos
            return c + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF)

        png = (b"\x89PNG\r\n\x1a\n"
               + chunk(b"IHDR", struct.pack(">IIBBBBB", self.ancho, self.alto, 8, 2, 0, 0, 0))
               + chunk(b"IDAT", zlib.compress(filas, 9))
               + chunk(b"IEND", b""))
        with open(ruta, "wb") as f:
            f.write(png)
