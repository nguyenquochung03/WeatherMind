import requests
import json
import time
from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODEL

SYSTEM_PROMPT = """Bạn là WeatherMind AI, trợ lý thời tiết thông minh.
Bạn trả lời bằng tiếng Việt, ngắn gọn, thân thiện.
Khi được cung cấp dữ liệu thời tiết, hãy phân tích và đưa ra lời khuyên hữu ích.
Gợi ý trang phục, hoạt động phù hợp với thời tiết."""

# OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Cache working models to avoid repeated API calls
_working_models = []
_last_model_check = 0

def get_working_free_models():
    """Lấy danh sách model miễn phí đang hoạt động tốt"""
    global _working_models, _last_model_check
    
    # Cache for 5 minutes
    if time.time() - _last_model_check < 300 and _working_models:
        return _working_models
    
    try:
        response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
        all_models = response.json().get('data', [])
        free_models = [m['id'] for m in all_models if ':free' in m['id']]
        
        # Priority list (lighter models first)
        priority = [
            "qwen/qwen3-coder:free",
            "meta-llama/llama-3.2-3b-instruct:free", 
            "google/gemma-3-4b-it:free",
            "qwen/qwen-2-7b-instruct:free",
            "google/gemma-3-12b-it:free",
            "google/gemma-2-9b-it:free",
            "mistralai/mistral-7b-instruct:free",
            "huggingfaceh4/zephyr-7b-beta:free"
        ]
        
        # Sort by priority
        _working_models = [m for m in priority if m in free_models]
        _working_models += [m for m in free_models if m not in priority]
        _last_model_check = time.time()
        
        return _working_models
        
    except Exception as e:
        print(f"❌ Không thể lấy danh sách model: {e}")
        return []

def try_model(model_id, messages):
    """Thử gọi một model cụ thể"""
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:7860",
                "X-Title": "WeatherMind",
            },
            model=model_id,
            messages=messages,
            max_tokens=600,
            temperature=0.7,
            timeout=20
        )
        return completion.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            print(f"🔴 {model_id}: BUSY (429)")
        elif "403" in error_msg or "401" in error_msg:
            print(f"🔴 {model_id}: FORBIDDEN (403/401)")
        else:
            print(f"🔴 {model_id}: ERROR ({error_msg[:50]})")
        return None

def chat_with_ai(user_message: str, history: list, weather_context: str = "") -> str:
    if not OPENROUTER_API_KEY:
        return "⚠️ Chưa cấu hình OPENROUTER_API_KEY trong file .env"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if weather_context:
        messages.append({"role": "system", "content": f"Dữ liệu thời tiết hiện tại:\n{weather_context}"})
    
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": user_message})

    # Try user-specified model first
    if AI_MODEL and ":free" in AI_MODEL:
        result = try_model(AI_MODEL, messages)
        if result:
            return result
    
    # Fallback to auto-discovery
    working_models = get_working_free_models()
    for model in working_models:
        result = try_model(model, messages)
        if result:
            return result
        time.sleep(0.5)  # Brief pause between attempts
    
    return "❌ Tất cả model miễn phí đang bận. Vui lòng thử lại sau vài phút."

def stream_chat_with_ai(user_message: str, history: list, weather_context: str = ""):
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

    # Try user-specified model first
    if AI_MODEL and ":free" in AI_MODEL:
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:7860",
                    "X-Title": "WeatherMind",
                },
                model=AI_MODEL,
                messages=messages,
                max_tokens=600,
                temperature=0.7,
                stream=True,
                timeout=20
            )
            
            full_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    yield full_text
            return
        except Exception as e:
            print(f"🔴 {AI_MODEL}: {str(e)[:50]}")

    # Fallback to auto-discovery
    working_models = get_working_free_models()
    for model in working_models:
        try:
            print(f"🚀 Thử model: {model}")
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:7860",
                    "X-Title": "WeatherMind",
                },
                model=model,
                messages=messages,
                max_tokens=600,
                temperature=0.7,
                stream=True,
                timeout=20
            )
            
            full_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    yield full_text
            print(f"✅ Thành công với: {model}")
            return
        except Exception as e:
            print(f"🔴 {model}: {str(e)[:50]}")
            time.sleep(0.5)
            continue
    
    yield "❌ Tất cả model miễn phí đang bận. Vui lòng thử lại sau vài phút."
