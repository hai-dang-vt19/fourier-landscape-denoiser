import { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import FilterControl from './components/FilterControl';
import ComparisonView from './components/ComparisonView';
import SpectrumViewer from './components/SpectrumViewer';
import MetricsDisplay from './components/MetricsDisplay';
import ProcessingStatus from './components/ProcessingStatus';
import { processImage, healthCheck } from './services/api';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [magnitudeSpectrum, setMagnitudeSpectrum] = useState(null);
  const [filterMask, setFilterMask] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [filterParams, setFilterParams] = useState({
    filter_type: 'gaussian',
    filter_mode: 'lowpass',
    cutoff: 20, // Mặc định r=20 theo tài liệu
    order: 2,
  });

  // Health check khi component mount
  useEffect(() => {
    healthCheck()
      .then((data) => {
        console.log('API Health:', data);
      })
      .catch((err) => {
        console.error('API Health Check failed:', err);
        setError('Không thể kết nối đến server. Vui lòng kiểm tra lại.');
      });
  }, []);

  // Xử lý khi chọn ảnh
  const handleImageSelect = (imageBase64) => {
    setOriginalImage(imageBase64);
    setProcessedImage(null);
    setMagnitudeSpectrum(null);
    setFilterMask(null);
    setMetrics(null);
    setError(null);
  };

  // Chỉ cập nhật params khi thay đổi (không render)
  const handleFilterChange = (params) => {
    setFilterParams(params);
  };

  // Xử lý ảnh khi click nút
  const handleProcessImage = async (params) => {
    if (!originalImage) return;
    
    setIsProcessing(true);
    setError(null);
    try {
      const result = await processImage(originalImage, params);
      if (result.success) {
        setProcessedImage(result.processed_image);
        setMagnitudeSpectrum(result.magnitude_spectrum);
        setFilterMask(result.filter_mask);
        setMetrics(result.metrics);
      } else {
        throw new Error('Xử lý ảnh không thành công');
      }
    } catch (err) {
      setError(err.message);
      console.error('Error processing image:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <ProcessingStatus isProcessing={isProcessing} error={error} />
      
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Hệ Thống Xử Lý Ảnh
          </h1>
          <p className="text-gray-600">
            Sử dụng Biến Đổi Fourier 2D để khử nhiễu và xử lý ảnh
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Cột trái: Upload và Filter Control */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-blue-950 text-xl font-semibold mb-4">Upload Ảnh</h2>
              <ImageUploader onImageSelect={handleImageSelect} />
            </div>

            <FilterControl
              onFilterChange={handleFilterChange}
              onProcessClick={handleProcessImage}
              disabled={!originalImage || isProcessing}
            />
          </div>

          {/* Cột phải: Kết quả */}
          <div className="lg:col-span-2 space-y-6">
            <ComparisonView
              originalImage={originalImage}
              processedImage={processedImage}
            />

            <SpectrumViewer
              magnitudeSpectrum={magnitudeSpectrum}
              filterMask={filterMask}
            />

            <MetricsDisplay metrics={metrics} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

