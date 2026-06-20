import os
import json
from huggingface_hub import HfApi, hf_hub_download

def generate_labels():
    repo = "LibreYOLO/bone-fracture-7fylg"
    output_json = os.path.join("ejemplos", "labels.json")
    
    print("Conectando con Hugging Face Hub para obtener coordenadas...")
    api = HfApi()
    try:
        files = api.list_repo_files(repo_id=repo, repo_type="dataset")
    except Exception as e:
        print(f"Error al listar archivos del repo: {e}")
        return
        
    img_files = sorted([f for f in files if f.startswith("test/images/") and f.endswith(".jpg")])
    label_files = sorted([f for f in files if f.startswith("test/labels/") and f.endswith(".txt")])
    
    fractura_count = 0
    sano_count = 0
    
    label_data = {}
    
    # 5 imágenes que simularemos que están rotadas 180 grados en la base de datos
    # para que la app las auto-rote en el inicio
    rotated_examples = {
        "fractura_2.jpg": 180,
        "fractura_5.jpg": 180,
        "fractura_8.jpg": 180,
        "sano_1.jpg": 180,
        "sano_4.jpg": 180
    }
    
    for img_file in img_files:
        if fractura_count >= 10 and sano_count >= 5:
            break
            
        base_name = os.path.basename(img_file).replace(".jpg", "")
        corresponding_label = f"test/labels/{base_name}.txt"
        
        if corresponding_label in label_files:
            try:
                # Descargar etiqueta para verificar si está vacía
                label_path = hf_hub_download(repo_id=repo, filename=corresponding_label, repo_type="dataset", local_dir=".")
                
                is_fractured = False
                boxes = []
                if os.path.exists(label_path):
                    with open(label_path, "r") as f:
                        lines = f.readlines()
                        for line in lines:
                            line = line.strip()
                            if line:
                                is_fractured = True
                                parts = line.split()
                                if len(parts) >= 5:
                                    # YOLO format: class x_center y_center width height
                                    cls = int(parts[0])
                                    x_c = float(parts[1])
                                    y_c = float(parts[2])
                                    w = float(parts[3])
                                    h = float(parts[4])
                                    
                                    # Convert to 640x640 absolute coordinates
                                    xmin = int((x_c - w / 2.0) * 640.0)
                                    ymin = int((y_c - h / 2.0) * 640.0)
                                    xmax = int((x_c + w / 2.0) * 640.0)
                                    ymax = int((y_c + h / 2.0) * 640.0)
                                    
                                    # Asegurar límites del canvas
                                    xmin = max(0, min(xmin, 640))
                                    ymin = max(0, min(ymin, 640))
                                    xmax = max(0, min(xmax, 640))
                                    ymax = max(0, min(ymax, 640))
                                    
                                    boxes.append({
                                        "box": [xmin, ymin, xmax, ymax],
                                        "label": "FRACTURA"
                                    })
                                    
                    os.remove(label_path)
                
                if is_fractured and fractura_count < 10:
                    fractura_count += 1
                    filename = f"fractura_{fractura_count}.jpg"
                    label_data[filename] = {
                        "type": "fractura",
                        "initial_rotation": rotated_examples.get(filename, 0),
                        "boxes": boxes
                    }
                    print(f"Mapped {filename} with {len(boxes)} boxes.")
                    
                elif not is_fractured and sano_count < 5:
                    sano_count += 1
                    filename = f"sano_{sano_count}.jpg"
                    label_data[filename] = {
                        "type": "sano",
                        "initial_rotation": rotated_examples.get(filename, 0),
                        "boxes": []
                    }
                    print(f"Mapped {filename} as healthy.")
                    
            except Exception as e:
                print(f"Error procesando {base_name}: {e}")
                
    # Agregar neonato_clavicula.jpeg como sano de control de ejemplo o manual
    label_data["neonato_clavicula.jpeg"] = {
        "type": "sano",
        "initial_rotation": 0,
        "boxes": []
    }
    
    # Limpieza
    if os.path.exists("test"):
        import shutil
        shutil.rmtree("test")
        
    # Guardar en archivo JSON
    with open(output_json, "w") as f:
        json.dump(label_data, f, indent=4)
        
    print(f"¡Cajas de etiquetas generadas con éxito en: {output_json}!")

if __name__ == "__main__":
    generate_labels()
