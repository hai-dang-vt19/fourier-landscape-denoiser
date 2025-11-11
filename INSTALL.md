# 📦 Hướng Dẫn Cài Đặt Chi Tiết

Hướng dẫn chi tiết từng bước để cài đặt và chạy hệ thống.

## 🔍 Kiểm Tra Yêu Cầu

### Kiểm Tra Python

```bash
python --version
# Cần Python 3.11 hoặc cao hơn
```

Nếu chưa có Python, tải từ: https://www.python.org/downloads/

### Kiểm Tra Node.js

```bash
node --version
# Cần Node.js 18 hoặc cao hơn
npm --version
```

Nếu chưa có Node.js, tải từ: https://nodejs.org/

### Kiểm Tra Docker (Tùy chọn - Chỉ cho Backend)

```bash
docker --version
docker-compose --version
```

Nếu chưa có Docker, tải từ: https://www.docker.com/get-started

**Lưu ý:** Frontend chạy ngoài Docker để có hiệu năng tốt hơn.

## 📥 Cài Đặt Backend

### Bước 1: Di chuyển vào thư mục backend

```bash
cd backend
```

### Bước 2: Tạo Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Sau khi kích hoạt, bạn sẽ thấy `(venv)` ở đầu dòng lệnh.

### Bước 3: Cài Đặt Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Kiểm Tra Cài Đặt

```bash
python -c "import numpy, cv2, scipy, flask; print('OK')"
```

Nếu không có lỗi, cài đặt thành công!

## 📥 Cài Đặt Frontend

### Bước 1: Di chuyển vào thư mục frontend

```bash
cd frontend
```

### Bước 2: Cài Đặt Dependencies

```bash
npm install
```

Hoặc nếu dùng yarn:
```bash
yarn install
```

### Bước 3: Kiểm Tra Cài Đặt

```bash
npm run dev
```

Nếu server khởi động thành công, cài đặt đúng!

## 🐳 Cài Đặt Backend Với Docker (Tùy chọn)

**Lưu ý:** Chỉ backend chạy trong Docker. Frontend nên chạy ngoài Docker để có hiệu năng tốt hơn.

### Bước 1: Đảm bảo Docker đang chạy

Mở Docker Desktop và đợi đến khi trạng thái "Running".

### Bước 2: Build và chạy Backend

```bash
# Từ thư mục root của dự án
docker-compose up --build
```

Lần đầu tiên sẽ mất vài phút để download images và build.

### Bước 3: Kiểm Tra Backend

- Backend: http://localhost:5000/api/health

### Bước 4: Chạy Frontend Ngoài Docker

Frontend vẫn cần chạy ngoài Docker:

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:3000

## ⚙️ Cấu Hình

### Tạo File .env

Tạo file `.env` ở thư mục root:

```env
# Backend
FLASK_ENV=development
FLASK_DEBUG=1
BACKEND_PORT=5000

# Frontend
VITE_API_URL=http://localhost:5000
FRONTEND_PORT=3000
```

### Cấu Hình Ports

Nếu port 3000 hoặc 5000 đã được sử dụng:

**Backend (app.py):**
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Đổi port
```

**Frontend (vite.config.js):**
```javascript
server: {
  port: 3001,  // Đổi port
  // ...
}
```

**Docker (docker-compose.yml):**
```yaml
ports:
  - "5001:5000"  # Đổi port host
```

## ✅ Kiểm Tra Cài Đặt

### Test Backend

```bash
cd backend
python app.py
```

Mở trình duyệt: http://localhost:5000/api/health

Kết quả mong đợi:
```json
{"status": "ok", "message": "Server đang hoạt động"}
```

### Test Frontend

```bash
cd frontend
npm run dev
```

Mở trình duyệt: http://localhost:3000

Bạn sẽ thấy giao diện upload ảnh.

### Test Tích Hợp

1. Upload một ảnh phong cảnh
2. Điều chỉnh bộ lọc
3. Xem kết quả xử lý

Nếu thấy ảnh đã xử lý và metrics, hệ thống hoạt động đúng!

## 🔧 Xử Lý Lỗi Cài Đặt

### Lỗi: "pip: command not found"

**Giải pháp:**
```bash
python -m pip install --upgrade pip
```

### Lỗi: "npm: command not found"

**Giải pháp:**
- Cài đặt Node.js từ https://nodejs.org/
- Hoặc dùng nvm để quản lý Node.js versions

### Lỗi: "Permission denied" (Linux/Mac)

**Giải pháp:**
```bash
sudo chmod +x venv/bin/activate
```

### Lỗi: "Microsoft Visual C++ 14.0 is required" (Windows)

**Giải pháp:**
- Cài đặt Visual C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Hoặc cài đặt Visual Studio với C++ workload

### Lỗi: "opencv-python không cài được"

**Giải pháp:**
```bash
pip install --upgrade pip
pip install opencv-python-headless  # Thay thế nếu cần
```

### Lỗi: "Docker build failed"

**Giải pháp:**
```bash
# Xóa cache và build lại
docker-compose down
docker system prune -a
docker-compose build --no-cache
```

## 📚 Tài Liệu Tham Khảo

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Node.js Installation](https://nodejs.org/en/download/)
- [Docker Documentation](https://docs.docker.com/)
- [Vite Documentation](https://vitejs.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🆘 Cần Trợ Giúp?

Nếu gặp vấn đề không giải quyết được:
1. Kiểm tra phần Troubleshooting trong README.md
2. Tạo issue trên repository
3. Kiểm tra logs:
   - Backend: Xem output trong terminal
   - Frontend: Xem browser console (F12)
   - Docker: `docker-compose logs`

---

Sau khi cài đặt thành công, xem `QUICKSTART.md` để bắt đầu sử dụng!

