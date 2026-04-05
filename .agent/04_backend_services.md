# 04 — Backend Services

## services/weather_service.py

```python
import requests
from config import GEOCODING_URL, WEATHER_BASE_URL, REQUEST_TIMEOUT

WEATHER_CODES = {
    0: ("Trời quang", "☀️"), 1: ("Chủ yếu quang", "🌤️"),
    2: ("Có mây một phần", "⛅"), 3: ("Nhiều mây", "☁️"),
    45: ("Sương mù", "🌫️"), 48: ("Sương mù có băng", "🌫️"),
    51: ("Mưa phùn nhẹ", "🌦️"), 53: ("Mưa phùn", "🌦️"),
    61: ("Mưa nhỏ", "🌧️"), 63: ("Mưa vừa", "🌧️"), 65: ("Mưa lớn", "🌧️"),
    80: ("Mưa rào nhẹ", "🌦️"), 81: ("Mưa rào", "🌧️"), 82: ("Mưa rào lớn", "⛈️"),
    95: ("Dông bão", "⛈️"), 99: ("Dông kèm mưa đá", "⛈️"),
}


def get_coordinates(city_name: str) -> dict:
    """Chuyển tên thành phố thành tọa độ lat/lon."""
    try:
        resp = requests.get(
            GEOCODING_URL,
            params={"name": city_name, "count": 1, "language": "en", "format": "json"},
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()

        if not data.get("results"):
            return {"error": f"Không tìm thấy thành phố: {city_name}"}

        r = data["results"][0]
        return {
            "name": r["name"],
            "country": r.get("country", ""),
            "country_code": r.get("country_code", ""),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "timezone": r.get("timezone", "UTC"),
        }
    except requests.RequestException as e:
        return {"error": f"Lỗi kết nối: {str(e)}"}


def get_weather(city_name: str) -> dict:
    """Lấy thời tiết hiện tại + 7 ngày tới."""
    coords = get_coordinates(city_name)
    if "error" in coords:
        return coords

    try:
        resp = requests.get(
            WEATHER_BASE_URL,
            params={
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
                "timezone": coords["timezone"],
                "forecast_days": 7,
            },
            timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        raw = resp.json()

        # Parse current weather
        curr = raw["current"]
        code = curr.get("weather_code", 0)
        desc, icon = WEATHER_CODES.get(code, ("Không xác định", "❓"))

        current = {
            "temperature": curr["temperature_2m"],
            "feels_like": curr["apparent_temperature"],
            "humidity": curr["relative_humidity_2m"],
            "wind_speed": curr["wind_speed_10m"],
            "description": desc,
            "icon": icon,
        }

        # Parse daily forecast
        daily_raw = raw["daily"]
        daily = []
        for i in range(len(daily_raw["time"])):
            d_code = daily_raw["weather_code"][i]
            d_desc, d_icon = WEATHER_CODES.get(d_code, ("Không xác định", "❓"))
            daily.append({
                "date": daily_raw["time"][i],
                "temp_max": daily_raw["temperature_2m_max"][i],
                "temp_min": daily_raw["temperature_2m_min"][i],
                "precipitation": daily_raw["precipitation_sum"][i],
                "description": d_desc,
                "icon": d_icon,
            })

        return {
            "location": coords,
            "current": current,
            "daily": daily,
        }

    except requests.RequestException as e:
        return {"error": f"Lỗi lấy dữ liệu thời tiết: {str(e)}"}
```

---

## services/ai_service.py

```python
import requests
import json
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODEL

SYSTEM_PROMPT = """Bạn là WeatherMind AI, trợ lý thời tiết thông minh.
Bạn trả lời bằng tiếng Việt, ngắn gọn, thân thiện.
Khi được cung cấp dữ liệu thời tiết, hãy phân tích và đưa ra lời khuyên hữu ích.
Gợi ý trang phục, hoạt động phù hợp với thời tiết."""


def chat_with_ai(
    user_message: str,
    history: list,
    weather_context: str = ""
) -> str:
    """Gửi message đến AI và nhận phản hồi."""
    if not OPENROUTER_API_KEY:
        return "⚠️ Chưa cấu hình OPENROUTER_API_KEY trong file .env"

    # Build messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if weather_context:
        messages.append({
            "role": "system",
            "content": f"Dữ liệu thời tiết hiện tại:\n{weather_context}"
        })

    # Add history (Gradio format: list of [user, assistant])
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": user_message})

    try:
        resp = requests.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:7860",
                "X-Title": "WeatherMind",
            },
            json={
                "model": AI_MODEL,
                "messages": messages,
                "max_tokens": 600,
                "temperature": 0.7,
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    except requests.RequestException as e:
        return f"❌ Lỗi AI: {str(e)}"
    except (KeyError, IndexError) as e:
        return f"❌ Lỗi phân tích phản hồi AI: {str(e)}"


def stream_chat_with_ai(user_message: str, history: list, weather_context: str = ""):
    """Generator — stream từng token AI về UI."""
    if not OPENROUTER_API_KEY:
        yield "⚠️ Chưa cấu hình OPENROUTER_API_KEY"
        return

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if weather_context:
        messages.append({"role": "system", "content": f"Thời tiết hiện tại:\n{weather_context}"})
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": user_message})

    try:
        resp = requests.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:7860",
                "X-Title": "WeatherMind",
            },
            json={"model": AI_MODEL, "messages": messages, "max_tokens": 600, "stream": True},
            stream=True,
            timeout=30
        )
        resp.raise_for_status()

        full_text = ""
        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if line == "data: [DONE]":
                break
            if line.startswith("data: "):
                try:
                    chunk = json.loads(line[6:])
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    full_text += delta
                    yield full_text
                except (json.JSONDecodeError, KeyError):
                    continue

    except requests.RequestException as e:
        yield f"❌ Lỗi kết nối: {str(e)}"
```

---

## utils/formatters.py

```python
def format_weather_context(weather_data: dict) -> str:
    """Chuyển weather dict → chuỗi text cho AI context."""
    if "error" in weather_data:
        return ""

    loc = weather_data["location"]
    curr = weather_data["current"]

    lines = [
        f"Thành phố: {loc['name']}, {loc['country']}",
        f"Nhiệt độ: {curr['temperature']}°C (cảm giác {curr['feels_like']}°C)",
        f"Thời tiết: {curr['icon']} {curr['description']}",
        f"Độ ẩm: {curr['humidity']}%",
        f"Gió: {curr['wind_speed']} km/h",
    ]

    daily = weather_data.get("daily", [])
    if daily:
        lines.append("\nDự báo 3 ngày tới:")
        for d in daily[:3]:
            lines.append(f"  {d['date']}: {d['icon']} {d['temp_min']}–{d['temp_max']}°C")

    return "\n".join(lines)


def format_weather_html(weather_data: dict) -> str:
    """Render weather card dạng HTML đẹp cho Gradio gr.HTML."""
    if "error" in weather_data:
        return f'<div style="color:red;padding:20px">❌ {weather_data["error"]}</div>'

    loc = weather_data["location"]
    curr = weather_data["current"]

    return f"""
    <div style="
        background: linear-gradient(135deg, #1e3a5f, #2980b9);
        border-radius: 16px; padding: 28px; color: white;
        font-family: sans-serif; max-width: 500px; margin: 0 auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    ">
        <h2 style="margin:0 0 4px">{loc['name']}, {loc['country']}</h2>
        <p style="margin:0 0 20px;opacity:0.8">{loc.get('timezone','')}</p>

        <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
            <span style="font-size:72px">{curr['icon']}</span>
            <div>
                <div style="font-size:56px;font-weight:bold;line-height:1">{curr['temperature']}°C</div>
                <div style="opacity:0.9">{curr['description']}</div>
                <div style="opacity:0.7;font-size:14px">Cảm giác như {curr['feels_like']}°C</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
            <div style="background:rgba(255,255,255,0.15);border-radius:10px;padding:12px">
                <div style="opacity:0.7;font-size:13px">💧 Độ ẩm</div>
                <div style="font-size:24px;font-weight:bold">{curr['humidity']}%</div>
            </div>
            <div style="background:rgba(255,255,255,0.15);border-radius:10px;padding:12px">
                <div style="opacity:0.7;font-size:13px">💨 Gió</div>
                <div style="font-size:24px;font-weight:bold">{curr['wind_speed']} km/h</div>
            </div>
        </div>
    </div>
    """
```

## Bước tiếp theo

→ Đọc `05_gradio_ui.md`
