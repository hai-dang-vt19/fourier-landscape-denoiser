# 🔨 Hướng Dẫn Build Production

Hướng dẫn build hệ thống cho môi trường production.

## 🎯 Build Frontend Production

### Bước 1: Build Static Files

```bash
cd frontend
npm run build
```

Output sẽ ở thư mục `frontend/dist/`

### Bước 2: Test Build

```bash
npm run preview
```

Mở http://localhost:4173 để kiểm tra.

### Bước 3: Deploy

Copy thư mục `dist/` lên web server (Nginx, Apache, etc.)

## 🐳 Build Docker Images (Chỉ Backend)

**Lưu ý:** Frontend không build với Docker. Chỉ backend sử dụng Docker.

### Build Backend

```bash
docker-compose build
```

### Build Với No Cache

```bash
docker-compose build --no-cache
```

## 📦 Tạo Production Dockerfile

### Backend Production Dockerfile

Tạo `backend/Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p uploads results

# Use production WSGI server
RUN pip install gunicorn

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Frontend Production (Không Dùng Docker)

Frontend được build và deploy trực tiếp không qua Docker:

1. Build static files: `npm run build`
2. Deploy thư mục `dist/` lên web server (Nginx, Apache, etc.)
3. Cấu hình Nginx để serve static files và proxy API requests đến backend

**Lưu ý:** Frontend không sử dụng Docker để có hiệu năng tốt hơn.

## 🚀 Deploy Production

### Backend Với Docker

```bash
# Chạy backend trong Docker
docker-compose up -d
```

### Backend Với Gunicorn (Không Docker)

```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (Không Docker)

1. Build frontend: `cd frontend && npm run build`
2. Copy thư mục `dist/` vào web server (ví dụ: `/var/www/html/`)
3. Cấu hình Nginx để serve static files
4. Cấu hình reverse proxy cho API requests đến backend

**Lưu ý:** Frontend không sử dụng Docker, chỉ build và deploy static files.

## 🔒 Security Checklist

- [ ] Đặt `FLASK_DEBUG=0` trong production
- [ ] Sử dụng HTTPS
- [ ] Giới hạn file upload size
- [ ] Validate tất cả inputs
- [ ] Sử dụng environment variables cho secrets
- [ ] Cấu hình CORS đúng cách
- [ ] Enable rate limiting
- [ ] Log errors properly
- [ ] Backup database (nếu có)

## 📊 Performance Optimization

### Backend

1. **Sử dụng Gunicorn với workers:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Enable caching:**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

3. **Optimize image processing:**
- Giảm kích thước ảnh trước khi xử lý
- Sử dụng multiprocessing cho batch processing

### Frontend

1. **Code splitting:**
```javascript
// vite.config.js
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom']
      }
    }
  }
}
```

2. **Image optimization:**
- Compress images trước khi upload
- Lazy load images

3. **CDN:**
- Serve static assets từ CDN

## 🧪 Testing Production Build

### Test Backend

```bash
curl http://localhost:5000/api/health
```

### Test Frontend

```bash
# Build và preview
cd frontend
npm run build
npm run preview
```

### Test Backend Docker

```bash
# Chạy backend trong Docker
docker-compose up

# Test backend endpoint
curl http://localhost:5000/api/health
```

**Lưu ý:** Frontend chạy ngoài Docker, test frontend bằng cách chạy `npm run dev` trong thư mục frontend.

## 📝 Environment Variables Production

Tạo `.env.prod`:

```env
FLASK_ENV=production
FLASK_DEBUG=0
BACKEND_PORT=5000

VITE_API_URL=https://api.yourdomain.com
FRONTEND_PORT=3000
```

## 🔄 CI/CD Example (GitHub Actions)

Tạo `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker-compose build
          # Push to registry
      
      - name: Deploy
        run: |
          # Deploy commands
```

---

Xem `README.md` để biết thêm chi tiết về cấu hình và troubleshooting.

