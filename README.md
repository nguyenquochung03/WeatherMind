# 🌤️ WeatherMind Pro

WeatherMind Pro là một ứng dụng dự báo và phân tích thời tiết toàn diện, kết hợp dữ liệu thời tiết trực tiếp (real-time) với sức mạnh của Trí tuệ Nhân tạo (AI) thông qua OpenRouter. Ứng dụng cung cấp các biểu đồ phân tích xu hướng chi tiết và khả năng tư vấn, dự đoán sâu sắc từ AI.

## ✨ Tính năng nổi bật

- **🗺️ Giao diện Hiện đại "Professional Light Mode":** Cung cấp trải nghiệm người dùng tuyệt vời với thiết kế UI dạng 2 cột (sidebar và phần nội dung), hiệu ứng "Liquid glass", và các overlay spinner loading tùy chỉnh chuyên nghiệp.
- **📊 Phân tích & Xu hướng (Analytics & Trends):** Các biểu đồ động và tương tác cao được xây dựng thông qua thư viện `Plotly` và `Pandas`, giúp người dùng dễ dàng theo dõi biến động thời tiết.
- **🤖 Tư vấn AI (AI Prediction):** Tích hợp mạnh mẽ API của OpenRouter (mặc định hỗ trợ các model miễn phí như Llama 3) giúp người dùng nhận được các lời khuyên thực tế về kế hoạch trong ngày dựa trên điều kiện thời tiết.
- **⏱️ Dữ liệu Thời gian thực:** Chấm xanh nhấp nháy liên tục cho thấy trạng thái cập nhật dữ liệu trực tiếp.

## 🛠️ Trải nghiệm Công nghệ

- **Ngôn ngữ:** Python 3.9+
- **Framework Giao diện:** Gradio (với CSS tuỳ chỉnh cho giao diện siêu việt)
- **Xử lý logic & Dữ liệu:** Pandas, Plotly, Requests
- **Tích hợp:** OpenRouter API (cho AI) và Open-Meteo API / Các API thời tiết tương đương.

## 🚀 Hướng dẫn Cài đặt & Chạy ứng dụng

### 1. Yêu cầu hệ thống
Hãy chắc chắn rằng máy bạn đã cài đặt sẵn Python và `pip`.

### 2. Thiết lập dự án

Clone repository về máy và di chuyển vào thư mục dự án:
```bash
git clone <url-repository>
cd WeatherMind
```

Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Cấu hình Biến môi trường

Ứng dụng cần có cấu hình API Key để hoạt động phần tương tác AI. 

Tạo một file `.env` ở thư mục gốc (bạn có thể copy từ `.env.example`) và điền các thông số:
```env
# Đăng ký miễn phí tại https://openrouter.ai
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Model AI sử dụng (mặc định model miễn phí)
AI_MODEL=meta-llama/llama-3.2-3b-instruct:free

# Thiết lập Gradio
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false
```

### 4. Khởi chạy ứng dụng

Sử dụng lệnh sau để chạy:
```bash
python app.py
```

Truy cập vào ứng dụng qua giao diện trình duyệt tại: `http://127.0.0.1:7860/`

---

### 🐳 Chạy bằng Docker

Bạn cũng có thể khởi chạy toàn bộ dự án thông qua Docker mà không cần phải thiết lập môi trường Python trên máy cá nhân.

1. **Build Docker Image**
Từ thư mục gốc dự án (nơi chứa `Dockerfile`), chạy lệnh:
```bash
docker build -t weathermind .
```

2. **Khởi chạy Docker Container**
Đảm bảo bạn đã cấu hình xong file `.env`, sau đó chạy:
```bash
docker run -d --name weathermind_app -p 7860:7860 --env-file .env weathermind
```

3. Mở trình duyệt web của bạn và truy cập: `http://localhost:7860/`

---

### ☁️ Đưa lên Web (Deploy lên Render)

Dự án này đã có sẵn `Dockerfile`, vì vậy việc đưa nó lên mạng (deploy) thông qua [Render.com](https://render.com/) là cực kỳ dễ dàng và miễn phí.

**Các bước thực hiện:**
1. Đẩy (push) thư mục dự án của bạn lên một repository trên **GitHub**.
2. Đăng ký và đăng nhập vào Dashboard của **Render.com**.
3. Nhấp vào nút **"New"** và chọn **"Web Service"**.
4. Chọn **"Build and deploy from a Git repository"** và kết nối với repository GitHub mà bạn vừa tạo.
5. Cấu hình ứng dụng:
   - **Name:** Đặt một cái tên tuỳ ý (ví dụ: *weathermind-pro*).
   - **Language/Environment:** Bạn ĐẢM BẢO chọn **`Docker`** (Render sẽ tự động nhận diện `Dockerfile`).
   - **Instance Type:** Chọn gói **Free**.
6. Cuộn xuống phần **Advanced** -> **Environment Variables**, nhấp "Add Environment Variable" và thêm:
   - `OPENROUTER_API_KEY`: Dán mã OpenRouter API Key thật của bạn vào (BẮT BUỘC).
   - `AI_MODEL`: `meta-llama/llama-3.2-3b-instruct:free` (hoặc model khác bạn muốn).
7. Nhấp vào **"Create Web Service"**. Quá trình build sẽ bắt đầu và mất khoảng vài phút.
8. Sau khi xong, Render sẽ cấp cho bạn một tên miền công khai dạng `https://weathermind-xxx.onrender.com`. Gửi link này cho bạn bè trải nghiệm nhé!

## 📁 Cấu trúc Dự án

- `app.py`: Tệp khởi chạy chính chứa cấu hình Gradio, CSS tuỳ chỉnh và layout chung.
- `config.py`: File chứa thiết lập các tham số chung.
- `ui/`: Chứa mã nguồn liên quan đến từng phần giao diện (`sidebar.py`, `chart_tab.py`, `chat_tab.py`...).
- `services/`: Các module phục vụ cho việc lấy dữ liệu (ví dụ: `weather_service.py`) và xử lý kết nối AI API (`ai_service.py`).
- `utils/`: Chứa các hàm tiện ích nhỏ (nếu có).

## 📝 Giấy phép (License)
Dự án được tạo cho mục đích thử nghiệm và học tập.
