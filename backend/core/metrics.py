"""
Module tính toán các metrics đánh giá chất lượng ảnh: PSNR, SSIM, MSE
"""

import numpy as np
from skimage.metrics import structural_similarity as ssim
from typing import Tuple


def mse(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Tính Mean Squared Error (MSE) giữa hai ảnh
    
    Args:
        image1: Ảnh gốc
        image2: Ảnh đã xử lý
        
    Returns:
        Giá trị MSE
    """
    # Đảm bảo hai ảnh cùng kích thước
    if image1.shape != image2.shape:
        raise ValueError(f"Kích thước ảnh không khớp: {image1.shape} vs {image2.shape}")
    
    # Chuyển về float để tính toán chính xác
    img1 = image1.astype(np.float64)
    img2 = image2.astype(np.float64)
    
    # Tính MSE
    mse_value = np.mean((img1 - img2) ** 2)
    return float(mse_value)


def psnr(image1: np.ndarray, image2: np.ndarray, max_value: float = 255.0) -> float:
    """
    Tính Peak Signal-to-Noise Ratio (PSNR) giữa hai ảnh
    
    Args:
        image1: Ảnh gốc
        image2: Ảnh đã xử lý
        max_value: Giá trị pixel tối đa (255 cho ảnh 8-bit, 1.0 cho ảnh normalized)
        
    Returns:
        Giá trị PSNR (dB)
    """
    mse_value = mse(image1, image2)
    
    # Tránh chia cho 0
    if mse_value == 0:
        return float('inf')
    
    # Tính PSNR
    psnr_value = 20 * np.log10(max_value / np.sqrt(mse_value))
    return float(psnr_value)


def ssim_metric(image1: np.ndarray, image2: np.ndarray, 
                max_value: float = 255.0, multichannel: bool = None) -> float:
    """
    Tính Structural Similarity Index (SSIM) giữa hai ảnh
    
    Args:
        image1: Ảnh gốc
        image2: Ảnh đã xử lý
        max_value: Giá trị pixel tối đa (255 cho ảnh 8-bit, 1.0 cho ảnh normalized)
        multichannel: True nếu ảnh có nhiều kênh màu (None = tự động phát hiện)
        
    Returns:
        Giá trị SSIM (0-1, càng gần 1 càng tốt)
    """
    # Đảm bảo hai ảnh cùng kích thước
    if image1.shape != image2.shape:
        raise ValueError(f"Kích thước ảnh không khớp: {image1.shape} vs {image2.shape}")
    
    # Tự động phát hiện multichannel
    if multichannel is None:
        multichannel = len(image1.shape) == 3 and image1.shape[2] > 1
    
    # Chuyển về float và normalize nếu cần
    img1 = image1.astype(np.float64)
    img2 = image2.astype(np.float64)
    
    # Nếu max_value là 255, normalize về [0, 1]
    if max_value > 1.0:
        img1 = img1 / max_value
        img2 = img2 / max_value
    
    # Tính SSIM
    if multichannel:
        ssim_value = ssim(img1, img2, data_range=1.0, multichannel=True, channel_axis=2)
    else:
        ssim_value = ssim(img1, img2, data_range=1.0)
    
    return float(ssim_value)


def calculate_all_metrics(image1: np.ndarray, image2: np.ndarray, 
                         max_value: float = 255.0) -> dict:
    """
    Tính tất cả các metrics: MSE, PSNR, SSIM
    
    Args:
        image1: Ảnh gốc
        image2: Ảnh đã xử lý
        max_value: Giá trị pixel tối đa
        
    Returns:
        Dictionary chứa các metrics
    """
    mse_value = mse(image1, image2)
    psnr_value = psnr(image1, image2, max_value)
    ssim_value = ssim_metric(image1, image2, max_value)
    
    return {
        'mse': mse_value,
        'psnr': psnr_value,
        'ssim': ssim_value
    }

