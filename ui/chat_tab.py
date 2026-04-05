"""
ui/chat_tab.py — AI Prediction panel
Dark navy theme · Outfit + DM Sans · streaming chat
"""

import gradio as gr
from services.ai_service import stream_chat_with_ai
from utils.formatters import format_weather_context

# ══════════════════════════════════════════════════════════════════
#  CHAT TAB CSS
# ══════════════════════════════════════════════════════════════════
CHAT_CSS = """
<style>
/* ── Section heading (same accent-bar style) ────────────────── */
.wx-chat-heading {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #64748B !important;
    margin: 0 0 4px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
.wx-chat-heading::before {
    content: '';
    display: inline-block;
    width: 4px; height: 14px;
    background: #1E6FC3;
    border-radius: 99px;
    flex-shrink: 0;
}

.wx-chat-intro {
    font-size: 13px !important;
    color: #64748B !important;
    margin: 0 0 20px !important;
    padding: 0 !important;
    line-height: 1.6 !important;
}
.wx-chat-intro strong {
    color: #1E293B !important;
    font-weight: 600 !important;
}

/* ── Chatbot bubbles ────────────────────────────────────────── */
.wx-chatbot .message-wrap {
    background: transparent !important;
}
/* User bubble */
.wx-chatbot .message.user {
    background: #1E6FC3 !important;
    border: 1px solid #1E6FC3 !important;
    border-radius: 16px 16px 4px 16px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
/* Ensure inner text elements inherit the white color */
.wx-chatbot .message.user p,
.wx-chatbot .message.user span,
.wx-chatbot .message.user li,
.wx-chatbot .message.user a {
    color: #FFFFFF !important;
}
/* Bot bubble */
.wx-chatbot .message.bot {
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px 16px 16px 4px !important;
    color: #1E293B !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
/* Chatbot container */
.wx-chatbot > div {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}

/* ── Message input ──────────────────────────────────────────── */
/* Remove background/borders from Gradio inner wrappers */
.wx-msg-input,
.wx-msg-input > label,
.wx-msg-input .input-container {
    background: #FFFFFF !important;
    border: none !important;
    box-shadow: none !important;
}

/* Apply border and radius strictly to the `.block` outermost wrapper */
.wx-msg-input.block {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    padding: 0 !important;
}

/* Focus effect on the entire wrapper */
.wx-msg-input.block:focus-within {
    border-color: #1E6FC3 !important;
    box-shadow: 0 0 0 3px rgba(30,111,195,0.14) !important;
}

/* Style the actual inputs transparent */
.wx-msg-input textarea,
.wx-msg-input input {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 15px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #1E293B !important;
    padding: 14px 16px !important;
    caret-color: #1E6FC3 !important;
    resize: none !important;
    outline: none !important;
}

.wx-msg-input textarea:focus,
.wx-msg-input input:focus {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

.wx-msg-input textarea::placeholder,
.wx-msg-input input::placeholder {
    color: #94A3B8 !important;
}

.wx-msg-input textarea:disabled,
.wx-msg-input input:disabled {
    cursor: not-allowed !important;
    opacity: 0.6 !important;
}

/* ── Send button ────────────────────────────────────────────── */
.wx-send-btn button {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: #1E6FC3 !important;
    border: none !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
    padding: 12px 20px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    width: 100% !important;
    white-space: nowrap !important;
}
.wx-send-btn button:hover {
    background: #1a5bb4 !important;
    transform: translateY(-1px) !important;
}
.wx-send-btn button:active {
    transform: scale(0.98) !important;
}
.wx-send-btn button:disabled {
    background: #CBD5E1 !important;
    cursor: not-allowed !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Clear button ───────────────────────────────────────────── */
.wx-clear-btn button {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #64748B !important;
    padding: 12px 14px !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
.wx-clear-btn button:hover {
    background: #FEF2F2 !important;
    border-color: #FECACA !important;
    color: #EF4444 !important;
}

/* ── Suggestions heading ────────────────────────────────────── */
.wx-suggest-label {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
    margin: 20px 0 12px !important;
    padding: 0 !important;
}

/* ── Suggestion chips ───────────────────────────────────────── */
.wx-suggest-chip button {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #475569 !important;
    padding: 8px 16px !important;
    white-space: nowrap !important;
    line-height: 1.4 !important;
    transition: all 0.15s ease !important;
}
.wx-suggest-chip button:hover {
    background: #E2E8F0 !important;
    border-color: #CBD5E1 !important;
    color: #1E293B !important;
}
.wx-suggest-chip button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
"""

SUGGESTIONS = [
    "Hôm nay có nên mang ô không?",
    "Nên mặc gì cho phù hợp?",
    "Có thể chạy bộ ngoài trời không?",
    "Gợi ý hoạt động cuối tuần?",
    "Dự báo tuần tới thế nào?",
]


def create_chat_tab(weather_state: gr.State):
    """Renders the AI chat panel."""
    gr.HTML(CHAT_CSS)

    # ── Header ────────────────────────────────────────────────────
    gr.Markdown("WeatherMind AI", elem_classes="wx-chat-heading")
    gr.Markdown(
        "Tra cứu thành phố ở **sidebar bên trái** trước, "
        "rồi hỏi tôi bất kỳ điều gì về thời tiết nhé. 🌤️",
        elem_classes="wx-chat-intro",
    )

    # ── Chatbot ───────────────────────────────────────────────────
    chatbot = gr.Chatbot(
        value=[],
        label="",
        show_label=False,
        height=440,
        elem_classes="wx-chatbot",
        avatar_images=(
            None,
            "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=weathermind&backgroundColor=1e3a5f",
        ),
    )

    # ── Input row ─────────────────────────────────────────────────
    with gr.Row(equal_height=True):
        msg_input = gr.Textbox(
            placeholder="Hỏi về thời tiết… (Enter để gửi)",
            label="",
            scale=6,
            max_lines=3,
            show_label=False,
            elem_classes="wx-msg-input",
        )
        with gr.Column(scale=0, min_width=90):
            send_btn  = gr.Button("Gửi →", elem_classes="wx-send-btn")
            clear_btn = gr.Button("Xóa",   elem_classes="wx-clear-btn")

    # ── Suggestions ───────────────────────────────────────────────
    gr.Markdown("Câu hỏi gợi ý", elem_classes="wx-suggest-label")

    # Two rows of chips (wrap-friendly)
    with gr.Row():
        for s in SUGGESTIONS[:3]:
            chip = gr.Button(s, size="sm", elem_classes="wx-suggest-chip")
            chip.click(fn=lambda x=s: x, outputs=msg_input)
    with gr.Row():
        for s in SUGGESTIONS[3:]:
            chip = gr.Button(s, size="sm", elem_classes="wx-suggest-chip")
            chip.click(fn=lambda x=s: x, outputs=msg_input)

    # ── Logic ─────────────────────────────────────────────────────
    def respond(message, history, weather_data):
        if not message.strip():
            yield gr.update(), history
            return
        
        # Convert history to new format if needed
        formatted_history = []
        for msg in history:
            if isinstance(msg, dict):
                formatted_history.append((msg.get("content", ""), ""))
            elif isinstance(msg, (list, tuple)) and len(msg) == 2:
                formatted_history.append((msg[0], msg[1] if len(msg) > 1 else ""))
        
        weather_ctx = format_weather_context(weather_data) if weather_data else ""
        
        # Add user message
        history = history + [{"role": "user", "content": message}]
        
        # Add placeholder for assistant
        history.append({"role": "assistant", "content": ""})
        
        # Vô hiệu hóa input ngay khi bắt đầu xử lý
        yield gr.update(value="", interactive=False), history
        
        for partial in stream_chat_with_ai(message, formatted_history, weather_ctx):
            history[-1]["content"] = partial
            yield gr.update(value="", interactive=False), history
            
        # Kích hoạt lại input sau khi xử lý xong
        yield gr.update(interactive=True), history

    send_btn.click(respond,  [msg_input, chatbot, weather_state], [msg_input, chatbot])
    msg_input.submit(respond,[msg_input, chatbot, weather_state], [msg_input, chatbot])
    clear_btn.click(fn=lambda: ([], ""), outputs=[chatbot, msg_input])