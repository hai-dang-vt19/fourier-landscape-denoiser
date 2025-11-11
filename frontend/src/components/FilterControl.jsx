import { useState, useEffect } from 'react';

const FilterControl = ({ onFilterChange, onProcessClick, disabled = false }) => {
  const [filterType, setFilterType] = useState('gaussian');
  const [filterMode, setFilterMode] = useState('lowpass');
  const [cutoff, setCutoff] = useState(20); // Mặc định r=20 theo tài liệu
  const [order, setOrder] = useState(2);
  const [centerFreq, setCenterFreq] = useState(50);
  const [bandwidth, setBandwidth] = useState(25);
  const [preset, setPreset] = useState('custom');

  // Định nghĩa các preset ví dụ
  const presets = {
    custom: { name: 'Tùy chỉnh', filterType: 'gaussian', filterMode: 'lowpass', cutoff: 20, order: 2, centerFreq: 50, bandwidth: 25 },
    smooth_light: { name: 'Làm mượt nhẹ', filterType: 'gaussian', filterMode: 'lowpass', cutoff: 30, order: 2, centerFreq: 50, bandwidth: 25 },
    smooth_strong: { name: 'Làm mượt mạnh', filterType: 'gaussian', filterMode: 'lowpass', cutoff: 10, order: 2, centerFreq: 50, bandwidth: 25 },
    blur: { name: 'Làm mờ ảnh', filterType: 'gaussian', filterMode: 'lowpass', cutoff: 50, order: 2, centerFreq: 50, bandwidth: 25 },
    edge_enhance: { name: 'Tăng cường biên', filterType: 'butterworth', filterMode: 'highpass', cutoff: 15, order: 3, centerFreq: 50, bandwidth: 25 },
    sharpen: { name: 'Tăng độ sắc nét', filterType: 'ideal', filterMode: 'highpass', cutoff: 20, order: 2, centerFreq: 50, bandwidth: 25 },
    noise_reject: { name: 'Loại bỏ nhiễu tần số', filterType: 'gaussian', filterMode: 'bandreject', cutoff: 20, order: 2, centerFreq: 50, bandwidth: 20 },
    noise_reject_strong: { name: 'Loại bỏ nhiễu mạnh', filterType: 'butterworth', filterMode: 'bandreject', cutoff: 20, order: 4, centerFreq: 50, bandwidth: 30 },
  };

  // Hàm lấy params hiện tại
  const getCurrentParams = () => {
    const params = {
      filter_type: filterType,
      filter_mode: filterMode,
      cutoff: cutoff,
      order: order,
    };

    if (filterMode === 'bandreject') {
      params.center_freq = centerFreq;
      params.bandwidth = bandwidth;
    }

    return params;
  };

  // Xử lý khi chọn preset
  const handlePresetChange = (presetKey) => {
    setPreset(presetKey);
    const selectedPreset = presets[presetKey];
    if (selectedPreset) {
      setFilterType(selectedPreset.filterType);
      setFilterMode(selectedPreset.filterMode);
      setCutoff(selectedPreset.cutoff);
      setOrder(selectedPreset.order);
      setCenterFreq(selectedPreset.centerFreq);
      setBandwidth(selectedPreset.bandwidth);
      
      // Cập nhật params ngay lập tức
      const params = {
        filter_type: selectedPreset.filterType,
        filter_mode: selectedPreset.filterMode,
        cutoff: selectedPreset.cutoff,
        order: selectedPreset.order,
      };
      
      if (selectedPreset.filterMode === 'bandreject') {
        params.center_freq = selectedPreset.centerFreq;
        params.bandwidth = selectedPreset.bandwidth;
      }
      
      onFilterChange(params);
    }
  };

  // Xử lý khi thay đổi params thủ công (đặt về custom)
  const handleManualChange = () => {
    if (preset !== 'custom') {
      setPreset('custom');
    }
  };

  // Xử lý khi thay đổi params (chỉ update, không render)
  const handleParamChange = () => {
    const params = getCurrentParams();
    onFilterChange(params);
  };

  // Xử lý khi click nút xử lý
  const handleProcess = () => {
    const params = getCurrentParams();
    onProcessClick(params);
  };

  // Tự động cập nhật params khi các giá trị thay đổi
  useEffect(() => {
    handleParamChange();
  }, [filterType, filterMode, cutoff, order, centerFreq, bandwidth]);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h3 className="text-blue-950 text-xl font-semibold mb-4">Cài Đặt Bộ Lọc</h3>

      {/* Preset ví dụ */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Ví Dụ Thường Gặp
        </label>
        <select
          value={preset}
          onChange={(e) => handlePresetChange(e.target.value)}
          disabled={disabled}
          className="text-blue-700 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
        >
          {Object.entries(presets).map(([key, preset]) => (
            <option key={key} value={key}>
              {preset.name}
            </option>
          ))}
        </select>
      </div>

      {/* Loại bộ lọc */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Loại Bộ Lọc
        </label>
        <select
          value={filterType}
          onChange={(e) => {
            handleManualChange();
            setFilterType(e.target.value);
          }}
          disabled={disabled}
          className="text-blue-700 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="ideal">Ideal (Cắt đột ngột, lý tưởng)</option>
          <option value="butterworth">Butterworth (Mượt mà, điều chỉnh được)</option>
          <option value="gaussian">Gaussian (Mượt nhất, phân bố chuẩn)</option>
        </select>
      </div>

      {/* Chế độ lọc */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Chế Độ Lọc
        </label>
        <select
          value={filterMode}
          onChange={(e) => {
            handleManualChange();
            setFilterMode(e.target.value);
          }}
          disabled={disabled}
          className="text-blue-700 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="lowpass">Low-pass (Làm mượt)</option>
          <option value="highpass">High-pass (Tăng cường biên)</option>
          <option value="bandreject">Band-reject (Loại bỏ dải tần)</option>
        </select>
      </div>

      {/* Tần số cắt / Bán kính lọc */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Bán Kính Lọc (r) / Tần Số Cắt: {cutoff}
        </label>
        <input
          type="range"
          min="1"
          max="200"
          value={cutoff}
          onChange={(e) => {
            handleManualChange();
            setCutoff(Number(e.target.value));
          }}
          disabled={disabled}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>r=1 (mạnh)</span>
          <span className="font-semibold">r=20 (khuyến nghị)</span>
          <span>r=200 (nhẹ)</span>
        </div>
      </div>

      {/* Bậc bộ lọc (chỉ cho Butterworth) */}
      {filterType === 'butterworth' && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Bậc Bộ Lọc (Order): {order}
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={order}
            onChange={(e) => {
              handleManualChange();
              setOrder(Number(e.target.value));
            }}
            disabled={disabled}
            className="w-full"
          />
        </div>
      )}

      {/* Tham số cho Band-reject */}
      {filterMode === 'bandreject' && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tần Số Trung Tâm: {centerFreq}
            </label>
            <input
              type="range"
              min="1"
              max="200"
              value={centerFreq}
              onChange={(e) => {
                handleManualChange();
                setCenterFreq(Number(e.target.value));
              }}
              disabled={disabled}
              className="w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Độ Rộng Dải (Bandwidth): {bandwidth}
            </label>
            <input
              type="range"
              min="1"
              max="100"
              value={bandwidth}
              onChange={(e) => {
                handleManualChange();
                setBandwidth(Number(e.target.value));
              }}
              disabled={disabled}
              className="w-full"
            />
          </div>
        </>
      )}

      {/* Nút Xử Lý Ảnh */}
      <div className="pt-4 border-t border-gray-200">
        <button
          onClick={handleProcess}
          disabled={disabled}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
        >
          {disabled ? 'Đang xử lý...' : 'Xử Lý Ảnh'}
        </button>
      </div>
    </div>
  );
};

export default FilterControl;

