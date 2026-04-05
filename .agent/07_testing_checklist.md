# 07 — Testing Checklist

## Checklist trước khi demo

### ✅ Setup
- [ ] Đã cài đủ dependencies (`pip install -r requirements.txt`)
- [ ] File `.env` tồn tại và có `OPENROUTER_API_KEY`
- [ ] Chạy `python test_apis.py` — cả 2 test đều pass

### ✅ Tab Thời tiết
- [ ] Nhập "Hanoi" → hiện weather card với nhiệt độ và icon
- [ ] Nhập "Ho Chi Minh City" → hiển thị đúng
- [ ] Nhập tên sai "xyzxyz123" → hiện thông báo lỗi rõ ràng
- [ ] Nhập trống → hiện cảnh báo (không crash)
- [ ] Nhấn Enter (submit) trong textbox → hoạt động như click button
- [ ] Quick buttons ("Hà Nội", "Đà Nẵng"...) → tự điền và tìm kiếm

### ✅ Tab Biểu đồ
- [ ] Sau khi tra cứu thành phố → biểu đồ tự cập nhật
- [ ] Biểu đồ hiển thị 7 ngày, có 2 đường nhiệt độ max/min
- [ ] Có cột bar chart lượng mưa
- [ ] Tiêu đề biểu đồ hiển thị tên thành phố đúng
- [ ] Nút "Cập nhật biểu đồ" hoạt động

### ✅ Tab AI Chat
- [ ] Gửi tin nhắn → AI phản hồi trong vài giây
- [ ] Streaming hoạt động (text xuất hiện dần, không chờ hết rồi mới hiện)
- [ ] AI biết thông tin thời tiết của thành phố đã tra cứu
- [ ] Nút "Xóa" → xóa lịch sử chat
- [ ] Câu hỏi gợi ý click → điền vào input box
- [ ] Không có API key → hiện thông báo hướng dẫn rõ ràng

### ✅ General UX
- [ ] App load trong < 3 giây
- [ ] Không có lỗi trong terminal khi dùng bình thường
- [ ] Giao diện đẹp trên màn hình 1080p
- [ ] Tab title trên browser hiển thị "WeatherMind"

---

## Lỗi thường gặp & cách fix

### Lỗi: "Module not found"
```bash
# Chạy từ đúng thư mục
cd weathermind
python app.py  # ĐÚNG

# Sai nếu chạy từ ngoài:
python weathermind/app.py  # SAI — import path sẽ lỗi
```

### Lỗi: Open-Meteo không trả về results
```python
# Kiểm tra spelling thành phố
# Dùng tiếng Anh: "Ho Chi Minh City" thay vì "Hồ Chí Minh"
# Hoặc dùng tên quốc tế: "Hanoi", "Da Nang"
```

### Lỗi: OpenRouter 401 Unauthorized
```
→ Kiểm tra OPENROUTER_API_KEY trong .env
→ Key phải bắt đầu bằng "sk-or-"
→ Thử generate key mới trên openrouter.ai
```

### Lỗi: OpenRouter 429 Rate Limited
```
→ Model free có giới hạn request/ngày
→ Chờ vài phút hoặc đổi sang model khác:
   "google/gemma-3-12b-it:free"
   "meta-llama/llama-3.2-3b-instruct:free"
```

### Streaming không hoạt động
```python
# Đảm bảo app có queue:
app.queue()
app.launch(...)

# Và generator function dùng yield, không return
def respond(...):
    for chunk in stream_chat_with_ai(...):
        yield "", history  # ĐÚNG — yield
    # return "", history  # SAI — không dùng return
```

### Biểu đồ không cập nhật khi chuyển tab
```python
# Dùng weather_state.change() thay vì chỉ dùng refresh_btn
weather_state.change(
    fn=create_forecast_chart,
    inputs=[weather_state],
    outputs=[chart]
)
```

---

## Mở rộng ý tưởng (sau khi hoàn thành cơ bản)

| Tính năng | Độ khó | Mô tả |
|-----------|--------|-------|
| Dark mode toggle | ⭐ | Thêm nút switch theme |
| Export PDF | ⭐⭐ | Xuất báo cáo thời tiết |
| So sánh 2 thành phố | ⭐⭐ | Dual column layout |
| Thông báo thời tiết | ⭐⭐ | Alert khi mưa/bão |
| Map tương tác | ⭐⭐⭐ | Embed Leaflet.js trong gr.HTML |
| Multi-language | ⭐⭐⭐ | Dropdown chọn ngôn ngữ |

---

## Tóm tắt những gì đã học

```
Gradio Blocks          → Layout phức tạp, multi-tab
gr.State               → Chia sẻ data giữa components
Event chaining         → .click(), .submit(), .change()
REST API calls         → requests library, error handling
Streaming AI           → Generator + yield + queue
Plotly charts          → Embedded trong gr.Plot()
HTML rendering         → gr.HTML() với custom styling
Environment config     → python-dotenv, config.py
```

## Chúc mừng! 🎉

Bạn đã hoàn thành WeatherMind — một ứng dụng Gradio hoàn chỉnh với:
- Real-time weather data từ Open-Meteo
- Interactive charts với Plotly  
- AI chat với streaming từ OpenRouter
- Clean architecture: services / ui / utils
