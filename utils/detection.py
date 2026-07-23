"""
Detection logic
"""
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from utils.model_loader import get_model
from config import CONFIDENCE_THRESHOLD, CLASS_NAMES


# ====== WARNA BOUNDING BOX PER KELAS ======
COLORS = {
    'matang': (0, 255, 0),          # Hijau
    'setengah_matang': (0, 0, 255), # Merah
    
}

# Warna default jika kelas tidak dikenal
DEFAULT_COLOR = (232, 105, 48)  # Oranye


def run_detection(image):
    """Run deteksi pada gambar"""
    try:
        model = get_model()
        if model is None:
            return {
                'success': False,
                'error': 'Model tidak berhasil dimuat'
            }
        
        # Run inference
        results = model.predict(image, conf=CONFIDENCE_THRESHOLD)
        
        if results is None or len(results) == 0:
            return {
                'success': False,
                'error': 'Deteksi gagal'
            }
        
        # Process results
        result = results[0]
        detections = []
        
        if result.boxes is not None and len(result.boxes) > 0:
            for i, box in enumerate(result.boxes):
                confidence = float(box.conf[0]) if len(box.conf) > 0 else 0
                class_id = int(box.cls[0]) if len(box.cls) > 0 else -1
                
                detection = {
                    'id': i,
                    'class': CLASS_NAMES.get(class_id, 'Unknown'),
                    'confidence': confidence,
                    'box': box.xyxy[0].cpu().numpy().tolist() if hasattr(box, 'xyxy') else []
                }
                detections.append(detection)
        
        # Get annotated image
        annotated_image = result.plot()
        
        return {
            'success': True,
            'detections': detections,
            'count': len(detections),
            'image': annotated_image,
            'raw_result': result
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def process_detection_results(detection_result):
    """Process detection results untuk ditampilkan"""
    if not detection_result.get('success'):
        return None
    
    detections = detection_result.get('detections', [])
    
    # Group by class
    classes_count = {}
    for det in detections:
        class_name = det['class']
        classes_count[class_name] = classes_count.get(class_name, 0) + 1
    
    # Calculate average confidence
    confidences = [det['confidence'] for det in detections]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        'total_detections': len(detections),
        'classes_count': classes_count,
        'average_confidence': avg_confidence,
        'detections': detections
    }


def draw_detections_on_image(image, results, model, conf_threshold=0.5):
    """
    Draw detections on image dengan warna berbeda per kelas
    
    Args:
        image: PIL Image or numpy array
        results: YOLO detection results
        model: YOLO model
        conf_threshold: Confidence threshold
    
    Returns:
        tuple: (annotated_image, stats)
    """
    # Convert PIL to numpy if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image.copy()
    
    # Convert RGB to BGR for OpenCV
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = img_array
    
    stats = {
        'total': 0,
        'confidences': [],
        'class_distribution': {},
        'class_confidence': {},
        'detections': []
    }
    
    # Process results
    for result in results:
        if hasattr(result, 'boxes') and result.boxes is not None:
            boxes = result.boxes
            
            for box in boxes:
                conf = float(box.conf[0])
                if conf >= conf_threshold:
                    cls_id = int(box.cls[0])
                    cls_name = model.names.get(cls_id, CLASS_NAMES.get(cls_id, 'Unknown'))
                    
                    # ====== TENTUKAN WARNA BERDASARKAN KELAS ======
                    # Warna dalam format BGR untuk OpenCV
                    if cls_name in COLORS:
                        color_bgr = COLORS[cls_name]  # Sudah dalam format BGR
                    else:
                        color_bgr = DEFAULT_COLOR  # Oranye
                    
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    
                    # ====== GAMBAR BOUNDING BOX DENGAN WARNA SPESIFIK ======
                    cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color_bgr, 3)
                    
                    # ====== BUAT LABEL ======
                    label = f"{cls_name} {conf*100:.1f}%"
                    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    
                    # Background label (warna sama dengan box)
                    cv2.rectangle(img_bgr, 
                                 (x1, y1 - label_h - 10), 
                                 (x1 + label_w + 10, y1), 
                                 color_bgr, -1)
                    
                    # Text label (putih)
                    cv2.putText(img_bgr, label, (x1 + 5, y1 - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # Update stats
                    stats['total'] += 1
                    stats['confidences'].append(conf)
                    stats['class_distribution'][cls_name] = stats['class_distribution'].get(cls_name, 0) + 1
                    stats['detections'].append({
                        'class': cls_name,
                        'confidence': conf,
                        'box': [x1, y1, x2, y2],
                        'color': color_bgr
                    })
    
    # Calculate class confidence averages
    for cls_name in stats['class_distribution']:
        confs = [d['confidence'] for d in stats['detections'] if d['class'] == cls_name]
        stats['class_confidence'][cls_name] = np.mean(confs) if confs else 0
    
    # Convert back to RGB for display
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    return img_rgb, stats


def draw_detections_pil(image, results, model, conf_threshold=0.5):
    """
    Versi PIL - Draw detections dengan warna berbeda per kelas
    """
    if isinstance(image, Image.Image):
        img = image.copy().convert('RGB')
    else:
        img = Image.fromarray(image).convert('RGB')
    
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()
    
    stats = {
        'total': 0,
        'confidences': [],
        'class_distribution': {},
        'class_confidence': {},
        'detections': []
    }
    
    for result in results:
        if hasattr(result, 'boxes') and result.boxes is not None:
            boxes = result.boxes
            
            for box in boxes:
                conf = float(box.conf[0])
                if conf >= conf_threshold:
                    cls_id = int(box.cls[0])
                    cls_name = model.names.get(cls_id, CLASS_NAMES.get(cls_id, 'Unknown'))
                    
                    # ====== TENTUKAN WARNA ======
                    if cls_name in COLORS:
                        color_rgb = COLORS[cls_name]  # (R, G, B)
                    else:
                        color_rgb = (232, 105, 48)  # Oranye
                    
                    # Get box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    
                    # ====== GAMBAR BOUNDING BOX ======
                    draw.rectangle([x1, y1, x2, y2], outline=color_rgb, width=3)
                    
                    # ====== BUAT LABEL ======
                    label = f"{cls_name} {conf*100:.1f}%"
                    
                    # Ukuran text
                    try:
                        bbox = draw.textbbox((x1, y1), label, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                    except:
                        text_width = len(label) * 8
                        text_height = 16
                    
                    # Background label
                    draw.rectangle(
                        [x1, y1 - text_height - 4, x1 + text_width + 4, y1],
                        fill=color_rgb
                    )
                    
                    # Text label
                    draw.text((x1 + 2, y1 - text_height - 2), label, fill=(255, 255, 255), font=font)
                    
                    # Update stats
                    stats['total'] += 1
                    stats['confidences'].append(conf)
                    stats['class_distribution'][cls_name] = stats['class_distribution'].get(cls_name, 0) + 1
                    stats['detections'].append({
                        'class': cls_name,
                        'confidence': conf,
                        'box': [x1, y1, x2, y2],
                        'color': color_rgb
                    })
    
    # Calculate class confidence averages
    for cls_name in stats['class_distribution']:
        confs = [d['confidence'] for d in stats['detections'] if d['class'] == cls_name]
        stats['class_confidence'][cls_name] = np.mean(confs) if confs else 0
    
    return img, stats

