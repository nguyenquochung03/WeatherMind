import gradio as gr
from services.weather_service import get_weather
from utils.formatters import format_weather_html, format_weather_context


EMPTY_STATE_HTML = """
<div style="
    background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px;
    padding:48px 24px; text-align:center;
    box-shadow:0 1px 3px rgba(0,0,0,0.08);
">
    <div style="font-size:48px;margin-bottom:12px">🌍</div>
    <p style="font-size:16px;font-weight:600;color:#334155;margin:0 0 6px">
        Nhập tên thành phố để bắt đầu
    </p>
    <p style="font-size:13px;color:#94A3B8;margin:0">
        Hỗ trợ tất cả thành phố trên thế giới
    </p>
</div>
"""


def create_weather_tab():
    weather_state = gr.State({})

    with gr.Tab("🌤️ Thời tiết"):

        with gr.Group(elem_classes="wm-card"):
            gr.HTML('<p class="wm-label">Tra cứu thành phố</p>')
            with gr.Row(equal_height=True):
                city_input = gr.Textbox(
                    placeholder="Nhập tên thành phố... (VD: Hanoi, Tokyo, London)",
                    label="",
                    scale=5,
                    elem_classes="search-wrap",
                    max_lines=1,
                )
                search_btn = gr.Button(
                    "🔍 Tìm kiếm",
                    variant="primary",
                    scale=1,
                    min_width=120,
                    elem_classes="primary-btn",
                )

            gr.HTML('<p class="wm-label" style="margin-top:16px">Thành phố phổ biến</p>')
            with gr.Row(elem_classes="city-chips-row"):
                quick_cities = ["🇻🇳 Hà Nội", "🇻🇳 Hồ Chí Minh", "🇻🇳 Đà Nẵng", "🇯🇵 Tokyo", "🇬🇧 London", "🇺🇸 New York"]
                for city in quick_cities:
                    label = city.split(" ", 1)[1]
                    btn = gr.Button(city, size="sm", elem_classes="city-chip")
                    btn.click(fn=lambda c=label: c, outputs=city_input)

        weather_html = gr.HTML(EMPTY_STATE_HTML)

        def search_weather(city):
            city = city.strip()
            if not city:
                return EMPTY_STATE_HTML, {}, gr.update(visible=False)

            data = get_weather(city)
            html = format_weather_html(data)

            if "error" in data:
                return html, {}, gr.update(visible=False)

            return html, data, gr.update(visible=False)

        for trigger in [
            search_btn.click,
            city_input.submit,
        ]:
            trigger(
                fn=search_weather,
                inputs=[city_input],
                outputs=[weather_html, weather_state, gr.HTML(visible=False)],
                show_progress="minimal",
            )

    return weather_state
