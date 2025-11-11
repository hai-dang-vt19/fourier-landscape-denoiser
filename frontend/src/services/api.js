const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Gọi API health check
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
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

    const response = await fetch(`${API_BASE_URL}/api/process`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Lỗi xử lý ảnh');
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

    const response = await fetch(`${API_BASE_URL}/api/upload`, {
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

