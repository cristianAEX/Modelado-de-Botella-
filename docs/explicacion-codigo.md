# Guía para explicar el código al profesor

1. **Objeto → mundo.** `matriz_modelo` compone escala, rotación y traslación en una matriz 4x4. Se aplica a cada vértice `(x, y, z, 1)`. Las normales usan `w = 0`, así que la traslación no les afecta.
2. **Mundo → cámara.** `matriz_vista` (look-at) construye una base ortonormal (derecha, arriba, atrás) a partir de la posición y el objetivo de la cámara. La cámara queda en el origen mirando hacia -Z.
3. **Cámara → pantalla.** `matriz_proyeccion` genera `w = -z`. Al dividir entre `w` los objetos lejanos se ven más pequeños (perspectiva). El viewport pasa de [-1, 1] a píxeles e invierte Y.
4. **Caras traseras.** Se descarta el triángulo si su normal no apunta hacia la cámara.
5. **Rasterizado.** Para cada píxel de la caja envolvente se calculan las coordenadas baricéntricas (áreas de sub-triángulos / área total). Si las tres son ≥ 0, el píxel está dentro. El z-buffer conserva el más cercano.
6. **Iluminación.** `I = ka + kd·max(0, N·L)` más brillo especular Blinn-Phong. Plano la evalúa una vez por cara. Gouraud la evalúa en los 3 vértices e interpola el color con las baricéntricas.
7. **Alambre.** Bresenham dibuja las 3 aristas de cada triángulo visible, solo con enteros.

Preguntas probables: ¿por qué `w = 0` en las normales? ¿qué pasa con un triángulo detrás de la cámara (se descarta si `w <= cerca`)? ¿diferencia entre plano y Gouraud? ¿para qué sirve el z-buffer?
