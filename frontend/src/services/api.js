// Sử dụng relative URL để tận dụng Vite proxy (tránh CORS issues)
// Hoặc absolute URL nếu có VITE_API_URL được set (cho production)
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Gọi API health check
 */
export const healthCheck = async () => {
  try {
    const url = API_BASE_URL ? `${API_BASE_URL}/api/health` : '/api/health';
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    throw new Error(`Lỗi kết nối API: ${error.message}`);
  }
};

/**
 * Xử lý ảnh với bộ lọc Fourier
 * @param {string} imageBase64 - Ảnh dạng base64
 * @param {object} filterParams - Tham số bộ lọc
 */
export const processImage = async (imageBase64, filterParams) => {
  try {
    const formData = new FormData();
    
    // Chuyển base64 thành Blob
    const base64Data = imageBase64.split(',')[1] || imageBase64;
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'image/png' });
    
    formData.append('image', blob, 'image.png');
    formData.append('filter_type', filterParams.filter_type);
    formData.append('filter_mode', filterParams.filter_mode);
    formData.append('cutoff', filterParams.cutoff);
    formData.append('order', filterParams.order || 2);
    
    if (filterParams.center_freq) {
      formData.append('center_freq', filterParams.center_freq);
    }
    if (filterParams.bandwidth) {
      formData.append('bandwidth', filterParams.bandwidth);
    }

    // Thêm timeout 60 giây cho request xử lý ảnh
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000000);
    
    const url = API_BASE_URL ? `${API_BASE_URL}/api/process` : '/api/process';
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      // Thử đọc error message từ JSON
      let errorMessage = 'Lỗi xử lý ảnh';
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
      } catch (e) {
        // Nếu không parse được JSON, lấy text
        const errorText = await response.text();
        errorMessage = errorText || `HTTP ${response.status}: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Lỗi xử lý ảnh: ${error.message}`);
  }
};

/**
 * Upload ảnh lên server
 * @param {File} file - File ảnh
 */
export const uploadImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append('image', file);

    const url = API_BASE_URL ? `${API_BASE_URL}/api/upload` : '/api/upload';
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Lỗi upload ảnh');
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Lỗi upload: ${error.message}`);
  }
};

