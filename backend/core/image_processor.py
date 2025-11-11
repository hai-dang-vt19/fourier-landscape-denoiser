"""
Module xử lý ảnh chính: kết hợp Fourier transform, filters và metrics
"""

import numpy as np
import cv2
from typing import Dict, Tuple, Optional
from scipy.fft import next_fast_len

from .fourier_transform import fft2d, ifft2d, apply_filter, get_magnitude_spectrum
from .filters import create_filter_mask
from .metrics import calculate_all_metrics


class ImageProcessor:
    """Class xử lý ảnh với biến đổi Fourier"""
    
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        self.fft_spectrum = None
        self.filter_mask = None
        self.metrics = None
        self._optimal_shape: Optional[Tuple[int, int]] = None
        self._crop_slices: Optional[Tuple[slice, slice]] = None
        self._mask_cache: dict = {}
    
    def load_image(self, image_path: str) -> np.ndarray:
        """
        Đọc ảnh từ file
        
        Args:
            image_path: Đường dẫn đến file ảnh
            
        Returns:
            Ảnh đã đọc (BGR format từ OpenCV)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        
        self.original_image = image
        return image
    
    def load_image_from_array(self, image_array: np.ndarray):
        """
        Load ảnh từ numpy array
        
        Args:
            image_array: Mảng numpy chứa dữ liệu ảnh (BGR hoặc RGB)
        """
        self.original_image = image_array.copy()
    
    def process_image(self, filter_type: str = 'gaussian', 
                     filter_mode: str = 'lowpass',
                     cutoff: float = 50.0,
                     order: int = 2,
                     center_freq: Optional[float] = None,
                     bandwidth: Optional[float] = None) -> np.ndarray:
        """
        Xử lý ảnh với bộ lọc Fourier theo workflow:
        1. Tách 3 kênh RGB (nếu ảnh màu)
        2. Áp dụng FFT cho từng kênh độc lập
        3. Lọc với bán kính r (cutoff) - có thể điều chỉnh
        4. Merge 3 kênh đã lọc
        5. Trả về ảnh đã xử lý
        
        Args:
            filter_type: Loại bộ lọc ('ideal', 'butterworth', 'gaussian')
            filter_mode: Chế độ lọc ('lowpass', 'highpass', 'bandreject')
            cutoff: Tần số cắt (D0) - tương đương bán kính lọc r (ví dụ: r=20)
            order: Bậc bộ lọc (chỉ dùng cho Butterworth)
            center_freq: Tần số trung tâm (chỉ dùng cho band-reject)
            bandwidth: Độ rộng dải (chỉ dùng cho band-reject)
            
        Returns:
            Ảnh đã được xử lý (BGR format)
        """
        if self.original_image is None:
            raise ValueError("Chưa có ảnh để xử lý. Hãy load ảnh trước.")
        
        # Chuyển ảnh về float và normalize về [0, 1]
        image = self.original_image.astype(np.float32) / 255.0
        
        # Lấy kích thước ảnh
        height, width = image.shape[:2]
        # Tính kích thước FFT tối ưu để tăng tốc
        optimal_h = next_fast_len(height)
        optimal_w = next_fast_len(width)
        self._optimal_shape = (optimal_h, optimal_w)
        self._crop_slices = (slice(0, height), slice(0, width))
        # Pad ảnh đến kích thước tối ưu
        pad_h = optimal_h - height
        pad_w = optimal_w - width
        if pad_h > 0 or pad_w > 0:
            if image.ndim == 2:
                image_padded = np.pad(image, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0.0)
            else:
                image_padded = np.pad(image, ((0, pad_h), (0, pad_w), (0, 0)), mode='constant', constant_values=0.0)
        else:
            image_padded = image
        
        # Tạo mặt nạ bộ lọc (cache theo kích thước tối ưu và tham số)
        cache_key = (
            self._optimal_shape, filter_type, filter_mode, float(cutoff), int(order),
            None if center_freq is None else float(center_freq),
            None if bandwidth is None else float(bandwidth),
        )
        if cache_key in self._mask_cache:
            self.filter_mask = self._mask_cache[cache_key]
        else:
            self.filter_mask = create_filter_mask(
                optimal_h, optimal_w, filter_type, filter_mode,
                cutoff, order, center_freq, bandwidth
            )
            self._mask_cache[cache_key] = self.filter_mask
        
        # Bước 2: Thực hiện FFT cho từng kênh RGB độc lập
        # (fft2d tự động xử lý từng kênh riêng biệt nếu ảnh có 3 kênh)
        self.fft_spectrum = fft2d(image_padded)
        
        # Bước 3: Áp dụng bộ lọc với bán kính r (cutoff) cho từng kênh
        # (apply_filter áp dụng cùng mask cho tất cả kênh RGB)
        filtered_spectrum = apply_filter(self.fft_spectrum, self.filter_mask)
        
        # Bước 4: Merge 3 kênh đã lọc - thực hiện IFFT cho từng kênh và merge lại
        # (ifft2d tự động xử lý từng kênh và merge lại)
        processed = ifft2d(filtered_spectrum)
        if processed.ndim == 2:
            processed = processed[self._crop_slices[0], self._crop_slices[1]]
        else:
            processed = processed[self._crop_slices[0], self._crop_slices[1], :]
        
        # Đảm bảo giá trị trong khoảng [0, 1]
        processed = np.clip(processed, 0.0, 1.0)
        
        # Chuyển về [0, 255] và uint8
        processed = (processed * 255.0).astype(np.uint8)
        
        self.processed_image = processed
        
        # Tính metrics
        self.metrics = calculate_all_metrics(
            self.original_image, 
            self.processed_image,
            max_value=255.0
        )
        
        return processed
    
    def get_magnitude_spectrum_image(self) -> np.ndarray:
        """
        Lấy ảnh biên độ phổ để hiển thị
        
        Returns:
            Ảnh biên độ phổ (normalized về [0, 255])
        """
        if self.fft_spectrum is None:
            raise ValueError("Chưa có phổ Fourier. Hãy xử lý ảnh trước.")
        
        magnitude = get_magnitude_spectrum(self.fft_spectrum)
        # Crop về kích thước gốc để hiển thị
        if magnitude.ndim == 2:
            magnitude = magnitude[self._crop_slices[0], self._crop_slices[1]]
        else:
            magnitude = magnitude[self._crop_slices[0], self._crop_slices[1], :]
        
        # Normalize về [0, 255]
        magnitude_normalized = (magnitude / magnitude.max() * 255.0).astype(np.uint8)
        
        return magnitude_normalized
    
    def get_filter_mask_image(self) -> np.ndarray:
        """
        Lấy ảnh mặt nạ bộ lọc để hiển thị
        
        Returns:
            Ảnh mặt nạ (normalized về [0, 255])
        """
        if self.filter_mask is None:
            raise ValueError("Chưa có mặt nạ bộ lọc. Hãy xử lý ảnh trước.")
        
        # Crop mask về kích thước gốc để hiển thị
        mask_cropped = self.filter_mask[self._crop_slices[0], self._crop_slices[1]]
        mask_normalized = (mask_cropped * 255.0).astype(np.uint8)
        return mask_normalized
    
    def get_metrics(self) -> Optional[Dict]:
        """
        Lấy các metrics đã tính
        
        Returns:
            Dictionary chứa MSE, PSNR, SSIM hoặc None nếu chưa tính
        """
        return self.metrics
    
    def save_processed_image(self, output_path: str):
        """
        Lưu ảnh đã xử lý
        
        Args:
            output_path: Đường dẫn file output
        """
        if self.processed_image is None:
            raise ValueError("Chưa có ảnh đã xử lý để lưu.")
        
        cv2.imwrite(output_path, self.processed_image)

