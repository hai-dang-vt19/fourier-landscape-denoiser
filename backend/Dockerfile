FROM python:3.11-slim

WORKDIR /app

# Cài đặt các dependencies hệ thống
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Tạo các thư mục cần thiết
RUN mkdir -p uploads results

# Expose port
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app.py"]

