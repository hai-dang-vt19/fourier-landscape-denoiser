# 🚀 Hướng Dẫn Nhanh

Hướng dẫn nhanh để chạy hệ thống trong 5 phút.

## ⚡ Cách Nhanh Nhất

```bash
# 1. Clone repository
git clone <repository-url>
cd fourier-landscape-denoiser

# 2. Cài đặt và chạy Backend (Docker hoặc thủ công)
# Option A: Docker
docker-compose up

# Option B: Thủ công
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py

# 3. Cài đặt và chạy Frontend (Terminal mới - chạy ngoài Docker)
cd frontend
npm install
npm run dev

# 4. Mở trình duyệt
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

**Lưu ý:** Frontend chạy ngoài Docker để có hiệu năng tốt hơn.

## 📝 Cách Thủ Công

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

### Frontend (Terminal mới)

```bash
cd frontend
npm install
npm run dev
```

## 🎯 Sử Dụng

1. Mở `http://localhost:3000`
2. Upload ảnh phong cảnh
3. Chọn bộ lọc (mặc định: Gaussian Low-pass, r=20)
4. Xem kết quả!

## ⚙️ Cấu Hình Nhanh

### Ảnh Ban Đêm (Khử Nhiễu)
- Loại: **Gaussian**
- Chế độ: **Low-pass**
- Bán kính: **r = 25**

### Ảnh Du Lịch (Làm Sạch)
- Loại: **Gaussian**
- Chế độ: **Low-pass**
- Bán kính: **r = 20**

### Ảnh Nghệ Thuật (Tăng Nét)
- Loại: **Butterworth**
- Chế độ: **High-pass**
- Bán kính: **r = 15**
- Bậc: **2**

---

Xem `README.md` để biết chi tiết đầy đủ!

