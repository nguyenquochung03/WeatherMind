# 05 — Xây dựng UI với Gradio Blocks

## Kiến thức Gradio cần nắm

| Khái niệm | Mô tả |
|-----------|-------|
| `gr.Blocks()` | Layout tùy chỉnh, thay thế Interface |
| `gr.Tab()` | Multi-tab layout |
| `gr.Row()`, `gr.Column()` | Grid layout |
| `gr.State()` | Lưu trạng thái giữa các lần gọi |
| `gr.HTML()` | Render HTML tùy chỉnh |
| `gr.Plot()` | Hiển thị Plotly/Matplotlib chart |
| `gr.Chatbot()` | Component chat tích hợp sẵn |
| `.click()`, `.submit()` | Event handlers |
| `fn`, `inputs`, `outputs` | Kết nối logic với UI |

---

## ui/weather_tab.py

```python
import gradio as gr
from services.weather_service import get_weather
from utils.formatters import format_weather_html, format_weather_context


def create_weather_tab():
    """Trả về nội dung Tab thời tiết và weather_state."""
    weather_state = gr.State({})  # Lưu data thời tiết để dùng ở tab khác

    with gr.Tab("🌤️ Thời tiết"):
        gr.Markdown("## Tra cứu thời tiết\nNhập tên thành phố để xem thời tiết hiện tại.")

        with gr.Row():
            city_input = gr.Textbox(
                placeholder="Ví dụ: Hanoi, Ho Chi Minh City, Da Nang...",
                label="Tên thành phố",
                scale=4
            )
            search_btn = gr.Button("🔍 Tìm kiếm", variant="primary", scale=1)

        # Quick select buttons
        with gr.Row():
            gr.Markdown("**Thành phố nhanh:**")
        with gr.Row():
            for city in ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Tokyo"]:
                quick_btn = gr.Button(city, size="sm")
                quick_btn.click(fn=lambda c=city: c, outputs=city_input)

        # Weather display
        weather_html = gr.HTML("<p style='color:gray;text-align:center'>👆 Nhập thành phố để xem thời tiết</p>")
        status_msg = gr.Markdown(visible=False)

        def search_weather(city):
            if not city.strip():
                return (
                    "<p style='color:orange'>⚠️ Vui lòng nhập tên thành phố</p>",
                    gr.update(visible=False),
                    {}
                )
            data = get_weather(city.strip())
            html = format_weather_html(data)
            if "error" in data:
                return html, gr.update(value="❌ " + data["error"], visible=True), {}
            return html, gr.update(visible=False), data

        search_btn.click(
            fn=search_weather,
            inputs=[city_input],
            outputs=[weather_html, status_msg, weather_state]
        )
        city_input.submit(
            fn=search_weather,
            inputs=[city_input],
            outputs=[weather_html, status_msg, weather_state]
        )

    return weather_state
```

---

## ui/chart_tab.py

```python
import gradio as gr
import plotly.graph_objects as go
import pandas as pd


def create_forecast_chart(weather_data: dict):
    """Tạo biểu đồ nhiệt độ 7 ngày từ weather data."""
    if not weather_data or "error" in weather_data:
        fig = go.Figure()
        fig.add_annotation(text="Chưa có dữ liệu — hãy tra cứu thành phố trước",
                           xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    daily = weather_data["daily"]
    dates = [d["date"] for d in daily]
    temp_max = [d["temp_max"] for d in daily]
    temp_min = [d["temp_min"] for d in daily]
    precip = [d["precipitation"] for d in daily]
    icons = [d["icon"] for d in daily]

    fig = go.Figure()

    # Area chart nhiệt độ
    fig.add_trace(go.Scatter(
        x=dates, y=temp_max, name="Nhiệt độ cao nhất",
        fill="tozeroy", fillcolor="rgba(255, 99, 71, 0.2)",
        line=dict(color="tomato", width=2),
        mode="lines+markers+text",
        text=[f"{t}°" for t in temp_max], textposition="top center"
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=temp_min, name="Nhiệt độ thấp nhất",
        fill="tozeroy", fillcolor="rgba(30, 144, 255, 0.15)",
        line=dict(color="dodgerblue", width=2),
        mode="lines+markers+text",
        text=[f"{t}°" for t in temp_min], textposition="bottom center"
    ))

    # Bar chart mưa (trục Y phụ)
    fig.add_trace(go.Bar(
        x=dates, y=precip, name="Lượng mưa (mm)",
        marker_color="rgba(100, 180, 255, 0.6)",
        yaxis="y2"
    ))

    loc = weather_data["location"]
    fig.update_layout(
        title=f"Dự báo 7 ngày — {loc['name']}, {loc['country']}",
        xaxis_title="Ngày",
        yaxis=dict(title="Nhiệt độ (°C)", side="left"),
        yaxis2=dict(title="Lượng mưa (mm)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(240,248,255,0.8)",
        height=450,
    )
    return fig


def create_chart_tab(weather_state: gr.State):
    """Tạo Tab biểu đồ."""
    with gr.Tab("📊 Biểu đồ 7 ngày"):
        gr.Markdown("## Biểu đồ dự báo nhiệt độ\nNhiệt độ và lượng mưa 7 ngày tới.")

        refresh_btn = gr.Button("🔄 Cập nhật biểu đồ", variant="secondary")
        chart = gr.Plot(label="")

        refresh_btn.click(
            fn=create_forecast_chart,
            inputs=[weather_state],
            outputs=[chart]
        )
        # Auto-update khi weather_state thay đổi
        weather_state.change(
            fn=create_forecast_chart,
            inputs=[weather_state],
            outputs=[chart]
        )
```

---

## ui/chat_tab.py

```python
import gradio as gr
from services.ai_service import stream_chat_with_ai
from utils.formatters import format_weather_context


def create_chat_tab(weather_state: gr.State):
    """Tạo Tab AI Chat."""
    with gr.Tab("🤖 AI Chat"):
        gr.Markdown("""## Hỏi AI về thời tiết
        AI sẽ tự động sử dụng dữ liệu thời tiết bạn đã tra cứu để trả lời chính xác hơn.
        """)

        chatbot = gr.Chatbot(
            value=[],
            label="WeatherMind AI",
            height=450,
            bubble_full_width=False,
            show_copy_button=True,
        )

        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Hỏi AI về thời tiết... (VD: 'Có nên mang ô hôm nay không?')",
                label="",
                scale=5
            )
            send_btn = gr.Button("Gửi ➤", variant="primary", scale=1)
            clear_btn = gr.Button("🗑️ Xóa", scale=1)

        # Quick questions
        gr.Markdown("**Câu hỏi gợi ý:**")
        with gr.Row():
            suggestions = [
                "Hôm nay nên mặc gì?",
                "Thời tiết có phù hợp để chạy bộ không?",
                "Dự báo tuần này như thế nào?",
                "Gợi ý hoạt động cuối tuần"
            ]
            for q in suggestions:
                q_btn = gr.Button(q, size="sm")
                q_btn.click(fn=lambda x=q: x, outputs=msg_input)

        def respond(message, history, weather_data):
            if not message.strip():
                return "", history
            weather_ctx = format_weather_context(weather_data) if weather_data else ""
            history = history + [[message, ""]]
            # Streaming
            for partial in stream_chat_with_ai(message, history[:-1], weather_ctx):
                history[-1][1] = partial
                yield "", history

        send_btn.click(
            fn=respond,
            inputs=[msg_input, chatbot, weather_state],
            outputs=[msg_input, chatbot]
        )
        msg_input.submit(
            fn=respond,
            inputs=[msg_input, chatbot, weather_state],
            outputs=[msg_input, chatbot]
        )
        clear_btn.click(fn=lambda: [], outputs=chatbot)
```

---

## app.py — Entry point

```python
import gradio as gr
from ui.weather_tab import create_weather_tab
from ui.chart_tab import create_chart_tab
from ui.chat_tab import create_chat_tab
from config import GRADIO_PORT, GRADIO_SHARE

CSS = """
.gradio-container { max-width: 900px !important; margin: 0 auto !important; }
footer { display: none !important; }
"""

def build_app():
    with gr.Blocks(
        title="WeatherMind 🌤️",
        theme=gr.themes.Soft(primary_hue="blue"),
        css=CSS
    ) as app:
        gr.Markdown("""
        # 🌤️ WeatherMind
        ### Thời tiết thông minh — Powered by Open-Meteo & AI
        """)

        weather_state = create_weather_tab()
        create_chart_tab(weather_state)
        create_chat_tab(weather_state)

        gr.Markdown("""
        ---
        *Data: [Open-Meteo](https://open-meteo.com) | AI: [OpenRouter](https://openrouter.ai)*
        """)

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        show_error=True,
    )
```

## Chạy ứng dụng

```bash
cd weathermind
python app.py
# Mở trình duyệt: http://localhost:7860
```

## Bước tiếp theo

→ Đọc `06_advanced_features.md` hoặc `07_testing_checklist.md`
