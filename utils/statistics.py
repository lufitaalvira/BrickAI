"""
Statistics utilities
"""
import numpy as np


def calculate_all_statistics(detections):
    """Calculate all statistics from detections"""
    if not detections:
        return {
            'total': 0,
            'accuracy': 0,
            'average_confidence': 0,
            'min_confidence': 0,
            'max_confidence': 0,
            'class_distribution': {},
            'class_confidence': {}
        }
    
    confidences = [d.get('confidence', 0) for d in detections]
    classes = [d.get('class', 'Unknown') for d in detections]
    
    # Class distribution
    class_dist = {}
    for c in classes:
        class_dist[c] = class_dist.get(c, 0) + 1
    
    # Average confidence per class
    class_conf = {}
    for d in detections:
        class_name = d.get('class', 'Unknown')
        if class_name not in class_conf:
            class_conf[class_name] = []
        class_conf[class_name].append(d.get('confidence', 0))
    
    class_confidence = {}
    for class_name, confs in class_conf.items():
        class_confidence[class_name] = np.mean(confs) if confs else 0
    
    return {
        'total': len(detections),
        'accuracy': np.mean(confidences) * 100 if confidences else 0,
        'average_confidence': np.mean(confidences) if confidences else 0,
        'min_confidence': np.min(confidences) if confidences else 0,
        'max_confidence': np.max(confidences) if confidences else 0,
        'class_distribution': class_dist,
        'class_confidence': class_confidence,
        'detections': detections
    }


def format_statistics_for_display(stats):
    """Format statistics for display"""
    if not stats or stats.get('total', 0) == 0:
        return {
            'Total Deteksi': 0,
            'Akurasi': '0%',
            'Average Confidence': '0%',
            'Min Confidence': '0%',
            'Max Confidence': '0%',
            'Distribusi': {},
            'Rata-rata per Class': {}
        }
    
    # Format percentages
    avg_conf = stats.get('average_confidence', 0) * 100
    min_conf = stats.get('min_confidence', 0) * 100
    max_conf = stats.get('max_confidence', 0) * 100
    
    # Format class confidence
    class_conf = stats.get('class_confidence', {})
    formatted_class_conf = {}
    for class_name, conf in class_conf.items():
        formatted_class_conf[class_name] = f"{conf*100:.2f}%"
    
    return {
        'Total Deteksi': stats.get('total', 0),
        'Akurasi': f"{stats.get('accuracy', 0):.2f}%",
        'Average Confidence': f"{avg_conf:.2f}%",
        'Min Confidence': f"{min_conf:.2f}%",
        'Max Confidence': f"{max_conf:.2f}%",
        'Distribusi': stats.get('class_distribution', {}),
        'Rata-rata per Class': formatted_class_conf
    }


def format_detection_stats(stats):
    """
    Format detection statistics for display (untuk halaman deteksi)
    
    Args:
        stats: Dictionary hasil statistik dari deteksi
        
    Returns:
        Dictionary dengan format yang sudah diformat
    """
    if not stats:
        return {
            'total': 0,
            'accuracy': 0,
            'average_confidence': 0,
            'min_confidence': 0,
            'max_confidence': 0,
            'class_distribution': {},
            'class_confidence': {},
            'formatted': {
                'Total Deteksi': 0,
                'Akurasi': '0%',
                'Rata-rata Confidence': '0%',
                'Min Confidence': '0%',
                'Max Confidence': '0%',
                'Distribusi': {},
                'Rata-rata per Class': {}
            }
        }
    
    # Hitung statistik jika belum ada
    if 'accuracy' not in stats:
        confidences = stats.get('confidences', [])
        if confidences:
            stats['accuracy'] = np.mean(confidences) * 100
            stats['average_confidence'] = np.mean(confidences)
            stats['min_confidence'] = np.min(confidences)
            stats['max_confidence'] = np.max(confidences)
        else:
            stats['accuracy'] = 0
            stats['average_confidence'] = 0
            stats['min_confidence'] = 0
            stats['max_confidence'] = 0
    
    # Format untuk display
    formatted = format_statistics_for_display(stats)
    stats['formatted'] = formatted
    
    return stats