"""
Module chứa các bộ lọc tần số: Low-pass, High-pass, Band-reject
Hỗ trợ Ideal, Butterworth, và Gaussian filters
"""

import numpy as np
from typing import Tuple, Optional


def create_distance_matrix(height: int, width: int) -> np.ndarray:
    """
    Tạo ma trận khoảng cách từ tâm ảnh
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        
    Returns:
        Ma trận khoảng cách (H, W)
    """
    center_y, center_x = height // 2, width // 2
    y, x = np.ogrid[:height, :width]
    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    return distance


def ideal_lowpass_filter(height: int, width: int, cutoff: float) -> np.ndarray:
    """
    Tạo bộ lọc Low-pass Ideal
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0)
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    distance = create_distance_matrix(height, width)
    mask = (distance <= cutoff).astype(float)
    return mask


def ideal_highpass_filter(height: int, width: int, cutoff: float) -> np.ndarray:
    """
    Tạo bộ lọc High-pass Ideal
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0)
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    return 1.0 - ideal_lowpass_filter(height, width, cutoff)


def butterworth_lowpass_filter(height: int, width: int, cutoff: float, order: int = 2) -> np.ndarray:
    """
    Tạo bộ lọc Low-pass Butterworth
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0)
        order: Bậc của bộ lọc (mặc định 2)
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    distance = create_distance_matrix(height, width)
    mask = 1.0 / (1.0 + (distance / cutoff) ** (2 * order))
    return mask


def butterworth_highpass_filter(height: int, width: int, cutoff: float, order: int = 2) -> np.ndarray:
    """
    Tạo bộ lọc High-pass Butterworth
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0)
        order: Bậc của bộ lọc (mặc định 2)
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    return 1.0 - butterworth_lowpass_filter(height, width, cutoff, order)


def gaussian_lowpass_filter(height: int, width: int, cutoff: float) -> np.ndarray:
    """
    Tạo bộ lọc Low-pass Gaussian
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0) - độ lệch chuẩn
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    distance = create_distance_matrix(height, width)
    mask = np.exp(-(distance**2) / (2 * (cutoff**2)))
    return mask


def gaussian_highpass_filter(height: int, width: int, cutoff: float) -> np.ndarray:
    """
    Tạo bộ lọc High-pass Gaussian
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        cutoff: Tần số cắt (D0) - độ lệch chuẩn
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    return 1.0 - gaussian_lowpass_filter(height, width, cutoff)


def bandreject_filter(height: int, width: int, center_freq: float, bandwidth: float, filter_type: str = 'ideal') -> np.ndarray:
    """
    Tạo bộ lọc Band-reject (loại bỏ dải tần số)
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        center_freq: Tần số trung tâm của dải cần loại bỏ (D0)
        bandwidth: Độ rộng dải tần số (W)
        filter_type: Loại bộ lọc ('ideal', 'butterworth', 'gaussian')
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    distance = create_distance_matrix(height, width)
    
    if filter_type == 'ideal':
        # Ideal band-reject: loại bỏ dải tần số từ D0 - W/2 đến D0 + W/2
        mask = np.ones((height, width))
        reject_band = (distance >= (center_freq - bandwidth/2)) & (distance <= (center_freq + bandwidth/2))
        mask[reject_band] = 0.0
        return mask
    
    elif filter_type == 'butterworth':
        # Butterworth band-reject filter
        # Công thức: H(u,v) = 1 / (1 + [D(u,v)W / (D²(u,v) - D₀²)]^(2n))
        # Với n=2 (order=2): H(u,v) = 1 / (1 + [D(u,v)W / (D²(u,v) - D₀²)]^4)
        D = distance
        D0 = center_freq
        W = bandwidth
        order = 2  # Có thể thêm order parameter nếu cần
        
        # Tránh chia cho 0
        denominator = D**2 - D0**2
        denominator = np.where(np.abs(denominator) < 1e-10, 1e-10, denominator)
        
        # Tính [D*W / (D² - D₀²)]^(2*order)
        ratio = (D * W) / denominator
        mask = 1.0 / (1.0 + ratio ** (2 * order))
        return mask
    
    elif filter_type == 'gaussian':
        # Gaussian band-reject filter
        # Công thức: H(u,v) = 1 - exp(-[(D²(u,v) - D₀²)² / (D(u,v)W)²])
        D = distance
        D0 = center_freq
        W = bandwidth
        
        # Tránh chia cho 0
        denominator = D**2 - D0**2
        # Tính [(D² - D₀²)² / (DW)²]
        numerator = denominator**2
        denominator_sq = (D * W)**2
        denominator_sq = np.where(denominator_sq < 1e-10, 1e-10, denominator_sq)
        
        mask = 1.0 - np.exp(-(numerator / denominator_sq))
        return mask
    
    else:
        raise ValueError(f"Loại bộ lọc không hợp lệ: {filter_type}. Chọn 'ideal', 'butterworth', hoặc 'gaussian'")


def create_filter_mask(height: int, width: int, filter_type: str, filter_mode: str, 
                      cutoff: float, order: int = 2, center_freq: Optional[float] = None, 
                      bandwidth: Optional[float] = None) -> np.ndarray:
    """
    Hàm tổng quát để tạo mặt nạ bộ lọc
    
    Args:
        height: Chiều cao ảnh
        width: Chiều rộng ảnh
        filter_type: Loại bộ lọc ('ideal', 'butterworth', 'gaussian')
        filter_mode: Chế độ lọc ('lowpass', 'highpass', 'bandreject')
        cutoff: Tần số cắt (D0)
        order: Bậc bộ lọc (chỉ dùng cho Butterworth)
        center_freq: Tần số trung tâm (chỉ dùng cho band-reject)
        bandwidth: Độ rộng dải (chỉ dùng cho band-reject)
        
    Returns:
        Mặt nạ bộ lọc (H, W)
    """
    if filter_mode == 'lowpass':
        if filter_type == 'ideal':
            return ideal_lowpass_filter(height, width, cutoff)
        elif filter_type == 'butterworth':
            return butterworth_lowpass_filter(height, width, cutoff, order)
        elif filter_type == 'gaussian':
            return gaussian_lowpass_filter(height, width, cutoff)
        else:
            raise ValueError(f"Loại bộ lọc không hợp lệ: {filter_type}")
    
    elif filter_mode == 'highpass':
        if filter_type == 'ideal':
            return ideal_highpass_filter(height, width, cutoff)
        elif filter_type == 'butterworth':
            return butterworth_highpass_filter(height, width, cutoff, order)
        elif filter_type == 'gaussian':
            return gaussian_highpass_filter(height, width, cutoff)
        else:
            raise ValueError(f"Loại bộ lọc không hợp lệ: {filter_type}")
    
    elif filter_mode == 'bandreject':
        if center_freq is None:
            center_freq = cutoff
        if bandwidth is None:
            bandwidth = cutoff * 0.5
        return bandreject_filter(height, width, center_freq, bandwidth, filter_type)
    
    else:
        raise ValueError(f"Chế độ lọc không hợp lệ: {filter_mode}")

