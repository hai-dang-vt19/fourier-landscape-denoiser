const SpectrumViewer = ({ magnitudeSpectrum, filterMask }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">Phổ Fourier & Mặt Nạ Bộ Lọc</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            Biên Độ Phổ (Magnitude Spectrum)
          </h4>
          {magnitudeSpectrum ? (
            <img
              src={magnitudeSpectrum}
              alt="Magnitude Spectrum"
              className="w-full h-auto rounded-lg border border-gray-200"
            />
          ) : (
            <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
              Chưa có dữ liệu
            </div>
          )}
        </div>
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">
            Mặt Nạ Bộ Lọc (Filter Mask)
          </h4>
          {filterMask ? (
            <img
              src={filterMask}
              alt="Filter Mask"
              className="w-full h-auto rounded-lg border border-gray-200"
            />
          ) : (
            <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
              Chưa có dữ liệu
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SpectrumViewer;

