# 🌄 Hệ Thống Xử Lý Ảnh Phong Cảnh với Biến Đổi Fourier

Hệ thống web ứng dụng xử lý ảnh phong cảnh sử dụng biến đổi Fourier 2D để khử nhiễu, làm mượt và tăng cường chất lượng ảnh. Hệ thống hỗ trợ xử lý ảnh màu RGB với các bộ lọc tần số: Low-pass, High-pass, và Band-reject.

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Cách Chạy](#cách-chạy)
- [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## ✨ Tính Năng

- ✅ **Xử lý ảnh RGB**: Tách và xử lý từng kênh màu độc lập
- ✅ **Biến đổi Fourier 2D**: FFT/IFFT cho từng kênh RGB
- ✅ **Bộ lọc tần số**: 
  - Low-pass (làm mượt, khử nhiễu)
  - High-pass (tăng cường biên)
  - Band-reject (loại bỏ dải tần)
- ✅ **3 loại bộ lọc**: Ideal, Butterworth, Gaussian
- ✅ **Metrics đánh giá**: MSE, PSNR, SSIM
- ✅ **Giao diện trực quan**: So sánh before/after, hiển thị phổ Fourier
- ✅ **Tối ưu hiệu năng**: Cache mask, FFT tối ưu, debounce frontend

## 🖥️ Yêu Cầu Hệ Thống

### Backend
- Python 3.11+ 
- pip (Python package manager)
- Các thư viện Python (xem `backend/requirements.txt`)

### Frontend
- Node.js 18+ và npm/yarn
- Các package npm (xem `frontend/package.json`)

### Docker (Tùy chọn - Chỉ cho Backend)
- Docker Desktop
- Docker Compose
- **Lưu ý:** Frontend chạy ngoài Docker để có hiệu năng tốt hơn

## 📦 Cài Đặt

### Phương Pháp 1: Cài Đặt Thủ Công

#### 1. Clone Repository

```bash
git clone <repository-url>
cd fourier-landscape-denoiser
```

#### 2. Cài Đặt Backend

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

#### 3. Cài Đặt Frontend

```bash
# Di chuyển vào thư mục frontend
cd ../frontend

# Cài đặt dependencies
npm install
# hoặc
yarn install
```

### Phương Pháp 2: Sử Dụng Docker cho Backend (Tùy chọn)

```bash
# Chạy backend với Docker
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

**Lưu ý:** Frontend nên chạy ngoài Docker để có hiệu năng tốt hơn.

## 🚀 Cách Chạy

### Chạy Thủ Công

#### 1. Khởi Động Backend

```bash
# Từ thư mục backend
cd backend

# Kích hoạt virtual environment (nếu chưa kích hoạt)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Chạy Flask server
python app.py
```

Backend sẽ chạy tại: `http://localhost:5000`

#### 2. Khởi Động Frontend

```bash
# Từ thư mục frontend (terminal mới)
cd frontend

# Chạy development server
npm run dev
# hoặc
yarn dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

### Chạy Với Docker (Chỉ Backend)

```bash
# Từ thư mục root của dự án
docker-compose up

# Backend API: http://localhost:5000
# Frontend vẫn chạy ngoài Docker: http://localhost:3000
```

## 📖 Hướng Dẫn Sử Dụng

### 1. Upload Ảnh

- Click vào vùng "Kéo thả ảnh vào đây hoặc click để chọn"
- Hoặc kéo thả file ảnh trực tiếp vào vùng upload
- Hỗ trợ định dạng: PNG, JPG, JPEG, BMP, TIFF (tối đa 16MB)

### 2. Cấu Hình Bộ Lọc

#### Loại Bộ Lọc
- **Ideal**: Cắt sắc nét, có thể tạo ringing artifacts
- **Butterworth**: Mượt mà, có thể điều chỉnh bậc
- **Gaussian**: Mượt nhất, ít artifacts (khuyến nghị)

#### Chế Độ Lọc
- **Low-pass**: Làm mượt, khử nhiễu (phù hợp cho ảnh ban đêm)
- **High-pass**: Tăng cường biên, chi tiết
- **Band-reject**: Loại bỏ dải tần số cụ thể

#### Bán Kính Lọc (r)
- **r = 1-10**: Lọc mạnh, làm mượt nhiều
- **r = 20**: Khuyến nghị cho hầu hết ảnh phong cảnh
- **r = 50-200**: Lọc nhẹ, giữ nhiều chi tiết

### 3. Xem Kết Quả

Sau khi xử lý, bạn sẽ thấy:
- **So sánh ảnh**: Before/After side-by-side
- **Phổ Fourier**: Biên độ phổ và mặt nạ bộ lọc
- **Metrics**: MSE, PSNR, SSIM để đánh giá chất lượng

### 4. Use Cases

#### Cải Thiện Ảnh Chụp Ban Đêm
```
Loại bộ lọc: Gaussian
Chế độ: Low-pass
Bán kính: r = 20-30
```

#### Làm Sạch Ảnh Du Lịch
```
Loại bộ lọc: Gaussian
Chế độ: Low-pass
Bán kính: r = 15-25
```

#### Tăng Chất Lượng Ảnh Nghệ Thuật
```
Loại bộ lọc: Butterworth
Chế độ: High-pass
Bán kính: r = 10-20
Bậc: 2-3
```

## 🔌 API Documentation

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Server đang hoạt động"
}
```

### Process Image

```http
POST /api/process
Content-Type: multipart/form-data
```

**Parameters:**
- `image` (file): File ảnh cần xử lý
- `filter_type` (string): 'ideal', 'butterworth', 'gaussian'
- `filter_mode` (string): 'lowpass', 'highpass', 'bandreject'
- `cutoff` (float): Bán kính lọc (ví dụ: 20)
- `order` (int): Bậc bộ lọc (chỉ cho Butterworth, mặc định: 2)
- `center_freq` (float, optional): Tần số trung tâm (cho band-reject)
- `bandwidth` (float, optional): Độ rộng dải (cho band-reject)

**Response:**
```json
{
  "success": true,
  "original_image": "data:image/png;base64,...",
  "processed_image": "data:image/png;base64,...",
  "magnitude_spectrum": "data:image/png;base64,...",
  "filter_mask": "data:image/png;base64,...",
  "metrics": {
    "mse": 123.45,
    "psnr": 35.67,
    "ssim": 0.9234
  }
}
```

### Upload Image

```http
POST /api/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `image` (file): File ảnh cần upload

**Response:**
```json
{
  "success": true,
  "filename": "image.jpg",
  "filepath": "uploads/image.jpg",
  "preview": "data:image/png;base64,..."
}
```

## 🛠️ Troubleshooting

### Lỗi: "Không thể kết nối đến server"

**Nguyên nhân:** Backend chưa chạy hoặc sai port

**Giải pháp:**
1. Kiểm tra backend đang chạy tại `http://localhost:5000`
2. Kiểm tra file `.env` có `VITE_API_URL=http://localhost:5000`
3. Restart cả backend và frontend

### Lỗi: "Module not found" khi chạy backend

**Nguyên nhân:** Chưa cài đặt dependencies

**Giải pháp:**
```bash
cd backend
pip install -r requirements.txt
```

### Lỗi: "Cannot find module" khi chạy frontend

**Nguyên nhân:** Chưa cài đặt node_modules

**Giải pháp:**
```bash
cd frontend
npm install
```

### Ảnh xử lý bị mờ hoặc có artifacts

**Nguyên nhân:** Bán kính lọc quá nhỏ hoặc loại bộ lọc không phù hợp

**Giải pháp:**
- Tăng bán kính lọc (r) lên 30-50
- Thử chuyển sang bộ lọc Gaussian thay vì Ideal
- Giảm bậc bộ lọc Butterworth xuống 1-2

### Docker không build được

**Nguyên nhân:** Dockerfile có lỗi hoặc thiếu dependencies

**Giải pháp:**
1. Kiểm tra Docker đang chạy
2. Xóa cache và build lại:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Port đã được sử dụng

**Giải pháp:**
- Thay đổi port trong `docker-compose.yml` hoặc `.env`
- Hoặc dừng service đang dùng port đó

## 📁 Cấu Trúc Dự Án

```
fourier-landscape-denoiser/
├── backend/
│   ├── core/              # Core modules (Fourier, Filters, Metrics)
│   ├── utils/              # Utilities (IO, Validation)
│   ├── uploads/             # Thư mục upload ảnh
│   ├── results/            # Thư mục kết quả
│   ├── app.py              # Flask API server
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Docker config cho backend
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── App.jsx          # Main app component
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite config
├── data/
│   ├── sample_images/       # Ảnh mẫu
│   └── results/             # Kết quả lưu trữ
├── docker-compose.yml       # Docker Compose config
├── .env                     # Environment variables
└── README.md                # File này
```

## 🔧 Development

### Chạy Tests (Nếu có)

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Build Production

```bash
# Frontend
cd frontend
npm run build

# Output sẽ ở frontend/dist/
```

## 📝 Notes

- Hệ thống tự động xử lý ảnh RGB bằng cách tách 3 kênh và xử lý độc lập
- FFT được tối ưu với `scipy.fft.next_fast_len` để tăng tốc
- Mask được cache để tránh tính toán lại
- Frontend có debounce để giảm số lần gọi API

## 📄 License

[Thêm license của bạn ở đây]

## 👥 Contributors

[Thêm thông tin contributors]

## 🙏 Acknowledgments

- NumPy, OpenCV, SciPy cho xử lý ảnh và FFT
- React, Vite cho frontend framework
- Flask cho backend API

---

**Lưu ý:** Đảm bảo backend đang chạy trước khi sử dụng frontend. Nếu gặp vấn đề, xem phần Troubleshooting hoặc tạo issue trên repository.

