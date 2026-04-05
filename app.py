"""
app.py — WeatherMind Pro · Main entry point
Dark navy theme — consistent with premium sidebar design
"""

import gradio as gr
from ui.sidebar import create_sidebar_ui
from ui.chart_tab import create_chart_tab
from ui.chat_tab import create_chat_tab
from config import GRADIO_PORT, GRADIO_SHARE

# ══════════════════════════════════════════════════════════════════
#  GLOBAL CSS  (injected once at top-level)
# ══════════════════════════════════════════════════════════════════
APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base reset ─────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

/* ── Full-app light background ───────────────────────────────── */
body,
.gradio-container,
.gradio-container > .main,
.gradio-container .wrap,
footer { 
    background: #F8FAFC !important;
    color: #1E293B !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}

/* Remove Gradio footer */
footer { display: none !important; }

/* ── App header ─────────────────────────────────────────────── */
.wm-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 22px 4px 18px !important;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 24px;
}
.wm-header-title {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #1E293B !important;
    letter-spacing: -0.5px !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
}
.wm-header-sub {
    font-size: 12px !important;
    color: #64748B !important;
    margin: 0 !important;
    padding: 0 !important;
    font-weight: 400 !important;
    letter-spacing: 0.03em !important;
}
.wm-header-dot {
    width: 8px; height: 8px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(16,185,129,0.5);
    flex-shrink: 0;
    margin-left: 4px;
    animation: pulse-dot 2.5s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.55; transform: scale(0.8); }
}

/* ── Left sidebar column ────────────────────────────────────── */
.wm-sidebar-col {
    border-right: 1px solid #E2E8F0 !important;
    padding-right: 28px !important;
}

/* ── Right content column ───────────────────────────────────── */
.wm-content-col {
    padding-left: 28px !important;
}

/* ── Tabs ───────────────────────────────────────────────────── */
.gradio-tabs .tab-nav {
    background: transparent !important;
    border-bottom: 1px solid #E2E8F0 !important;
    gap: 8px !important;
    padding: 0 !important;
    margin-bottom: 32px !important;
}
.gradio-tabs .tab-nav button {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 12px 20px !important;
    transition: color 0.18s, border-color 0.18s !important;
    letter-spacing: 0.02em !important;
}
.gradio-tabs .tab-nav button:hover {
    color: #334155 !important;
}
.gradio-tabs .tab-nav button.selected {
    color: #1E6FC3 !important;
    border-bottom-color: #1E6FC3 !important;
    background: transparent !important;
}

/* ── All Gradio block/group backgrounds → default transparent ──────── */
.gradio-container .block,
.gradio-container .gr-group,
.gradio-container .gr-box,
.gradio-container fieldset {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── Remove number input spinners globally ───────────────────────── */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button,
.gr-number-input button,
button[aria-label="increment"],
button[aria-label="decrement"],
[class*="spin"],
[class*="stepper"] {
    display: none !important;
    -webkit-appearance: none !important;
}
input[type=number] {
    -moz-appearance: textfield !important;
}

/* ── Fullscreen Loading Overlay (Fixed Stacking) ──────────────────── */
/* Khi có ít nhất 1 component đang load, tạo ĐÚNG 1 lớp phủ mờ duy nhất */
.gradio-container:has([data-testid="status-tracker"]:not(.hide))::before {
    content: '' !important;
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    width: 100vw !important; height: 100vh !important;
    background: rgba(248, 250, 252, 0.4) !important;
    backdrop-filter: blur(3px) !important;
    -webkit-backdrop-filter: blur(3px) !important;
    z-index: 99998 !important;
    pointer-events: auto !important; /* Chặn click */
    display: block !important;
}

/* Gắn ĐÚNG 1 Spinner ở tâm màn hình */
.gradio-container:has([data-testid="status-tracker"]:not(.hide))::after {
    content: '' !important;
    position: fixed !important;
    top: 50% !important; left: 50% !important;
    width: 48px !important; height: 48px !important;
    margin: -24px 0 0 -24px !important;
    border: 4px solid rgba(30, 111, 195, 0.15) !important;
    border-top-color: #1E6FC3 !important;
    border-radius: 50% !important;
    z-index: 99999 !important;
    animation: spinner-spin 0.8s linear infinite !important;
    display: block !important;
    transform-origin: center center !important;
}

@keyframes spinner-spin {
    from { transform: translateZ(0) rotate(0deg); }
    to   { transform: translateZ(0) rotate(360deg); }
}

/* Ẩn TOÀN BỘ wrapper loader sinh ra cho từng component của Gradio */
.gradio-container [data-testid="status-tracker"] {
    display: none !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* ── Scrollbars ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
</style>
"""

HEADER_HTML = """
<div class="wm-header">
    <div>
        <p class="wm-header-title">🌤️ WeatherMind</p>
        <p class="wm-header-sub">Real-time weather · AI-powered insights</p>
    </div>
    <div class="wm-header-dot" title="Live data"></div>
</div>
"""


def build_app():
    theme = gr.themes.Base(
        font=gr.themes.GoogleFont("Inter"),
        primary_hue=gr.themes.Color(c50="#eff6ff", c100="#dbeafe", c200="#bfdbfe", c300="#93c5fd", c400="#60a5fa", c500="#1E6FC3", c600="#1a5bb4", c700="#1d4ed8", c800="#1e40af", c900="#1e3a8a", c950="#172554", name="primary"),
        neutral_hue=gr.themes.colors.slate,
    ).set(
        body_background_fill="#F8FAFC",
        body_text_color="#1E293B",
        button_primary_background_fill="#1E6FC3",
        button_primary_background_fill_hover="#1a5bb4",
        button_primary_text_color="#ffffff",
        button_secondary_background_fill="#FFFFFF",
        button_secondary_background_fill_hover="#F1F5F9",
        button_secondary_text_color="#1E293B",
        button_secondary_border_color="#E2E8F0",
        input_background_fill="#FFFFFF",
        input_border_color="#E2E8F0",
        input_placeholder_color="#94A3B8",
        block_background_fill="#FFFFFF",
        block_border_color="#E2E8F0",
        block_radius="12px",
        button_large_radius="8px",
        button_small_radius="8px",
        input_radius="8px",
    )

    with gr.Blocks(title="WeatherMind Pro") as app:
        gr.HTML(APP_CSS + HEADER_HTML)

        with gr.Row(equal_height=False):
            # ── LEFT: Sidebar ──────────────────────────────────
            with gr.Column(scale=1, min_width=300, elem_classes="wm-sidebar-col"):
                weather_state = create_sidebar_ui()

            # ── RIGHT: Tabs ────────────────────────────────────
            with gr.Column(scale=2, elem_classes="wm-content-col"):
                with gr.Tabs():
                    with gr.Tab("📊 Analytics & Trends"):
                        create_chart_tab(weather_state)
                    with gr.Tab("🤖 AI Prediction"):
                        create_chat_tab(weather_state)

    return app, theme


if __name__ == "__main__":
    app, theme = build_app()
    app.queue()
    app.launch(
        server_name="0.0.0.0",
        server_port=GRADIO_PORT,
        share=GRADIO_SHARE,
        show_error=True,
        theme=theme,
    )