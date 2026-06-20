import cv2
import numpy as np

class XRayPreprocessor:
    """
    Clase encargada del Procesamiento Digital de Imágenes (PDI) para placas de Rayos X.
    Contiene el pipeline de filtros interactivos emulando una consola médica DICOM.
    """
    
    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        """
        Carga una imagen desde el disco duro en escala de grises (1 solo canal de 8-bits).
        Es el formato estándar requerido para el análisis radiológico digital.
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {image_path}")
        return image

    @staticmethod
    def apply_window_leveling(image: np.ndarray, window: float, level: float) -> np.ndarray:
        """
        Aplica Window Leveling (Ajuste de Ventana y Nivel) lineal sobre la matriz de píxeles.
        
        Matemática del proceso:
        1. Se calcula el rango de interés: [mínimo = L - W/2, máximo = L + W/2].
        2. Los valores por debajo del mínimo se truncan a 0 (negro absoluto / tejido blando).
        3. Los valores por encima del máximo se truncan a 255 (blanco absoluto / hiperdenso).
        4. El rango intermedio se escala de forma lineal ocupando todo el espectro visual de 8 bits.
        """
        # Calcular los límites inferior y superior de la ventana
        min_val = level - (window / 2.0)
        max_val = level + (window / 2.0)
        
        # Evitar división por cero
        if max_val == min_val:
            max_val += 1.0
            
        # Aplicar transformación lineal: f(x) = (x - min) * (255 / (max - min))
        output = (image.astype(np.float32) - min_val) * (255.0 / (max_val - min_val))
        
        # Truncar/Saturar los valores en el rango [0, 255] y convertir a uint8
        output = np.clip(output, 0, 255).astype(np.uint8)
        return output

    @staticmethod
    def apply_gaussian_blur(image: np.ndarray, kernel_size: int) -> np.ndarray:
        """
        Aplica un filtro Gaussiano bidimensional para suavizar el ruido de fotones (grano de sal y pimienta).
        
        Matemática: Realiza una convolución espacial de la imagen con una máscara de Gauss.
        El kernel_size debe ser un número entero impar (ej. 3, 5, 7) para tener un píxel central de referencia.
        """
        if kernel_size <= 0:
            return image
            
        # Asegurar que el kernel_size sea impar
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    @staticmethod
    def apply_clahe(image: np.ndarray, clip_limit: float, tile_grid_size: int) -> np.ndarray:
        """
        CLAHE (Contrast Limited Adaptive Histogram Equalization).
        Ecualiza el contraste de forma local dividiendo la imagen en bloques (tiles) de tamaño NXN.
        El parámetro clip_limit limita la amplificación de contraste para no generar artefactos de ruido.
        """
        if clip_limit <= 0 or tile_grid_size <= 1:
            return image
            
        # Crear el objeto CLAHE de OpenCV
        clahe = cv2.createCLAHE(
            clipLimit=clip_limit, 
            tileGridSize=(tile_grid_size, tile_grid_size)
        )
        return clahe.apply(image)

    @staticmethod
    def apply_edge_enhancement(image: np.ndarray, filter_type: str, alpha: float) -> np.ndarray:
        """
        Aplica realce de bordes (filtros de gradiente) para delinear discontinuidades óseas (fracturas).
        
        Tipos de filtros:
        1. 'Laplacian': Derivada de segundo orden. Ideal para detectar líneas finas de fracturas.
           Se suma (o resta) a la imagen original multiplicada por una ganancia 'alpha' (Unsharp Masking).
        2. 'Sobel': Derivadas de primer orden en X e Y para resaltar bordes direccionales.
        """
        if alpha <= 0:
            return image
            
        if filter_type.lower() == 'laplacian':
            # Obtener el Laplaciano en alta precisión de punto flotante (CV_64F) para evitar overflow
            laplacian = cv2.Laplacian(image, cv2.CV_64F)
            
            # Sumar el gradiente a la imagen original para realzar los detalles
            # f_realzada = f_original - alpha * laplacian (el signo depende de la convención de la máscara)
            enhanced = image.astype(np.float64) - (alpha * laplacian)
            
            # Recortar en el rango de 8-bits y convertir
            return cv2.convertScaleAbs(enhanced)
            
        elif filter_type.lower() == 'sobel':
            # Derivada horizontal (X) y vertical (Y)
            sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
            
            # Calcular la magnitud del gradiente: mag = sqrt(x^2 + y^2)
            magnitude = cv2.magnitude(sobel_x, sobel_y)
            
            # Combinar la magnitud (bordes detectados) con la imagen original usando alpha
            combined = image.astype(np.float64) + (alpha * magnitude)
            return cv2.convertScaleAbs(combined)
            
        return image
