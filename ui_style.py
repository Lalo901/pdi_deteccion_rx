# --- Estilos CSS e Interacciones JavaScript de la Interfaz ---

# CSS para el estilo oscuro de la consola clínica
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

body, .gradio-container, input, button, select, textarea, span, p, h1, h2, h3, div, table, td, tr {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

:root, .gradio-container {
    --primary-50: #ecfeff !important;
    --primary-100: #cffafe !important;
    --primary-200: #a5f3fc !important;
    --primary-300: #67e8f9 !important;
    --primary-400: #22d3ee !important;
    --primary-500: #0ea5e9 !important;
    --primary-600: #0284c7 !important;
    --primary-700: #0369a1 !important;
    
    --body-background-fill: #090d16 !important;
    --background-fill-primary: #0f172a !important;
    --background-fill-secondary: #0b0f19 !important;
    --border-color-primary: #1e293b !important;
    --border-color-secondary: #1e293b !important;
    --body-text-color: #f1f5f9 !important;
    --body-text-color-subdued: #94a3b8 !important;
    
    --input-background-fill: #0b0f19 !important;
    --input-border-color: #1e293b !important;
    --input-border-color-focus: #0ea5e9 !important;
}

/* Bordes redondeados consistentes para todos los paneles, grupos y formularios de Gradio */
.sidebar-panel, .report-panel, .gradio-container .block, .gradio-container .form, .gradio-container .group {
    border-radius: 16px !important;
}

.report-panel {
    background-color: #0f172a !important;
    border: 1px solid #1e293b !important;
    padding: 20px !important;
}
.sidebar-panel {
    background-color: #0b0f19 !important;
    border: 1px solid #1f2937 !important;
    padding: 16px !important;
}
/* Evitar el auto-zoom molesto al hacer click en las cajas de la imagen procesada */
.gradio-container .annotation-container,
.gradio-container .annotation,
.gradio-container div[style*="absolute"] {
    pointer-events: none !important;
}
/* Pero reactivar pointer-events para los botones de la barra de herramientas del visualizador */
.gradio-container .button-layout, 
.gradio-container button {
    pointer-events: auto !important;
}
/* Asegurar que el contenedor recorte las imágenes con zoom y no desborde la UI */
#original_view, #annotated_view {
    overflow: hidden !important;
}
#original_view img, #annotated_view img {
    max-width: 100% !important;
    max-height: 100% !important;
    object-fit: contain !important;
}

/* Cabeceras de Sección Clínicas */
.section-header {
    border-left: 3.5px solid #0ea5e9 !important;
    padding-left: 10px !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    margin-bottom: 14px !important;
    margin-top: 8px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.75px !important;
}

/* Indicadores de alerta con animación */
@keyframes pulse {
    0% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
    }
    70% {
        transform: scale(1.1);
        box-shadow: 0 0 0 6px rgba(239, 68, 68, 0);
    }
    100% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
    }
}
.pulsing-dot-red {
    display: inline-block;
    width: 9px;
    height: 9px;
    background-color: #ef4444;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 1.8s infinite;
}
.dot-green {
    display: inline-block;
    width: 9px;
    height: 9px;
    background-color: #10b981;
    border-radius: 50%;
    margin-right: 8px;
    box-shadow: 0 0 8px #10b981;
}
"""

# JavaScript para el zoom y paneo interactivo en el navegador
js_code = """
(function() {
    console.log("[DICOM Zoom] Cargando módulo de zoom y paneo interactivo...");
    const initZoomPan = () => {
        const viewers = ['original_view', 'annotated_view'];
        viewers.forEach(id => {
            const container = document.getElementById(id);
            if (!container) {
                console.log("[DICOM Zoom] Esperando contenedor: " + id);
                return;
            }
            
            // Si ya fue inicializado, evitar duplicar listeners
            if (container.dataset.zoomInitialized === "true") return;
            container.dataset.zoomInitialized = "true";
            
            console.log("[DICOM Zoom] Inicializando visor: " + id);
            let scale = 1;
            let isDragging = false;
            let startX = 0, startY = 0;
            let translateX = 0, translateY = 0;
            
            const getImg = () => container.querySelector('img');
            
            const update = () => {
                const img = getImg();
                if (img) {
                    img.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
                    img.style.transformOrigin = 'center center';
                    img.style.transition = isDragging ? 'none' : 'transform 0.1s ease-out';
                    img.style.cursor = scale > 1 ? (isDragging ? 'grabbing' : 'grab') : 'zoom-in';
                }
            };
            
            // Escuchar el evento wheel en modo captura y sin pasividad para poder hacer preventDefault
            container.addEventListener('wheel', (e) => {
                const img = getImg();
                if (!img) return;
                
                e.preventDefault();
                const zoomFactor = 0.2;
                if (e.deltaY < 0) {
                    scale += zoomFactor;
                } else {
                    scale -= zoomFactor;
                }
                
                scale = Math.max(1, Math.min(scale, 5));
                if (scale === 1) {
                    translateX = 0;
                    translateY = 0;
                }
                update();
            }, { passive: false });
            
            container.addEventListener('mousedown', (e) => {
                const img = getImg();
                if (!img || scale <= 1) return;
                
                e.preventDefault();
                isDragging = true;
                startX = e.clientX - translateX;
                startY = e.clientY - translateY;
                update();
            });
            
            window.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                translateX = e.clientX - startX;
                translateY = e.clientY - startY;
                update();
            });
            
            window.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    update();
                }
            });
            
            container.addEventListener('dblclick', () => {
                scale = 1;
                translateX = 0;
                translateY = 0;
                update();
            });
            
            // Observar cambios internos para aplicar propiedades a nuevas imágenes cargadas por Gradio
            const observer = new MutationObserver(() => {
                const img = getImg();
                if (img) {
                    img.draggable = false;
                    img.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
                    update();
                }
            });
            observer.observe(container, { childList: true, subtree: true });
            
            const img = getImg();
            if (img) {
                img.draggable = false;
                img.style.cursor = 'zoom-in';
            }
        });
    };
    
    // Intentar inicializar periódicamente por si Gradio tarda en cargar
    setTimeout(initZoomPan, 1000);
    const interval = setInterval(() => {
        if (document.getElementById('original_view') && document.getElementById('annotated_view')) {
            initZoomPan();
        }
    }, 1000);
})();
"""
