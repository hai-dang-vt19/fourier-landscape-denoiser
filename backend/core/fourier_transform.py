"""
Module xử lý biến đổi Fourier 2D cho ảnh
Hỗ trợ FFT, IFFT và các thao tác trên miền tần số
"""

import numpy as np
from typing import Tuple, Optional


def fft2d(image: np.ndarray) -> np.ndarray:
    """
    Thực hiện biến đổi Fourier 2D (FFT) cho ảnh
    Workflow: Tách 3 kênh RGB và áp dụng FFT cho từng kênh độc lập
    
    Args:
        image: Ảnh đầu vào (H, W) hoặc (H, W, C)
        
    Returns:
        Phổ Fourier đã được dịch tâm (centered)
        - Nếu ảnh grayscale: (H, W)
        - Nếu ảnh RGB: (H, W, 3) - mỗi kênh được xử lý riêng biệt
    """
    if len(image.shape) == 2:
        # Ảnh grayscale
        fft = np.fft.fft2(image)
        return np.fft.fftshift(fft)
    elif len(image.shape) == 3:
        # Ảnh màu RGB - Bước 1: Tách 3 kênh RGB
        # Bước 2: Áp dụng FFT cho từng kênh độc lập
        fft_channels = []
        for i in range(image.shape[2]):
            fft = np.fft.fft2(image[:, :, i])
            fft_channels.append(np.fft.fftshift(fft))
        # Merge lại thành (H, W, 3)
        return np.stack(fft_channels, axis=2)
    else:
        raise ValueError(f"Ảnh phải có 2 hoặc 3 chiều, nhận được {len(image.shape)}")


def ifft2d(fft_spectrum: np.ndarray) -> np.ndarray:
    """
    Thực hiện biến đổi Fourier ngược 2D (IFFT) cho phổ
    Workflow: Áp dụng IFFT cho từng kênh RGB và merge lại
    
    Args:
        fft_spectrum: Phổ Fourier đã được dịch tâm
        
    Returns:
        Ảnh phục hồi (phần thực)
        - Nếu phổ grayscale: (H, W)
        - Nếu phổ RGB: (H, W, 3) - merge 3 kênh đã xử lý
    """
    if len(fft_spectrum.shape) == 2:
        # Ảnh grayscale
        ifft = np.fft.ifftshift(fft_spectrum)
        image = np.fft.ifft2(ifft)
        return np.real(image)
    elif len(fft_spectrum.shape) == 3:
        # Ảnh màu RGB - Bước 4: Merge 3 kênh đã lọc
        # Áp dụng IFFT cho từng kênh độc lập
        image_channels = []
        for i in range(fft_spectrum.shape[2]):
            ifft = np.fft.ifftshift(fft_spectrum[:, :, i])
            channel = np.fft.ifft2(ifft)
            image_channels.append(np.real(channel))
        # Merge lại thành (H, W, 3)
        return np.stack(image_channels, axis=2)
    else:
        raise ValueError(f"Phổ phải có 2 hoặc 3 chiều, nhận được {len(fft_spectrum.shape)}")


def get_magnitude_spectrum(fft_spectrum: np.ndarray) -> np.ndarray:
    """
    Tính biên độ phổ (magnitude spectrum)
    
    Args:
        fft_spectrum: Phổ Fourier
        
    Returns:
        Biên độ phổ (log scale để hiển thị tốt hơn)
    """
    magnitude = np.abs(fft_spectrum)
    # Áp dụng log scale để hiển thị tốt hơn
    magnitude_log = np.log1p(magnitude)
    return magnitude_log


def get_phase_spectrum(fft_spectrum: np.ndarray) -> np.ndarray:
    """
    Tính pha phổ (phase spectrum)
    
    Args:
        fft_spectrum: Phổ Fourier
        
    Returns:
        Pha phổ (radian)
    """
    return np.angle(fft_spectrum)


def apply_filter(fft_spectrum: np.ndarray, filter_mask: np.ndarray) -> np.ndarray:
    """
    Áp dụng bộ lọc lên phổ Fourier
    Bước 3: Lọc với bán kính r (cutoff) cho từng kênh RGB độc lập
    
    Args:
        fft_spectrum: Phổ Fourier (H, W) hoặc (H, W, 3)
        filter_mask: Mặt nạ bộ lọc với bán kính r (cùng kích thước với ảnh)
        
    Returns:
        Phổ đã được lọc (cùng shape với input)
    """
    if len(fft_spectrum.shape) == 2:
        return fft_spectrum * filter_mask
    elif len(fft_spectrum.shape) == 3:
        # Áp dụng cùng một mask (với bán kính r) cho từng kênh RGB độc lập
        filtered_channels = []
        for i in range(fft_spectrum.shape[2]):
            filtered_channels.append(fft_spectrum[:, :, i] * filter_mask)
        return np.stack(filtered_channels, axis=2)
    else:
        raise ValueError(f"Phổ phải có 2 hoặc 3 chiều, nhận được {len(fft_spectrum.shape)}")

