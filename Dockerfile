# Sử dụng image Python phiên bản thon gọn (slim)
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Khắc phục lỗi thiếu thư viện khi chạy một số tính năng của hệ điều hành
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements.txt trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào trong container
COPY . .

# Khai báo port mà container sẽ chạy
EXPOSE 7860

# Lệnh khởi chạy ứng dụng
CMD ["python", "-u", "app.py"]
