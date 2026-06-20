import os
import cv2
from preprocessing import XRayPreprocessor

def run_pdi_test():
    print("=" * 60)
    print("  TEST LOCAL: Procesamiento Digital de Radiografías (PDI)")
    print("=" * 60)
    
    # 1. Definir rutas
    img_input_path = os.path.join("ejemplos", "fractura_1.jpg")
    output_dir = "resultados_test_pdi"
    os.makedirs(output_dir, exist_ok=True)
    
    # Verificar que la imagen existe
    if not os.path.exists(img_input_path):
        print(f"❌ ERROR: No se encontró la imagen de prueba en: {img_input_path}")
        print("Asegúrate de haber descargado las imágenes del Hito 1.")
        return
        
    print(f"📥 Cargando radiografía de prueba: {img_input_path}")
    
    try:
        # 2. Cargar imagen en escala de grises
        raw_img = XRayPreprocessor.load_image(img_input_path)
        print(f"   [OK] Imagen cargada. Dimensiones originales: {raw_img.shape[1]}x{raw_img.shape[0]}")
        cv2.imwrite(os.path.join(output_dir, "01_original_gris.jpg"), raw_img)
        
        # 3. Aplicar Window Leveling (Brillo y Contraste para Hueso)
        # Nivel alto (180) y ventana estrecha (100) para aislar tejido blando y resaltar densidad ósea
        windowed_img = XRayPreprocessor.apply_window_leveling(raw_img, window=100, level=180)
        print("   [OK] Filtro 1: Window Leveling aplicado (W=100, L=180).")
        cv2.imwrite(os.path.join(output_dir, "02_window_leveling.jpg"), windowed_img)
        
        # 4. Aplicar Suavizado Gaussiano (Remoción de Ruido)
        # Usamos un kernel pequeño de 3x3 para no borrar los detalles óseos finos
        blurred_img = XRayPreprocessor.apply_gaussian_blur(windowed_img, kernel_size=3)
        print("   [OK] Filtro 2: Suavizado Gaussiano aplicado (Kernel=3x3).")
        cv2.imwrite(os.path.join(output_dir, "03_suavizado_gaussiano.jpg"), blurred_img)
        
        # 5. Aplicar CLAHE (Realce de Contraste Adaptativo Local)
        # Clip limit de 3.0 para estirar el contraste y grilla local de 8x8 para micro-texturas
        clahe_img = XRayPreprocessor.apply_clahe(blurred_img, clip_limit=3.0, tile_grid_size=8)
        print("   [OK] Filtro 3: CLAHE aplicado (ClipLimit=3.0, Grid=8x8).")
        cv2.imwrite(os.path.join(output_dir, "04_clahe_local.jpg"), clahe_img)
        
        # 6. Aplicar Realce de Bordes (Laplaciano)
        # Restamos la derivada de segundo orden para delinear la corteza ósea de la fractura
        final_enhanced_img = XRayPreprocessor.apply_edge_enhancement(clahe_img, filter_type="laplacian", alpha=0.35)
        print("   [OK] Filtro 4: Realce de Bordes Laplaciano aplicado (Alpha=0.35).")
        cv2.imwrite(os.path.join(output_dir, "05_final_procesada.jpg"), final_enhanced_img)
        
        print("\n🎉 ¡PROCESAMIENTO DE PRUEBA COMPLETADO CON ÉXITO!")
        print(f"📂 Los resultados intermedios y finales se guardaron en: {os.path.abspath(output_dir)}")
        print("Detalle de archivos guardados:")
        print("  - 01_original_gris.jpg     -> Radiografía cargada limpia.")
        print("  - 02_window_leveling.jpg   -> Tejido blando eliminado, hueso contrastado.")
        print("  - 03_suavizado_gaussiano.jpg -> Grano y ruido cuántico removidos.")
        print("  - 04_clahe_local.jpg       -> Micro-detalles y trabéculas óseas realzados.")
        print("  - 05_final_procesada.jpg   -> Bordes de fracturas sutiles delineados.")
        
    except Exception as e:
        print(f"❌ ERROR durante la ejecución del test: {e}")

if __name__ == "__main__":
    run_pdi_test()
