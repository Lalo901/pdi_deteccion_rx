---
title: Asistente Clinico de Diagnostico de Fracturas en RX
emoji: 🩻
colorFrom: blue
colorTo: slate
sdk: docker
app_port: 7860
pinned: false
---

# Asistente Clínico de Diagnóstico de Fracturas en RX (PDI + Hugging Face)
## Laboratorio Integrador - Materia: Procesamiento Digital de Imágenes

Este repositorio contiene el MVP de un asistente de diagnóstico asistido por IA para radiografías (RX) pediátricas y neonatales, enfocado en microfracturas y lesiones obstétricas de nacimiento. El sistema simula una consola médica DICOM permitiendo la manipulación interactiva de las imágenes para realzar bordes óseos mediante PDI antes de su análisis automático.

---

## 👥 Integrantes del Equipo
*   **Eduardo Farfán** (Desarrollo Individual)
*   **Materia:** Procesamiento Digital de Imágenes
*   **Cátedra/Institución:** Tecnicatura Superior en Ciencias de Datos e IA (IFTS24)
*   **Profesor:** Matias Barreto
*   **Ayudante de Cátedra:** Cynthia Villagra

---

## 📁 Estructura del Proyecto

La arquitectura del repositorio está diseñada de forma plana para garantizar el despliegue directo en Hugging Face Spaces usando Docker:

```text
pdi_deteccion_rx/
├── .venv/                      # Entorno virtual local (uv)
├── ejemplos/                   # Galería de imágenes médicas de control (640x640)
│   ├── fractura_1.jpg al fractura_10.jpg
│   ├── sano_1.jpg al sano_5.jpg
│   └── labels.json             # Metadatos de coordenadas e inversiones anatómicas
├── ejemplos_externos/          # [NUEVO] 5 imágenes crudas para prueba de carga libre
│   ├── externo_sano_neonato_1.jpg al 2.jpg
│   ├── externo_frac_neonato_1.jpg
│   └── externo_frac_pediatrico_1.jpg al 2.jpg
├── implementation_plan.md      # Plan de implementación técnica (mentor)
├── deteccionRx.md              # Directrices del proyecto y cronograma académico
├── tecnica_procesing.md        # Guía teórica y conceptos de PDI para la defensa
├── README.md                   # Este archivo (Metadatos de Hugging Face y documentación)
├── app.py                      # Interfaz en Gradio y orquestación del flujo
├── preprocessing.py            # Módulo de Procesamiento Digital de Imágenes (PDI) con OpenCV
├── Dockerfile                  # Definición del contenedor de producción
├── docker-compose.yml          # Ejecución local en Docker
└── requirements.txt            # Dependencias del proyecto
```

---

## 🚀 Guía de Reproducibilidad (Cómo ejecutar en local)

Este proyecto puede ejecutarse de dos maneras en tu máquina local. Se recomienda tener instalado **Docker** o el gestor **`uv`** de Python.

### Opción A: Ejecución Local en Contenedor (Docker) - Recomendado
Garantiza que la aplicación se ejecute en un entorno idéntico al de Hugging Face Spaces.
```bash
# 1. Clonar el repositorio
git clone https://github.com/farfaneduardo/pdi_deteccion_rx.git
cd pdi_deteccion_rx

# 2. Construir e iniciar el contenedor local
docker compose up --build
```
Una vez iniciado, abre tu navegador en **`http://localhost:7860`**.

### Opción B: Ejecución en Entorno Local (Python + uv)
Ideal para desarrollo rápido y pruebas en tiempo real de los filtros.
```bash
# 1. Crear el entorno virtual
uv venv .venv

# 2. Activar el entorno
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Instalar dependencias
uv pip install -r requirements.txt

# 4. Iniciar la aplicación local
python app.py
```
Una vez iniciado, abre tu navegador en **`http://localhost:7860`**.

---

## 🔬 Metodología PDI Aplicada
Para compensar la baja mineralización de los huesos neonatales y eliminar el ruido del sensor de RX, el sistema aplica en cadena:
1.  **Ajuste Geométrico:** Rotaciones espaciales puras de `0°`, `90°`, `180°`, `270°` y efecto espejo que reordenan la matriz de píxeles sin interpolación destructiva, adaptando las cajas de diagnóstico dinámicamente.
2.  **Window Leveling (Ajuste de Ventana):** Mapeo de la intensidad de 12-16 bits a los 8 bits de pantalla (W=100, L=180) para aislar el tejido óseo del blando.
3.  **Suavizado Gaussiano:** Remoción de ruido cuántico de fotones en la placa.
4.  **CLAHE:** Ecualización local del contraste en cuadrículas de 8x8 para destacar fisuras milimétricas.
5.  **Laplaciano/Sobel:** Resaltado de discontinuidades en la corteza ósea (detección de bordes de fracturas).

---

## 🏥 Triage Híbrido e IA
El MVP combina:
*   **Inferencia en Tiempo Real (IA):** Clasificación binaria (Fractura / Sano) en CPU con el Vision Transformer `Hemgg/bone-fracture-detection-using-xray`.
*   **Localización Asistida:** Dibuja cajas delimitadoras (*Bounding Boxes*) para los 15 casos de la base de ejemplos y delega la localización manual al clínico (asistido por filtros de bordes PDI) en cargas de radiografías externas, protegiendo los límites de RAM del servidor en la nube.

---

## 📦 Origen de las Imágenes de Prueba (Dataset)

Todas las imágenes utilizadas para validar la consola (tanto los ejemplos predeterminados como los archivos de prueba externos) provienen del dataset público de Hugging Face **`LibreYOLO/bone-fracture-7fylg`**, el cual está basado en el dataset clínico y benchmark académico internacional **GRAZPEDWRI-DX** de la Universidad Médica de Graz.

### 1. Galería de Ejemplos de Control (`ejemplos/`)
Consta de **15 imágenes** seleccionadas de diáfisis pediátricas y neonatales (10 fracturas y 5 sanas) que cuentan con localización activa mediante cajas delimitadoras (`labels.json`):
*   **Imágenes con Fractura (10):** `fractura_1.jpg` a `fractura_10.jpg`
*   **Imágenes Sanas (5):** `sano_1.jpg` a `sano_5.jpg`

### 2. Imágenes Crudas de Carga Externa (`ejemplos_externos/`)
Consta de **5 imágenes** descargadas en su estado nativo crudo (sin procesamiento ni marcas y fuera del conjunto de ejemplos) diseñadas para probar la robustez del cargador libre de la consola médica y la predicción de clasificación en CPU:
*   `externo_sano_neonato_1.jpg`: Diáfisis neonatal sana, sin núcleos carpianos visibles en muñeca.
*   `externo_sano_neonato_2.jpg`: Segunda diáfisis neonatal sana.
*   `externo_frac_neonato_1.jpg`: Fractura en la diáfisis del radio en paciente neonatal.
*   `externo_frac_pediatrico_1.jpg`: Fractura en la diáfisis de cúbito/radio en paciente pediátrico (núcleos carpianos en desarrollo visibles).
*   `externo_frac_pediatrico_2.jpg`: Fractura desplazada en la diáfisis en paciente pediátrico.
