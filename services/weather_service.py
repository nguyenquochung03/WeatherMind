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
