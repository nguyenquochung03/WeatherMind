# 02 — Cài đặt môi trường

## requirements.txt

```txt
gradio>=4.44.0
requests>=2.31.0
python-dotenv>=1.0.0
plotly>=5.18.0
pandas>=2.1.0
```

## Cài đặt

```bash
cd weathermind
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## File .env.example

```env
# OpenRouter API Key (đăng ký miễn phí tại https://openrouter.ai)
OPENROUTER_API_KEY=your_key_here

# Model AI sử dụng (miễn phí)
AI_MODEL=mistralai/mistral-7b-instruct:free

# Gradio settings
GRADIO_SERVER_PORT=7860
GRADIO_SHARE=false
```

## File config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = os.getenv("AI_MODEL", "mistralai/mistral-7b-instruct:free")

# Open-Meteo (không cần key)
WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Gradio
GRADIO_PORT = int(os.getenv("GRADIO_SERVER_PORT", 7860))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# Timeout cho API calls
REQUEST_TIMEOUT = 10  # seconds
```

## Lấy OpenRouter API Key

1. Vào https://openrouter.ai
2. Đăng ký tài khoản (GitHub/Google)
3. Vào Settings → Keys → Create Key
4. Copy key vào file `.env`
5. Model `mistralai/mistral-7b-instruct:free` — hoàn toàn miễn phí

## Kiểm tra cài đặt

```bash
python -c "import gradio; print('Gradio OK:', gradio.__version__)"
python -c "import requests; print('Requests OK')"
python -c "from config import WEATHER_BASE_URL; print('Config OK')"
```

## Bước tiếp theo

→ Đọc `03_api_integration.md`
