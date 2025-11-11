"""
Module xử lý đọc/ghi ảnh và chuyển đổi định dạng
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import os


def read_image(image_path: str) -> np.ndarray:
    """
    Đọc ảnh từ file
    
    Args:
        image_path: Đường dẫn đến file ảnh
        
    Returns:
        Ảnh đã đọc (BGR format từ OpenCV)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy file: {image_path}")
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Không thể đọc ảnh từ {image_path}. Có thể file không phải là ảnh hợp lệ.")
    
    return image


def save_image(image: np.ndarray, output_path: str, quality: int = 95) -> bool:
    """
    Lưu ảnh ra file
    
    Args:
        image: Ảnh cần lưu (numpy array)
        output_path: Đường dẫn file output
        quality: Chất lượng ảnh (1-100, chỉ áp dụng cho JPEG)
        
    Returns:
        True nếu lưu thành công
    """
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    # Xác định extension để quyết định tham số
    ext = os.path.splitext(output_path)[1].lower()
    
    if ext in ['.jpg', '.jpeg']:
        # Lưu JPEG với chất lượng
        cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    elif ext == '.png':
        # Lưu PNG với compression
        compression = 9 - int(quality / 10)  # Chuyển quality về compression level (0-9)
        cv2.imwrite(output_path, image, [cv2.IMWRITE_PNG_COMPRESSION, compression])
    else:
        # Các định dạng khác
        cv2.imwrite(output_path, image)
    
    return os.path.exists(output_path)


def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    """
    Chuyển đổi ảnh từ BGR (OpenCV) sang RGB
    
    Args:
        image: Ảnh BGR
        
    Returns:
        Ảnh RGB
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def convert_rgb_to_bgr(image: np.ndarray) -> np.ndarray:
    """
    Chuyển đổi ảnh từ RGB sang BGR (OpenCV)
    
    Args:
        image: Ảnh RGB
        
    Returns:
        Ảnh BGR
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


def resize_image(image: np.ndarray, max_size: Optional[Tuple[int, int]] = None, 
                scale_factor: Optional[float] = None) -> np.ndarray:
    """
    Thay đổi kích thước ảnh
    
    Args:
        image: Ảnh gốc
        max_size: Kích thước tối đa (width, height) - giữ tỷ lệ
        scale_factor: Tỷ lệ thu phóng
        
    Returns:
        Ảnh đã thay đổi kích thước
    """
    if max_size is not None:
        height, width = image.shape[:2]
        max_width, max_height = max_size
        
        # Tính scale để vừa với max_size
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    elif scale_factor is not None:
        height, width = image.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    else:
        return image


def normalize_image(image: np.ndarray, target_range: Tuple[float, float] = (0.0, 1.0)) -> np.ndarray:
    """
    Chuẩn hóa ảnh về một khoảng giá trị
    
    Args:
        image: Ảnh gốc
        target_range: Khoảng giá trị đích (min, max)
        
    Returns:
        Ảnh đã chuẩn hóa
    """
    min_val, max_val = target_range
    img_min = image.min()
    img_max = image.max()
    
    if img_max == img_min:
        return np.full_like(image, min_val, dtype=np.float32)
    
    normalized = (image - img_min) / (img_max - img_min)
    normalized = normalized * (max_val - min_val) + min_val
    
    return normalized.astype(np.float32)

