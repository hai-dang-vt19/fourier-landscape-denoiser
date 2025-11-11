const MetricsDisplay = ({ metrics }) => {
  if (!metrics) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-blue-950 text-xl font-semibold mb-4">Chỉ Số Đánh Giá</h3>
        <p className="text-gray-500">Chưa có dữ liệu metrics</p>
      </div>
    );
  }

  const { mse, psnr, ssim } = metrics;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-blue-950 text-xl font-semibold mb-4">Chỉ Số Đánh Giá</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="text-sm font-medium text-blue-700 mb-1">MSE</h4>
          <p className="text-2xl font-bold text-blue-900">
            {mse.toFixed(2)}
          </p>
          <p className="text-xs text-blue-600 mt-1">
            Mean Squared Error (càng thấp càng tốt)
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="text-sm font-medium text-green-700 mb-1">PSNR</h4>
          <p className="text-2xl font-bold text-green-900">
            {psnr.toFixed(2)} dB
          </p>
          <p className="text-xs text-green-600 mt-1">
            Peak Signal-to-Noise Ratio (càng cao càng tốt)
          </p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h4 className="text-sm font-medium text-purple-700 mb-1">SSIM</h4>
          <p className="text-2xl font-bold text-purple-900">
            {ssim.toFixed(4)}
          </p>
          <p className="text-xs text-purple-600 mt-1">
            Structural Similarity Index (0-1, càng gần 1 càng tốt)
          </p>
        </div>
      </div>
    </div>
  );
};

export default MetricsDisplay;

