import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = os.getenv("AI_MODEL", "openai/gpt-oss-120b:free")

# Open-Meteo (không cần key)
WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Gradio
GRADIO_PORT = int(os.getenv("GRADIO_SERVER_PORT", 7860))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# Timeout cho API calls
REQUEST_TIMEOUT = 10  # seconds
