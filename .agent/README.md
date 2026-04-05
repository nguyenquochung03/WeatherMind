# 🤖 AI Agent — Weather AI Assistant với Gradio

## Tổng quan dự án

Xây dựng ứng dụng **WeatherMind** — một Weather Dashboard thông minh kết hợp:
- 🌤️ **Open-Meteo API** — Dữ liệu thời tiết real-time, hoàn toàn miễn phí, không cần API key
- 🧠 **OpenRouter API** — AI chat (dùng model miễn phí như `mistralai/mistral-7b-instruct`)
- 🎨 **Gradio** — Framework UI Python hiện đại

## Mục tiêu học tập

Sau khi hoàn thành, bạn sẽ biết:
- Tổ chức project Gradio theo kiến trúc BE/FE rõ ràng
- Gọi REST API bên ngoài từ Python (requests / httpx)
- Sử dụng `gr.Blocks()` để tạo layout phức tạp
- Xây dựng multi-tab UI với Gradio
- Streaming AI response trong Gradio
- Xử lý state, loading state, error handling

## Danh sách file hướng dẫn

| File | Mô tả |
|------|-------|
| `01_project_structure.md` | Cấu trúc thư mục & kiến trúc tổng thể |
| `02_environment_setup.md` | Cài đặt môi trường, dependencies |
| `03_api_integration.md` | Tích hợp Open-Meteo & OpenRouter API |
| `04_backend_services.md` | Viết các service layer (business logic) |
| `05_gradio_ui.md` | Xây dựng toàn bộ UI với Gradio Blocks |
| `06_advanced_features.md` | Tính năng nâng cao: streaming, state, theming |
| `07_testing_checklist.md` | Kiểm tra hoàn chỉnh trước khi demo |

## Thứ tự thực hiện

01 → 02 → 03 → 04 → 05 → 06 → 07

## APIs sử dụng

### 1. Open-Meteo (Thời tiết) — MIỄN PHÍ, KHÔNG CẦN KEY
- Base URL: `https://api.open-meteo.com/v1/forecast`
- Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
- Docs: https://open-meteo.com/en/docs

### 2. OpenRouter (AI) — CẦN FREE API KEY
- Base URL: `https://openrouters.ai/api/v1/chat/completions`
- Đăng ký miễn phí tại: https://openrouter.ai
- Model miễn phí: `mistralai/mistral-7b-instruct:free`

## Kết quả cuối cùng

Ứng dụng có 3 tab:
1. **Thời tiết** — Nhập tên thành phố → hiện weather card đẹp
2. **Biểu đồ** — Đồ thị nhiệt độ 7 ngày tới
3. **AI Chat** — Chat với AI về thời tiết
