import sys
import os
sys.path.append(os.path.abspath("."))

from app import process_and_diagnose

try:
    print("Corriendo prueba de process_and_diagnose sobre fractura_1.jpg...")
    res = process_and_diagnose(
        img_input=None,
        example_name="fractura_1.jpg",
        source_tab="gallery",
        rotation_str="0°",
        mirror=False,
        window=100,
        level=180,
        gaussian_blur=3,
        clahe_clip=3.0,
        clahe_grid=8,
        edge_filter="Laplacian",
        edge_alpha=0.35
    )
    print("¡Éxito sin excepciones!")
    print("Resultado:", res[2]) # Imprimir reporte HTML
except Exception as e:
    import traceback
    print("❌ EXCEPCIÓN DETECTADA:")
    traceback.print_exc()
