import { useState, useEffect } from 'react';

const FilterControl = ({ onFilterChange, disabled = false }) => {
  const [filterType, setFilterType] = useState('gaussian');
  const [filterMode, setFilterMode] = useState('lowpass');
  const [cutoff, setCutoff] = useState(20); // Mặc định r=20 theo tài liệu
  const [order, setOrder] = useState(2);
  const [centerFreq, setCenterFreq] = useState(50);
  const [bandwidth, setBandwidth] = useState(25);

  useEffect(() => {
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

    onFilterChange(params);
  }, [filterType, filterMode, cutoff, order, centerFreq, bandwidth]);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h3 className="text-xl font-semibold mb-4">Cài Đặt Bộ Lọc</h3>

      {/* Loại bộ lọc */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Loại Bộ Lọc
        </label>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="ideal">Ideal</option>
          <option value="butterworth">Butterworth</option>
          <option value="gaussian">Gaussian</option>
        </select>
      </div>

      {/* Chế độ lọc */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Chế Độ Lọc
        </label>
        <select
          value={filterMode}
          onChange={(e) => setFilterMode(e.target.value)}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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
          onChange={(e) => setCutoff(Number(e.target.value))}
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
            onChange={(e) => setOrder(Number(e.target.value))}
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
              onChange={(e) => setCenterFreq(Number(e.target.value))}
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
              onChange={(e) => setBandwidth(Number(e.target.value))}
              disabled={disabled}
              className="w-full"
            />
          </div>
        </>
      )}
    </div>
  );
};

export default FilterControl;

