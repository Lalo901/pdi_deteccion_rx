# Asistente Clínico de Diagnóstico de Fracturas en RX (PDI + Hugging Face)
## Directrices del Proyecto y Arquitectura del MVP

Este documento centraliza los requerimientos, el cronograma oficial y las especificaciones técnicas del MVP. Se utiliza como referencia constante para el desarrollo diario y la alineación académica.

---

## 1. Directrices Académicas y Cronograma Oficial

### Hito 1: Entrega del Laboratorio Integrador (Trabajo Práctico 2)
*   **Fecha Límite:** Martes 23 de junio
*   **Línea de Trabajo Elegida:** **Línea 2: Tareas y modelos de Hugging Face.**
*   **Requisitos Obligatorios:**
    *   Despliegue (*deploy*) de la aplicación en **Hugging Face Spaces**.
    *   Uso de **Gradio** como librería de desarrollo e interfaz de usuario.
    *   Creación de un repositorio específico para este desarrollo en **GitHub**.
    *   Archivo `README.md` claro, completo y profesional que indique:
        *   Propósito del desarrollo y contexto.
        *   Integrantes del equipo (Desarrollo Individual: Eduardo Farfán).
        *   Instrucciones para garantizar la **reproducibilidad** y el entendimiento del proyecto.
*   **Valor Agregado:**
    *   La aplicación de conocimientos sobre **Docker** para el empaquetado y despliegue (suma valor pero no es excluyente).
*   **Instancia de Evaluación:** Defensa y corrección grupal en una sesión remota.

> [!CAUTION]
> **CONDICIONALIDAD EXCLUYENTE:** 
> La aprobación y entrega del Laboratorio Integrador (Hito 1 - 23 de Junio) es una condición obligatoria y eliminatoria. Si no se entrega o no se aprueba este MVP, se pierde el derecho a rendir la Evaluación Presencial Teórica del 30 de Junio. Ambos hitos se complementan, siendo el primero la llave de acceso al segundo.

### Hito 2: Evaluación Presencial (Aspectos Teóricos)
*   **Fecha:** Martes 30 de junio
*   **Modalidad:** Examen de opción múltiple (*multiple choice*) de 10 preguntas.
*   **Temas a Cubrir (Fundamentos de Clase):**
    *   Diferenciación técnica al trabajar con espacios de color **RGB y HSV** (¡importante repasar para PDI!).
    *   Fundamentos de redes neuronales y visión por computadora.
    *   Conceptos teóricos de procesamiento digital de imágenes desarrollados en clase.

---

## 2. Objetivo del MVP (Consola DICOM + IA Neonatal)

El sistema está diseñado como una **herramienta de apoyo al triaje radiológico** para médicos especialistas y generalistas. Se enfoca especialmente en la detección de:
1.  **Traumatismos óseos neonatales por parto/cesárea:** Fracturas diafisiarias sutiles (fémur, húmero y clavícula) que ocurren durante extracciones difíciles o distocia de hombros.
2.  **Fracturas y fisis pediátricas:** Apoyo en la diferenciación geométrica entre cartílagos de crecimiento normales (fisis) y fracturas reales (ej. Salter-Harris o tallo verde), las cuales son causas comunes de falsos positivos en diagnóstico infantil.

El MVP consta de un **Visualizador DICOM interactivo (PDI en OpenCV)** donde el médico manipula la radiografía en tiempo real para contrastar bordes, y un **Módulo Predictivo (IA en Hugging Face)** que analiza la placa e indica sospechas de fractura.

---

## 3. Stack Tecnológico e Infraestructura

*   **Entorno Virtual local:** Gestionado con `uv` (alto rendimiento).
*   **Preprocesamiento de Imagen (PDI):** `OpenCV` (brillo/contraste, CLAHE, reducción de ruido con filtros gaussianos y realce de bordes laplaciano).
*   **Modelos de IA:** `transformers` de Hugging Face (utilizando el Vision Transformer `Hemgg/bone-fracture-detection-using-xray`).
*   **Interfaz de Usuario (UI):** `Gradio` (estilo consola clínica oscura).
*   **Empaquetado y Despliegue:** `Docker` (con `Dockerfile` y `docker-compose.yml` en la raíz del repositorio).

---

## 4. Estructura de Archivos del Proyecto

La estructura real de archivos en el directorio `/home/farfaneduardo/Documentos/Proyectos/pdi_deteccion_rx` es la siguiente:

```text
pdi_deteccion_rx/
├── .venv/                      # Entorno virtual local (uv)
├── ejemplos/                   # 15 imágenes clínicas de alta resolución (640x640)
│   ├── fractura_1.jpg al fractura_10.jpg
│   └── sano_1.jpg al sano_5.jpg
├── implementation_plan.md      # Plan de implementación detallado del mentor
├── deteccionRx.md              # Este documento (Directrices del proyecto)
├── app.py                      # [Pendiente] Código principal de Gradio (Sábado 20)
├── preprocessing.py            # [Pendiente] Módulo de PDI con OpenCV (Jueves 18)
├── Dockerfile                  # [Pendiente] Configuración del contenedor (Sábado 20)
├── docker-compose.yml          # [Pendiente] Orquestación local (Sábado 20)
└── requirements.txt            # [Pendiente] Dependencias (Sábado 20)
```

---

## 5. Plan de Ejecución y Estado del MVP

*   [x] **Paso 1:** Configurar infraestructura de desarrollo local con `uv venv`. (Miércoles 17)
*   [x] **Paso 2:** Obtener e indexar 15 imágenes clínicas pediátricas/neonatales limpias en resolución `640x640` desde Hugging Face Datasets. (Miércoles 17)
*   [ ] **Paso 3 (Hoy - Jueves 18):** Desarrollar las funciones del pipeline de PDI en `preprocessing.py` y validarlas con un script de test local.
*   [ ] **Paso 4 (Sábado 20):** Desarrollar la interfaz web interactiva en Gradio (`app.py`), integrar el modelo Vision Transformer de Hugging Face y escribir la dockerización (`Dockerfile` / `docker-compose.yml`).
*   [ ] **Paso 5 (Domingo 21 - Lunes 22):** Desplegar en Hugging Face Spaces y redactar la documentación oficial de reproducibilidad en `README.md`.
*   [ ] **Paso 6 (Martes 23):** Entrega del Laboratorio Integrador.
