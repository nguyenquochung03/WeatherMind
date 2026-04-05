# 01 — Cấu trúc thư mục & Kiến trúc

## Cây thư mục cần tạo

```
weathermind/
├── .agent/                    # Hướng dẫn (đã có)
├── app.py                     # Entry point — chạy app này
├── config.py                  # Cấu hình, env vars
├── requirements.txt           # Dependencies
├── .env                       # API keys (không commit git)
├── .env.example               # Template env
│
├── services/                  # Business logic / API calls
│   ├── __init__.py
│   ├── weather_service.py     # Gọi Open-Meteo API
│   └── ai_service.py         # Gọi OpenRouter API
│
├── ui/                        # Gradio UI components
│   ├── __init__.py
│   ├── weather_tab.py         # Tab thời tiết
│   ├── chart_tab.py           # Tab biểu đồ
│   └── chat_tab.py            # Tab AI chat
│
└── utils/
    ├── __init__.py
    └── formatters.py          # Format dữ liệu, icons
```

## Kiến trúc luồng dữ liệu

```
User nhập thành phố
        │
        ▼
[Gradio UI - ui/weather_tab.py]
        │
        ▼
[services/weather_service.py]
        │  ① Geocoding API → tọa độ lat/lon
        │  ② Forecast API → dữ liệu thời tiết
        ▼
[utils/formatters.py] → Format thành dict đẹp
        │
        ▼
[Gradio UI] → Render HTML card + chart
```

## Nguyên tắc tổ chức

- **services/** — KHÔNG chứa Gradio code. Chỉ là Python thuần, dễ test.
- **ui/** — KHÔNG chứa business logic. Chỉ gọi service và render.
- **app.py** — Chỉ import UI và launch app.
- **config.py** — Dùng `python-dotenv` để load `.env`

## Lệnh tạo cấu trúc

```bash
mkdir -p weathermind/{services,ui,utils}
cd weathermind
touch app.py config.py requirements.txt .env .env.example
touch services/__init__.py services/weather_service.py services/ai_service.py
touch ui/__init__.py ui/weather_tab.py ui/chart_tab.py ui/chat_tab.py
touch utils/__init__.py utils/formatters.py
```

## Bước tiếp theo

→ Đọc `02_environment_setup.md`
