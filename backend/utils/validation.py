"""
Module validation cho các tham số đầu vào
"""

import os
from typing import List, Optional, Tuple
import numpy as np


ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
ALLOWED_FILTER_TYPES = ['ideal', 'butterworth', 'gaussian']
ALLOWED_FILTER_MODES = ['lowpass', 'highpass', 'bandreject']


def validate_image_file(file_path: str) -> bool:
    """
    Kiểm tra file ảnh có hợp lệ không
    
    Args:
        file_path: Đường dẫn file
        
    Returns:
        True nếu hợp lệ
    """
    if not os.path.exists(file_path):
        return False
    
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS


def validate_filter_type(filter_type: str) -> bool:
    """
    Kiểm tra loại bộ lọc có hợp lệ không
    
    Args:
        filter_type: Loại bộ lọc
        
    Returns:
        True nếu hợp lệ
    """
    return filter_type.lower() in ALLOWED_FILTER_TYPES


def validate_filter_mode(filter_mode: str) -> bool:
    """
    Kiểm tra chế độ lọc có hợp lệ không
    
    Args:
        filter_mode: Chế độ lọc
        
    Returns:
        True nếu hợp lệ
    """
    return filter_mode.lower() in ALLOWED_FILTER_MODES


def validate_cutoff(cutoff: float, min_value: float = 0.1, max_value: float = 1000.0) -> bool:
    """
    Kiểm tra giá trị cutoff có hợp lệ không
    
    Args:
        cutoff: Tần số cắt
        min_value: Giá trị tối thiểu
        max_value: Giá trị tối đa
        
    Returns:
        True nếu hợp lệ
    """
    return min_value <= cutoff <= max_value


def validate_order(order: int, min_value: int = 1, max_value: int = 10) -> bool:
    """
    Kiểm tra bậc bộ lọc có hợp lệ không
    
    Args:
        order: Bậc bộ lọc
        min_value: Giá trị tối thiểu
        max_value: Giá trị tối đa
        
    Returns:
        True nếu hợp lệ
    """
    return min_value <= order <= max_value


def validate_image_array(image: np.ndarray) -> bool:
    """
    Kiểm tra numpy array có phải là ảnh hợp lệ không
    
    Args:
        image: Mảng numpy
        
    Returns:
        True nếu hợp lệ
    """
    if not isinstance(image, np.ndarray):
        return False
    
    if len(image.shape) not in [2, 3]:
        return False
    
    if len(image.shape) == 3 and image.shape[2] not in [1, 3, 4]:
        return False
    
    return True


def validate_processing_params(filter_type: str, filter_mode: str, 
                              cutoff: float, order: int = 2,
                              center_freq: Optional[float] = None,
                              bandwidth: Optional[float] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate tất cả tham số xử lý
    
    Args:
        filter_type: Loại bộ lọc
        filter_mode: Chế độ lọc
        cutoff: Tần số cắt
        order: Bậc bộ lọc
        center_freq: Tần số trung tâm
        bandwidth: Độ rộng dải
        
    Returns:
        (is_valid, error_message)
    """
    if not validate_filter_type(filter_type):
        return False, f"Loại bộ lọc không hợp lệ: {filter_type}"
    
    if not validate_filter_mode(filter_mode):
        return False, f"Chế độ lọc không hợp lệ: {filter_mode}"
    
    if not validate_cutoff(cutoff):
        return False, f"Giá trị cutoff không hợp lệ: {cutoff}"
    
    if not validate_order(order):
        return False, f"Bậc bộ lọc không hợp lệ: {order}"
    
    if filter_mode == 'bandreject':
        if center_freq is not None and not validate_cutoff(center_freq):
            return False, f"Tần số trung tâm không hợp lệ: {center_freq}"
        if bandwidth is not None and not validate_cutoff(bandwidth):
            return False, f"Độ rộng dải không hợp lệ: {bandwidth}"
    
    return True, None

