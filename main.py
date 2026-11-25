"""Visor interactivo de la botella 3D.

Controles:
  1 alambre | 2 ambiental | 3 plano | 4 gouraud
  Flechas  rotar         W A S D  mover en pantalla      Q / E  acercar / alejar
  ESPACIO  rotación automática       R  reiniciar        ESC  salir

Modo sin ventana (para capturas o pruebas):
  python main.py --guardar captura.png --modo gouraud --angulo 30
"""
import argparse
import math
import os
import sys

from graficacion import config as cfg
from graficacion.cargar_obj import cargar_obj
from graficacion.framebuffer import Framebuffer
from graficacion.renderizar import renderizar

RUTA_DEFECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "botella.obj")


def estado_inicial(modo):
    return {"modo": modo, "esc": 1.0, "ang_x": 0.0, "ang_y": 0.0, "pos": [0.0, 0.0, 0.0], "auto": True}


def bucle_interactivo(modelo, args):
    try:
        import pygame
    except ImportError:
        sys.exit("Falta pygame para la ventana: pip install -r requirements.txt\n"
                 "(o usa --guardar archivo.png para renderizar sin ventana)")

    pygame.init()
    fb = Framebuffer(args.ancho, args.alto)
    pantalla = pygame.display.set_mode((args.ancho * args.zoom, args.alto * args.zoom))
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("monospace", 16)
    est = estado_inicial(args.modo)

    ejecutando = True
    while ejecutando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                ejecutando = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif ev.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    est["modo"] = cfg.MODOS[ev.key - pygame.K_1]
                elif ev.key == pygame.K_SPACE:
                    est["auto"] = not est["auto"]
                elif ev.key == pygame.K_r:
                    est = estado_inicial(est["modo"])

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            est["ang_y"] -= 0.06
        if teclas[pygame.K_RIGHT]:
            est["ang_y"] += 0.06
        if teclas[pygame.K_UP]:
            est["ang_x"] -= 0.04
        if teclas[pygame.K_DOWN]:
            est["ang_x"] += 0.04
        if teclas[pygame.K_a]:
            est["pos"][0] -= 0.1
        if teclas[pygame.K_d]:
            est["pos"][0] += 0.1
        if teclas[pygame.K_w]:
            est["pos"][1] += 0.1
        if teclas[pygame.K_s]:
            est["pos"][1] -= 0.1
        if teclas[pygame.K_q]:
            est["pos"][2] += 0.1
        if teclas[pygame.K_e]:
            est["pos"][2] -= 0.1
        if est["auto"]:
            est["ang_y"] += 0.03

        renderizar(modelo, est, fb)
        img = pygame.image.frombuffer(bytes(fb.datos), (fb.ancho, fb.alto), "RGB")
        pantalla.blit(pygame.transform.scale(img, pantalla.get_size()), (0, 0))
        texto = f"{est['modo']}  {reloj.get_fps():.0f} fps"
        pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (8, 6))
        pygame.display.flip()
        reloj.tick(30)
    pygame.quit()


def main():
    ap = argparse.ArgumentParser(description="Render 3D de una botella (pipeline propio)")
    ap.add_argument("--obj", default=RUTA_DEFECTO, help="archivo .obj a cargar")
    ap.add_argument("--modo", choices=cfg.MODOS, default="gouraud")
    ap.add_argument("--ancho", type=int, default=320, help="ancho del render en píxeles")
    ap.add_argument("--alto", type=int, default=240, help="alto del render en píxeles")
    ap.add_argument("--zoom", type=int, default=2, help="factor de ampliación de la ventana")
    ap.add_argument("--guardar", metavar="PNG", help="renderiza un cuadro a PNG sin abrir ventana")
    ap.add_argument("--angulo", type=float, default=30.0, help="giro en Y (grados) para --guardar")
    ap.add_argument("--inclinacion", type=float, default=10.0, help="giro en X (grados) para --guardar")
    args = ap.parse_args()

    modelo = cargar_obj(args.obj)
    if args.guardar:
        est = estado_inicial(args.modo)
        est["ang_y"] = math.radians(args.angulo)
        est["ang_x"] = math.radians(args.inclinacion)
        fb = Framebuffer(args.ancho, args.alto)
        renderizar(modelo, est, fb)
        fb.guardar_png(args.guardar)
        print("Guardado", args.guardar)
    else:
        bucle_interactivo(modelo, args)


if __name__ == "__main__":
    main()
