const ComparisonView = ({ originalImage, processedImage }) => {
  if (!originalImage && !processedImage) {
    return (
      <div className="bg-white p-8 rounded-lg shadow-md text-center text-gray-500">
        <p>Chưa có ảnh để so sánh</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-blue-950 text-xl font-semibold mb-4">So Sánh Ảnh</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Ảnh Gốc</h4>
          {originalImage ? (
            <img
              src={originalImage}
              alt="Original"
              className="w-full h-auto rounded-lg border border-gray-200"
            />
          ) : (
            <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
              Chưa có ảnh
            </div>
          )}
        </div>
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Ảnh Đã Xử Lý</h4>
          {processedImage ? (
            <img
              src={processedImage}
              alt="Processed"
              className="w-full h-auto rounded-lg border border-gray-200"
            />
          ) : (
            <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
              Chưa có ảnh
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComparisonView;

