"""
utils/formatters.py — Text formatters for weather data using native Gradio components
"""

import gradio as gr


def format_weather_markdown(weather_data: dict) -> str:
    """Returns a formatted Markdown string for the weather display."""

    if "error" in weather_data:
        return f"""## ⚠️ Không tìm thấy thành phố

**{weather_data['error']}**

_Vui lòng thử lại với tên thành phố khác._
"""

    if not weather_data:
        return """## 🌍 Khám phá thời tiết

Nhập tên thành phố ở ô tìm kiếm bên trên để xem dữ liệu thời tiết real-time.
"""

    loc = weather_data["location"]
    curr = weather_data["current"]
    daily = weather_data.get("daily", [])

    # Build forecast rows
    forecast_rows = []
    for d in daily[1:4]:
        date_short = d["date"][5:]  # MM-DD format
        forecast_rows.append(
            f"| {date_short} | {d['icon']} | {d['temp_min']}°C - {d['temp_max']}°C | 💧{d['precipitation']}mm |"
        )

    forecast_section = ""
    if forecast_rows:
        forecast_section = """

### 📅 Dự báo 3 ngày tới

| Ngày | Thời tiết | Nhiệt độ | Mưa |
|------|-----------|----------|-----|
""" + "\n".join(forecast_rows)

    return f"""## 📍 {loc['name']}, {loc['country']}

*{loc.get('timezone', '')}*

# {curr['icon']} {curr['temperature']}°C

**{curr['description']}**

_Cảm giác như {curr['feels_like']}°C_

---

### 💧 Độ ẩm: {curr['humidity']}%
### 💨 Gió: {curr['wind_speed']} km/h
{forecast_section}
"""


def format_weather_gradio():
    """Creates and returns a Gradio Markdown component for weather display."""
    return gr.Markdown(
        value="""## 🌍 Khám phá thời tiết

Nhập tên thành phố ở ô tìm kiếm bên trên để xem dữ liệu thời tiết real-time.
""",
        label="Thời tiết hiện tại",
    )


def format_weather_context(weather_data: dict) -> str:
    """Returns plain-text weather context for the AI prompt."""
    if not weather_data or "error" in weather_data:
        return ""
    loc = weather_data["location"]
    curr = weather_data["current"]
    daily = weather_data.get("daily", [])
    lines = [
        f"Địa điểm: {loc['name']}, {loc['country']}",
        f"Nhiệt độ: {curr['temperature']}°C (cảm giác {curr['feels_like']}°C)",
        f"Thời tiết: {curr['icon']} {curr['description']}",
        f"Độ ẩm: {curr['humidity']}% | Gió: {curr['wind_speed']} km/h",
    ]
    if daily:
        lines.append("Dự báo 3 ngày tới:")
        for d in daily[:3]:
            lines.append(f"  {d['date']}: {d['icon']} {d['temp_min']}–{d['temp_max']}°C, mưa {d['precipitation']}mm")
    return "\n".join(lines)
