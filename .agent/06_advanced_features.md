# 06 — Tính năng nâng cao

## 1. Loading State (hiển thị spinner khi đang tải)

```python
# Trong weather_tab.py
search_btn.click(
    fn=search_weather,
    inputs=[city_input],
    outputs=[weather_html, status_msg, weather_state],
    # Hiện spinner trên nút trong khi fn đang chạy
    show_progress="minimal"
)

# Hoặc disable input trong lúc chờ:
search_btn.click(
    fn=search_weather,
    inputs=[city_input],
    outputs=[weather_html, status_msg, weather_state],
).then(
    fn=lambda: gr.update(interactive=True),
    outputs=[search_btn]
)
```

## 2. Error Handling UI đẹp

```python
def search_weather_safe(city):
    """Wrapper với error handling toàn diện."""
    try:
        if len(city.strip()) < 2:
            return (
                _error_html("Tên thành phố quá ngắn"),
                {}
            )
        data = get_weather(city.strip())
        return format_weather_html(data), data

    except Exception as e:
        return _error_html(f"Lỗi không mong đợi: {e}"), {}


def _error_html(msg):
    return f"""
    <div style="background:#fff3cd;border:1px solid #ffc107;
                border-radius:8px;padding:16px;color:#856404">
        ⚠️ {msg}
    </div>
    """
```

## 3. Gradio Themes & Custom CSS

```python
# Dùng theme có sẵn
theme = gr.themes.Soft(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.sky,
    neutral_hue=gr.themes.colors.slate,
    font=gr.themes.GoogleFont("Inter"),
)

# Custom CSS nâng cao
CSS = """
/* Card shadow */
.weather-card { box-shadow: 0 4px 20px rgba(0,0,0,0.1); }

/* Button hover */
.primary-btn:hover { transform: translateY(-1px); transition: 0.2s; }

/* Chatbot bubble */
.chatbot .message { border-radius: 12px !important; }

/* Tab active indicator */
.tab-nav button.selected { border-bottom: 3px solid #2980b9 !important; }
"""
```

## 4. gr.State — Chia sẻ data giữa các Tab

```python
# Trong app.py — tạo 1 state dùng chung
with gr.Blocks() as app:
    # State này accessible từ TẤT CẢ tabs
    shared_weather = gr.State({})
    shared_city = gr.State("")

    # Pass state vào từng tab function
    weather_state = create_weather_tab(shared_weather, shared_city)
    create_chart_tab(shared_weather)
    create_chat_tab(shared_weather)
```

## 5. Auto-refresh Chart khi chuyển Tab

```python
# Dùng gr.Tab(id=...) và app.select()
with gr.Tabs() as tabs:
    with gr.Tab("📊 Biểu đồ", id="chart"):
        chart = gr.Plot()

# Khi chọn tab chart → tự cập nhật
tabs.select(
    fn=lambda data, selected: create_forecast_chart(data) if selected.index == 1 else None,
    inputs=[weather_state],
    outputs=[chart]
)
```

## 6. Gradio Queue — Xử lý nhiều request đồng thời

```python
# Trong app.py — QUAN TRỌNG cho streaming
app.queue(
    max_size=20,           # Tối đa 20 requests đợi
    default_concurrency_limit=5  # Tối đa 5 chạy đồng thời
)

app.launch(server_port=7860)
```

## 7. Thêm Tab Lịch sử tìm kiếm

```python
def create_history_tab(history_state: gr.State):
    with gr.Tab("📋 Lịch sử"):
        history_df = gr.Dataframe(
            headers=["Thành phố", "Nhiệt độ", "Thời tiết", "Thời gian"],
            datatype=["str", "str", "str", "str"],
            interactive=False
        )
        clear_hist_btn = gr.Button("🗑️ Xóa lịch sử")

        # Update khi weather thay đổi
        # history_state là list of dicts
        def add_to_history(weather_data, history):
            if not weather_data or "error" in weather_data:
                return history, gr.update()
            from datetime import datetime
            entry = {
                "city": weather_data["location"]["name"],
                "temp": f"{weather_data['current']['temperature']}°C",
                "desc": weather_data["current"]["description"],
                "time": datetime.now().strftime("%H:%M %d/%m")
            }
            history = [entry] + history[:9]  # Giữ 10 entry gần nhất
            rows = [[e["city"], e["temp"], e["desc"], e["time"]] for e in history]
            return history, rows

        return history_state
```

## 8. Deploy lên Hugging Face Spaces (miễn phí)

```bash
# 1. Tạo account tại huggingface.co
# 2. Tạo Space mới, chọn SDK = Gradio

# 3. Thêm file requirements.txt vào repo
# 4. Set secrets (thay .env):
#    Settings → Repository secrets → OPENROUTER_API_KEY

# 5. Trong app.py, launch không cần port:
if __name__ == "__main__":
    app.launch()

# 6. Push code:
git init
git add .
git commit -m "Initial WeatherMind"
git remote add origin https://huggingface.co/spaces/USERNAME/weathermind
git push -u origin main
```

## Bước tiếp theo

→ Đọc `07_testing_checklist.md`
