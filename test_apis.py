import requests

def test_weather():
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": "Ho Chi Minh City", "count": 1}
    ).json()
    loc = geo["results"][0]
    print(f"✅ Geocoding: {loc['name']}, {loc['latitude']}, {loc['longitude']}")

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
    if not OPENROUTER_API_KEY:
        print("⚠️ OPENROUTER_API_KEY not set, skipping AI test")
        return
    
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
    if 'choices' in r:
        print(f"✅ AI: {r['choices'][0]['message']['content']}")
    else:
        print(f"⚠️ AI Error: {r}")

if __name__ == "__main__":
    test_weather()
    test_ai()
