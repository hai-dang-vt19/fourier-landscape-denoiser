# Workflow Xử Lý Ảnh Phong Cảnh với Biến Đổi Fourier

## Quy Trình Xử Lý (Theo Tài Liệu)

### 1. Tách 3 Kênh RGB
- Ảnh màu được tách thành 3 kênh: Red, Green, Blue
- Mỗi kênh được xử lý độc lập để đảm bảo chất lượng màu sắc

### 2. Áp Dụng FFT Cho Từng Kênh Độc Lập
- Thực hiện biến đổi Fourier 2D (FFT) cho từng kênh RGB riêng biệt
- Mỗi kênh có phổ tần số riêng, được xử lý độc lập

### 3. Lọc Với Bán Kính r (Có Thể Điều Chỉnh)
- Áp dụng bộ lọc tần số với bán kính r (cutoff frequency)
- Mặc định: r = 20 (khuyến nghị cho ảnh phong cảnh)
- Có thể điều chỉnh từ 1-200 tùy theo nhu cầu:
  - r nhỏ (1-10): Lọc mạnh, làm mượt nhiều
  - r trung bình (20-50): Cân bằng, phù hợp cho hầu hết ảnh phong cảnh
  - r lớn (100-200): Lọc nhẹ, giữ nhiều chi tiết

### 4. Merge 3 Kênh Đã Lọc
- Thực hiện IFFT (Inverse FFT) cho từng kênh đã lọc
- Merge 3 kênh RGB lại thành ảnh màu hoàn chỉnh

### 5. Hiển Thị Kết Quả
- So sánh trực quan before/after
- Hiển thị metrics: MSE, PSNR, SSIM
- Hiển thị phổ Fourier và mặt nạ bộ lọc

## Các Loại Bộ Lọc

### Low-pass Filter (Làm Mượt)
- Loại bỏ nhiễu tần số cao
- Làm mượt ảnh, phù hợp cho ảnh chụp thiếu sáng
- Khuyến nghị: Gaussian với r=20

### High-pass Filter (Tăng Cường Biên)
- Giữ lại tần số cao, loại bỏ tần số thấp
- Tăng cường biên và chi tiết
- Phù hợp cho ảnh cần làm nét

### Band-reject Filter (Loại Bỏ Dải Tần)
- Loại bỏ một dải tần số cụ thể
- Phù hợp cho việc loại bỏ nhiễu tuần hoàn

## Use Cases

1. **Cải Thiện Ảnh Chụp Ban Đêm**
   - Low-pass filter với r=20-30
   - Loại bỏ nhiễu Gaussian từ thiếu sáng

2. **Làm Sạch Ảnh Du Lịch**
   - Low-pass filter với r=15-25
   - Giữ lại chi tiết quan trọng

3. **Tăng Chất Lượng Ảnh Nghệ Thuật**
   - High-pass filter với r=10-20
   - Tăng cường biên và độ tương phản

## Output

- Ảnh phong cảnh sắc nét hơn
- Loại bỏ nhiễu Gaussian từ chụp thiếu sáng
- So sánh trực quan before/after với metrics chính xác

