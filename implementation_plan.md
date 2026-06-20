# Plan de Implementación - Asistente Clínico de Diagnóstico de Fracturas en RX (PDI + Hugging Face)

Este proyecto desarrolla un **Asistente de Triaje Médico para Radiografías (RX)** enfocado en la detección de fracturas sutiles y microfracturas pediátricas y neonatales (difíciles de diagnosticar) a lo largo de diferentes perfiles de pacientes.

---

## 1. Justificación de los Marcadores Anatómicos Físicos (Letras R y L)

Durante la visualización de las placas (como en `sano_4.jpg`), se aprecian letras impresas en la radiografía como **R** (*Right* / Derecha) o **L** (*Left* / Izquierda). 
*   **Significado Médico:** Son marcadores anatómicos de plomo físicos colocados por el técnico radiólogo sobre el chasis al momento de la toma del Rayos X. 
*   **Propósito:** Garantizan la orientación anatómica correcta para evitar errores quirúrgicos o de diagnóstico de lateralidad.
*   **Impacto en PDI/IA:** Estas marcas son nativas del proceso clínico de captura y **no constituyen anotaciones de ayuda visual digital** (como flechas de diagnóstico). Por lo tanto, no representan ruido artificial ni alteran la reproducibilidad médica del MVP; al contrario, emulan fielmente el entorno clínico real.

---

## 2. Convivencia de Entornos y Configuración Local Realizada

El entorno de desarrollo local se ha configurado de manera exitosa para convivir limpiamente con Docker:
*   **Creación del Entorno Virtual:** Se inicializó el entorno virtual local mediante el gestor de alta velocidad `uv` ejecutando:
    ```bash
    uv venv .venv
    ```
*   **Instalación de Dependencias de Soporte:** Se instalaron las dependencias esenciales para la obtención y validación de imágenes:
    ```bash
    uv pip install huggingface_hub datasets pillow
    ```
*   **Aislamiento de Docker:** Se creará un archivo `.dockerignore` para excluir la carpeta `.venv` local del contenedor, asegurando que Docker compile un sistema totalmente independiente y reproducible en Hugging Face Spaces.

---

## 3. Repositorio de Imágenes Clínicas de Prueba

Las 15 imágenes clínicas de alta calidad fueron obtenidas de forma automatizada desde el dataset público **`LibreYOLO/bone-fracture-7fylg`** de Hugging Face (que proviene del benchmark académico internacional de trauma pediátrico **GRAZPEDWRI-DX** de la Universidad Médica de Graz).

### Detalles del Procesamiento y Descarga:
1.  **Resolución Nativa:** Las imágenes se obtuvieron en su resolución original de **`640x640` píxeles**, libre de rotaciones o augmentaciones artificiales perjudiciales para el análisis de PDI.
2.  **Clasificación por Etiquetas:** Se analizó el archivo de anotaciones de coordenadas de cada imagen:
    *   Si el archivo de etiquetas presentaba coordenadas, se clasificó como **Fracturado** (`fractura_*.jpg`).
    *   Si el archivo de etiquetas estaba vacío, se validó como hueso de control **Sano** (`sano_*.jpg`).
3.  **Higiene Visual:** Las imágenes están libres de flechas rojas u otras marcas de diagnóstico digital humano, siendo aptas para el tratamiento puro en OpenCV.

---

## 4. Estructura de Archivos del Proyecto

La carpeta de trabajo `/home/farfaneduardo/Documentos/Proyectos/pdi_deteccion_rx` cuenta con la siguiente estructura:

```text
pdi_deteccion_rx/
├── .venv/                      # Entorno virtual local (uv)
├── ejemplos/                   # 15 imágenes de alta calidad (640x640)
│   ├── fractura_1.jpg al fractura_10.jpg
│   └── sano_1.jpg al sano_5.jpg
├── implementation_plan.md      # Este plan de implementación actualizado
├── app.py                      # (Pendiente) Interfaz de Gradio
├── preprocessing.py            # (Pendiente) Módulo de PDI con OpenCV
├── Dockerfile                  # (Pendiente) Dockerfile
├── docker-compose.yml          # (Pendiente) Docker compose
├── requirements.txt            # (Pendiente) Dependencias
└── LSGonzález-TFG-IC-2021.pdf  # Referencia científica
```

---

## 5. Calendario de Actividades y Avance

### Fase 1: Setup e Imágenes (Miércoles 17) - [COMPLETADA]
*   **Miércoles 17 (Hoy):**
    *   [x] Aprobación y reestructuración del Plan.
    *   [x] Inicialización del entorno virtual `.venv` con `uv`.
    *   [x] Creación de la carpeta `/ejemplos/`.
    *   [x] Descarga y validación dimensional (`640x640`) de las 15 imágenes clínicas limpias de Hugging Face.

### Fase 2: Módulo de PDI (Jueves 18) - [SIGUIENTE HITO]
*   **Jueves 18 (Tus horas: 19:00 a 23:00 - 4 hs):**
    *   [ ] Desarrollo de `preprocessing.py`: Crear las funciones matemáticas con OpenCV (Window Leveling, CLAHE, Filtros Gaussianos y realce Laplaciano/Sobel).
    *   [ ] Crear script rápido en local para validar el procesamiento matemático e interactivo.

### Fase 3: Integración de IA y Gradio (Sábado 20)
*   **Sábado 20 (Tus horas: 08:00 a 22:00 - 14 hs):**
    *   [ ] Integración del modelo de IA Vision Transformer para clasificación de fracturas.
    *   [ ] Desarrollo de la interfaz de consola DICOM en Gradio (`app.py`).
    *   [ ] Creación de `Dockerfile` y `docker-compose.yml` en la raíz. Pruebas locales de Docker.

### Fase 4: Despliegue y Documentación (Domingo 21 - Lunes 22)
*   [ ] Despliegue en Hugging Face Spaces vía Git/Docker.
*   [ ] Redacción de la documentación científica en `README.md`.
