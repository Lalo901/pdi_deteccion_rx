# Fundamentos de Procesamiento Digital de Imágenes (PDI) en Radiología
## Guía Conceptual y Storytelling para la Presentación de la Consola RX

Este documento recopila la base teórica y la justificación técnica de las técnicas de PDI aplicadas al diagnóstico de fracturas pediátricas y neonatales en nuestra consola médica. Su estructura está diseñada para servir como base para diapositivas de defensa académica ante un público técnico en computación científica, pero no médico.

---

## 1. El Ajuste de Window Leveling (Mapeo de Ventana)
### ¿Cómo aislamos el hueso del tejido blando?

En PDI, una radiografía digital es una matriz de intensidades de píxeles. La densidad del material biológico determina el valor del píxel:
*   **Aire y Tejidos Blandos (Baja densidad):** Permiten el paso casi total de la radiación. Llegan con mucha energía al detector y se registran como **valores de píxel bajos (tonos oscuros/negros)**.
*   **Huesos (Alta densidad de calcio):** Bloquean el paso de la radiación (son radiopacos). Llegan con poca energía al detector y se registran como **valores de píxel altos (tonos claros/blancos)**.

```text
Intensidad de Píxel en 8-bits:
[0 (Negro/Aire) ── 140 (Tejido Blando) ── 180 (Cartílago) ── 255 (Hueso/Calcio)]
                                          ▲──────── Window (100) ────────▲
                                                   Level (180)
```

#### El Ajuste Calibrado para el MVP (W=100, L=180):
1.  **Nivel (Level = 180):** Desplaza el punto central del brillo hacia los valores altos de gris donde el hueso de los niños (menos mineralizado) empieza a ser visible.
2.  **Ancho de Ventana (Window = 100):** Abarca el rango exacto de intensidades de `130 a 230`:
    *   Cualquier píxel con valor menor a 130 (tejido blando, grasa, aire) se fuerza a **0 (negro absoluto)**.
    *   Cualquier píxel mayor a 230 (zonas de hueso denso) se fuerza a **255 (blanco absoluto)**.
    *   *El resultado:* El contorno del tejido blando desaparece y la textura ósea se expande en toda la escala dinámica de grises de la pantalla para una visualización ultra-nítida.

---

## 2. Storytelling: El Pipeline de PDI Calibrado y Probado

### Paso 1: Window Leveling (Aislamiento Cortical)
*   **Parámetros:** `Window = 100`, `Level = 180`.
*   **Matemática PDI:** Estiramiento lineal del histograma restringido.
*   **Storytelling:** *"Apagamos la iluminación ambiental (tejido blando) y enfocamos un proyector directo sobre el hueso para inspeccionar su integridad cortical."*

### Paso 2: Filtro Gaussiano (Limpieza Cuántica)
*   **Parámetros:** `Kernel = 3x3`.
*   **Matemática PDI:** Convolución espacial con una máscara de Gauss. Se elige un kernel pequeño de 3x3 para evitar borrar las micro-trabéculas óseas del recién nacido.
*   **Storytelling:** *"El grano de la placa de Rayos X es como polvo sobre una lupa. Pasamos un filtro suave de 3x3 para remover el grano sin difuminar los bordes de la fractura."*

### Paso 3: CLAHE (Lupa de Contraste Adaptativo Local)
*   **Parámetros:** `ClipLimit = 3.0`, `TileGridSize = 8x8`.
*   **Matemática PDI:** Divide la radiografía en 64 sub-bloques autónomos de 8x8 píxeles. Estira localmente los contrastes y restringe la amplificación de ruido a un factor de 3.0 para evitar la saturación.
*   **Storytelling:** *"En lugar de iluminar toda la placa por igual, colocamos 64 linternas inteligentes en miniatura sobre el hueso. Cada una revela la textura ósea en su cuadrícula asignada, sacando a la luz micro-fisuras ocultas."*

### Paso 4: Realce de Bordes Laplaciano (Delineado de Discontinuidades)
*   **Parámetros:** `Filter = Laplacian`, `Alpha = 0.35` (Ganancia).
*   **Matemática PDI:** Derivada de segundo orden espacial para aislar variaciones de brillo de alta frecuencia (bordes). Se realiza una operación de máscara de desenfoque (*unsharp masking*) para superponer el gradiente sobre la imagen original.
*   **Storytelling:** *"Es nuestro marcador de precisión. Resalta los bordes óseos en blanco brillante y afila las fisuras, que aparecen como interrupciones negras afiladas. Esto hace evidente cualquier fractura al ojo no experto."*

---

## 3. Transformaciones Geométricas Espaciales (Rotaciones y Espejo)
### ¿Cómo manipulamos la orientación de la placa sin alterar sus píxeles?

En el uso clínico real, es común que la placa de Rayos X ingrese con rotaciones accidentales de 180° o en efecto espejo debido a la colocación del chasis por el técnico radiólogo.
*   **Sin distorsión:** Las rotaciones de exactamente 90°, 180° y 270°, así como el espejo horizontal, son **transformaciones espaciales puras**. Modifican la posición de los píxeles (mediante transposiciones de filas y columnas) pero **no escalan ni interpolan valores intermedios**, por lo cual **no existe pérdida de resolución ni deformación de los huesos**.
*   **Transformación de Coordenadas de Caja:** Cuando el usuario rota la placa, las coordenadas de la caja del Bounding Box de la fractura $[xmin, ymin, xmax, ymax]$ deben ser recalculadas con trigonometría discreta para alinearse al nuevo canvas de $640\times640$:
    *   *Espejo:* $xmin_{new} = 640 - xmax$ y $xmax_{new} = 640 - xmin$.
    *   *Rotación 180°:* $xmin_{new} = 640 - xmax$ y $ymin_{new} = 640 - ymax$ (y viceversa).
*   **Storytelling:** *"Es como girar una placa física de acetato bajo el negatoscopio clínico. El hueso y la sospecha marcada por la IA giran de la mano de forma matemática, garantizando que el diagnóstico siempre apunte al lugar anatómico correcto."*

---

## 4. Estrategia Híbrida: Diagnóstico IA (ViT) y Localización en la Consola

Para garantizar que nuestra aplicación sea 100% estable en servidores gratuitos en la nube (como Hugging Face Spaces en su CPU free-tier) sin requerir una GPU de alto costo, diseñamos un flujo híbrido:

1.  **Diagnóstico Global por IA (Vision Transformer - ViT):** 
    Utiliza el modelo preentrenado `Hemgg/bone-fracture-detection-using-xray`. La IA analiza los patrones de píxeles globales y clasifica la placa como "FRACTURA DETECTADA" o "NORMAL" con un porcentaje de certeza médica. Esto corre de forma instantánea en la CPU de Hugging Face.
2.  **Localización en Imágenes de Control:** 
    Los 15 ejemplos cargados en la base de datos de la consola médica tienen asociadas sus coordenadas reales de fractura del dataset GRAZPEDWRI-DX. Al seleccionarse, se dibuja un **Bounding Box interactivo** semitransparente que localiza físicamente la lesión para educar al médico y al jurado.
3.  **Localización en Imágenes Externas (Carga Libre):**
    Para imágenes subidas por el usuario en caliente, la IA clasifica globalmente y las herramientas de **PDI actúan como el localizador manual del clínico**. El médico (o usuario) utiliza el realce Laplaciano y los ajustes de ventana para ubicar la interrupción de la corteza ósea de forma directa.
4.  **Justificación de Escalabilidad Futura (ViT vs. YOLO):**
    *   **¿YOLO corre en Hugging Face Spaces?** Sí, un modelo de detección de objetos como YOLOv8 o YOLOv9 puede correr en CPU en HF Spaces. Sin embargo, para este MVP **no es factible en tiempo real** por cuestiones de recursos y latencia:
        *   *Latencia Crítica en CPU:* Gradio ejecuta la función de procesamiento en caliente cada vez que el usuario desplaza un slider PDI (Brillo, Contraste, Laplaciano). Si tuviéramos que correr inferencia de detección de objetos (YOLO) en CPU en cada movimiento del slider, la aplicación sufriría de un lag severo (varios segundos de congelamiento de pantalla por cada cambio).
        *   *Enfoque de la Materia (PDI):* El objetivo académico del proyecto es el Procesamiento Digital de Imágenes. Si la IA dibujara automáticamente la caja en todas las imágenes externas de forma infalible, el usuario no tendría incentivo para manipular los filtros de la consola. Delegar la localización en imágenes externas a los filtros PDI (Laplaciano y Ventana) hace que la consola funcione como un negatoscopio digital interactivo real.
    *   **¿Cómo se implementaría en producción?** En un entorno clínico real de producción, la arquitectura se escalaría montando un servidor de inferencia dedicado con GPU (usando Nvidia Triton o FastAPI en una instancia con aceleración por hardware). Allí, un modelo **YOLOv8-obb (Oriented Bounding Boxes)** o **DETR** detectaría y dibujaría las cajas de las microfracturas en caliente en menos de 50ms, sirviendo las coordenadas a la consola DICOM del médico de manera instantánea.
5.  **Storytelling:** *"La IA actúa como el médico de triaje, alertando '¡Cuidado, aquí hay una fractura al 98%!'. El procesamiento de imágenes de OpenCV actúa como la lupa del especialista, permitiendo resaltar los bordes para ver exactamente dónde está la lesión sin requerir hardware de supercomputación. En producción, añadiríamos un nodo GPU para que YOLO dibuje las cajas de forma automática en microsegundos, pero en este MVP, combinamos la IA de clasificación rápida con filtros PDI interactivos para mantener la interfaz fluida, rápida y didáctica."*
