# 03 — Tích hợp API

## Open-Meteo API — Thời tiết

### Endpoint 1: Geocoding (tên thành phố → tọa độ)

```
GET https://geocoding-api.open-meteo.com/v1/search
    ?name=Hanoi
    &count=1
    &language=en
    &format=json
```

Response mẫu:
```json
{
  "results": [{
    "id": 1581130,
    "name": "Hanoi",
    "latitude": 21.0245,
    "longitude": 105.8412,
    "country": "Vietnam",
    "country_code": "VN",
    "timezone": "Asia/Bangkok"
  }]
}
```

### Endpoint 2: Forecast (tọa độ → thời tiết)

```
GET https://api.open-meteo.com/v1/forecast
    ?latitude=21.0245
    &longitude=105.8412
    &current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,apparent_temperature
    &daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code
    &timezone=Asia/Bangkok
    &forecast_days=7
```

### Weather Code → Mô tả tiếng Việt

```python
WEATHER_CODES = {
    0: ("Trời quang", "☀️"),
    1: ("Chủ yếu quang", "🌤️"),
    2: ("Có mây một phần", "⛅"),
    3: ("Nhiều mây", "☁️"),
    45: ("Sương mù", "🌫️"),
    51: ("Mưa phùn nhẹ", "🌦️"),
    61: ("Mưa nhỏ", "🌧️"),
    63: ("Mưa vừa", "🌧️"),
    65: ("Mưa lớn", "⛈️"),
    80: ("Mưa rào", "🌦️"),
    95: ("Dông bão", "⛈️"),
}
```

---

## OpenRouter API — AI Chat

### Request format

```python
import requests

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:7860",  # Required by OpenRouter
    "X-Title": "WeatherMind",
}

payload = {
    "model": "mistralai/mistral-7b-instruct:free",
    "messages": [
        {"role": "system", "content": "You are a helpful weather assistant..."},
        {"role": "user", "content": "Hà Nội hôm nay có mưa không?"}
    ],
    "max_tokens": 500,
    "temperature": 0.7,
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=30
)

data = response.json()
answer = data["choices"][0]["message"]["content"]
```

### Streaming (nâng cao — xem file 06)

```python
payload["stream"] = True
response = requests.post(..., stream=True)

for line in response.iter_lines():
    if line.startswith(b"data: "):
        chunk = json.loads(line[6:])
        delta = chunk["choices"][0]["delta"].get("content", "")
        yield delta
```

---

## Test nhanh API

Tạo file `test_apis.py` tại root để kiểm tra:

```python
# test_apis.py
import requests

def test_weather():
    # 1. Geocoding
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Ho Chi Minh City", "count": 1}
    ).json()
    loc = geo["results"][0]
    print(f"✅ Geocoding: {loc['name']}, {loc['latitude']}, {loc['longitude']}")

    # 2. Forecast
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "current": "temperature_2m,weather_code",
            "timezone": "Asia/Bangkok"
        }
    ).json()
    temp = weather["current"]["temperature_2m"]
    print(f"✅ Forecast: {temp}°C")

def test_ai():
    from config import OPENROUTER_API_KEY, AI_MODEL
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": AI_MODEL,
            "messages": [{"role": "user", "content": "Say hello in Vietnamese"}],
            "max_tokens": 50
        }
    ).json()
    print(f"✅ AI: {r['choices'][0]['message']['content']}")

if __name__ == "__main__":
    test_weather()
    test_ai()
```

```bash
python test_apis.py
```

## Bước tiếp theo

→ Đọc `04_backend_services.md`
