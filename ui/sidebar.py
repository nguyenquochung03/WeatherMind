"""
ui/sidebar.py — Premium weather app sidebar
Full redesign: glassmorphism card, animated sky orbs, cinematic gradients
"""

import gradio as gr
from services.weather_service import get_weather

QUICK_CITIES = [
    ("🇻🇳", "Hà Nội"),
    ("🇻🇳", "Hồ Chí Minh"),
    ("🇻🇳", "Đà Nẵng"),
    ("🇯🇵", "Tokyo"),
    ("🇬🇧", "London"),
    ("🇺🇸", "New York"),
    ("🇦🇺", "Sydney"),
    ("🇸🇬", "Singapore"),
]

# ══════════════════════════════════════════════════════════════════
#  FULL SIDEBAR CSS
# ══════════════════════════════════════════════════════════════════
SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ═══════════════════════════════════════════════════════════════
   GLOBAL — ẩn spin buttons trên mọi input number trong sidebar
═══════════════════════════════════════════════════════════════ */
.wx-sidebar input[type=number]::-webkit-inner-spin-button,
.wx-sidebar input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none !important;
    appearance: none !important;
    margin: 0 !important;
}
.wx-sidebar input[type=number],
input[type=number] {
    -moz-appearance: textfield !important;
}
/* Ẩn spin buttons Gradio tự thêm vào */
.wx-sidebar .gr-number-input button,
.wx-sidebar button[aria-label="increment"],
.wx-sidebar button[aria-label="decrement"],
.wx-sidebar [class*="spin"],
.wx-sidebar [class*="stepper"] {
    display: none !important;
}

/* ── Root / reset ─────────────────────────────────────────── */
.wx-sidebar * { box-sizing: border-box; }
.wx-sidebar {
    font-family: 'Inter', system-ui, sans-serif !important;
    padding: 0 !important;
}

/* ═══════════════════════════════════════════════════════════════
   SEARCH SECTION
═══════════════════════════════════════════════════════════════ */
.wx-search-wrap {
    padding: 6px 0 24px !important;
}

/* ── Tiêu đề section ────────────────────────────────────────── */
.wx-search-label {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #64748B !important;
    margin: 0 0 16px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
.wx-search-label::before {
    content: '';
    display: inline-block;
    width: 4px; height: 14px;
    background: #1E6FC3;
    border-radius: 99px;
    flex-shrink: 0;
}

/* ── Search input ───────────────────────────────────────────── */
.wx-search-wrap .gr-textbox {
    border-radius: 8px !important;
    overflow: hidden !important;
}
.wx-search-wrap .gr-textbox textarea,
.wx-search-wrap .gr-textbox input {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 15px !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
}
.wx-search-wrap .gr-textbox textarea:focus,
.wx-search-wrap .gr-textbox input:focus {
    background: #FFFFFF !important;
    border-color: #1E6FC3 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(30,111,195,0.14) !important;
}
.wx-search-wrap .gr-textbox textarea::placeholder,
.wx-search-wrap .gr-textbox input::placeholder {
    color: #94A3B8 !important;
}

/* ── Search button ─────────────────────────────────────────── */
.wx-search-btn button {
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
}
.wx-search-btn button:hover {
    background: #1a5bb4 !important;
    transform: translateY(-1px) !important;
}
.wx-search-btn button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* ── Popular label ─────────────────────────────────────────── */
.wx-cities-label {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    color: #94A3B8 !important;
    margin: 20px 0 12px !important;
    padding: 0 !important;
}

/* ── City chip buttons ─────────────────────────────────────── */
.wx-city-chip button {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #475569 !important;
    padding: 8px 16px !important;
    transition: all 0.15s ease !important;
    white-space: nowrap !important;
}
.wx-city-chip button:hover {
    background: #E2E8F0 !important;
    border-color: #CBD5E1 !important;
    color: #1E293B !important;
}

/* ── Section divider ───────────────────────────────────────── */
.wx-divider {
    height: 1px !important;
    background: #F1F5F9 !important;
    margin: 24px 0 !important;
    border: none !important;
}

/* ═══════════════════════════════════════════════════════════════
   WEATHER CARD SECTION
═══════════════════════════════════════════════════════════════ */

/* ── Section heading ───────────────────────────────────────── */
.wx-card-heading {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #64748B !important;
    margin: 0 0 16px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
.wx-card-heading::before {
    content: '';
    display: inline-block;
    width: 4px; height: 14px;
    background: #1E6FC3;
    border-radius: 99px;
    flex-shrink: 0;
}

/* ── Error box ─────────────────────────────────────────────── */
.wx-error {
    background: #FEF2F2 !important;
    border: 1px solid #FECACA !important;
    border-radius: 12px !important;
    padding: 16px !important;
    animation: wx-fadein 0.3s ease;
}
.wx-error p {
    font-size: 14px !important;
    color: #EF4444 !important;
    margin: 0 !important;
    font-weight: 500 !important;
}

/* ── Weather card wrapper ──────────────────────────────────── */
.wx-card {
    border-radius: 12px !important;
    overflow: hidden !important;
    position: relative !important;
    animation: wx-fadein 0.3s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
}

.wx-card-bg {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    padding: 24px !important;
}

.wx-card-inner {
    position: relative;
    z-index: 1;
}

/* ── Location ──────────────────────────────────────────────── */
.wx-location p,
.wx-location h2, .wx-location h1 {
    font-family: 'Inter', system-ui, sans-serif !important;
    margin: 0 0 12px 0 !important;
    padding: 0 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #64748B !important;
}

/* ── Hero: icon + temp ─────────────────────────────────────── */
.wx-hero-row {
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
    padding: 12px 0 !important;
}
.wx-icon-col {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.wx-icon-col .gr-textbox,
.wx-icon-col .block {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.wx-icon-col textarea,
.wx-icon-col input {
    font-size: 72px !important;
    line-height: 1 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    text-align: center !important;
    width: 80px !important;
    resize: none !important;
    color: #1E6FC3 !important; /* Primary color */
    filter: none !important;
    /* ẩn spin buttons bên trong icon textbox */
    -webkit-appearance: none !important;
    -moz-appearance: none !important;
}
.wx-icon-col input[type=number]::-webkit-inner-spin-button,
.wx-icon-col input[type=number]::-webkit-outer-spin-button {
    display: none !important;
    -webkit-appearance: none !important;
}

/* ── Nhiệt độ ──────────────────────────────────────────────── */
.wx-temp p,
.wx-temp h1,
.wx-temp h2 {
    font-family: 'Inter', system-ui, sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
    font-size: 64px !important;
    font-weight: 800 !important;
    color: #1E293B !important;
    line-height: 1 !important;
    letter-spacing: -2px !important;
    text-shadow: none !important;
}

/* ── Description pill ──────────────────────────────────────── */
.wx-desc p {
    font-family: 'Inter', system-ui, sans-serif !important;
    display: inline-block !important;
    background: #F1F5F9 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 16px 0 0 0 !important;
    font-size: 14px !important;
    color: #334155 !important;
    font-weight: 600 !important;
    text-transform: capitalize !important;
}

/* ── Solid divider ─────────────────────────────────────────── */
.wx-glass-divider {
    height: 1px;
    margin: 24px 0;
    background: #F1F5F9;
}

/* ── Stats row ─────────────────────────────────────────────── */
.wx-stats-row {
    display: flex !important;
    justify-content: space-between !important;
    padding: 0 !important;
}
.wx-stat {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 8px !important;
    flex: 1 !important;
}
.wx-stat-sep {
    width: 1px;
    background: #E2E8F0;
    align-self: stretch;
    margin: 0 16px;
}
.wx-stat-icon p {
    margin: 0 !important; padding: 0 !important;
    font-size: 24px !important; line-height: 1 !important;
}
.wx-stat-val p {
    font-family: 'Inter', system-ui, sans-serif !important;
    margin: 0 !important; padding: 0 !important;
    font-size: 16px !important; font-weight: 700 !important;
    color: #1E293B !important;
}
.wx-stat-lbl p {
    font-family: 'Inter', system-ui, sans-serif !important;
    margin: 0 !important; padding: 0 !important;
    font-size: 12px !important;
    color: #64748B !important;
    font-weight: 500 !important;
}

/* ── Animations ────────────────────────────────────────────── */
@keyframes wx-fadein {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
"""


def create_sidebar_ui():
    """Create premium weather app sidebar with full redesign."""

    gr.HTML(SIDEBAR_CSS)
    weather_state = gr.State({})

    # ══════════════════════════════════════════════════════════════
    #  SEARCH SECTION
    # ══════════════════════════════════════════════════════════════
    with gr.Column(elem_classes="wx-sidebar wx-search-wrap"):
        gr.Markdown("🔍  City Search", elem_classes="wx-search-label")

        with gr.Row(equal_height=True):
            city_input = gr.Textbox(
                placeholder="Search city, e.g. Tokyo, Hanoi…",
                show_label=False,
                scale=4,
                elem_id="city-search-input"
            )
            search_btn = gr.Button(
                "Search",
                variant="primary",
                scale=1,
                elem_classes="wx-search-btn",
            )

        gr.Markdown("Popular", elem_classes="wx-cities-label")

        with gr.Row():
            for flag, city in QUICK_CITIES[:4]:
                btn = gr.Button(f"{flag} {city}", size="sm", elem_classes="wx-city-chip")
                btn.click(fn=lambda c=city: c, outputs=city_input, show_progress="full")

        with gr.Row():
            for flag, city in QUICK_CITIES[4:]:
                btn = gr.Button(f"{flag} {city}", size="sm", elem_classes="wx-city-chip")
                btn.click(fn=lambda c=city: c, outputs=city_input, show_progress="full")

    # Divider
    gr.HTML('<div class="wx-divider"></div>')

    # ══════════════════════════════════════════════════════════════
    #  WEATHER DISPLAY SECTION
    # ══════════════════════════════════════════════════════════════
    with gr.Column(elem_classes="wx-sidebar"):
        gr.Markdown("Current Weather", elem_classes="wx-card-heading")

        # ── Error container ──────────────────────────────────────
        with gr.Column(visible=False, elem_classes="wx-error") as error_container:
            error_msg = gr.Markdown()

        # ── Weather card ─────────────────────────────────────────
        with gr.Column(visible=False, elem_classes="wx-card") as weather_card:
            with gr.Column(elem_classes="wx-card-bg"):
                with gr.Column(elem_classes="wx-card-inner"):

                    # Location
                    location_text = gr.Markdown(elem_classes="wx-location")

                    # Hero row: big icon + big temp
                    with gr.Row(elem_classes="wx-hero-row"):
                        with gr.Column(scale=1, min_width=84, elem_classes="wx-icon-col"):
                            weather_icon = gr.Textbox(
                                show_label=False,
                                container=False,
                            )
                        with gr.Column(scale=3, elem_classes="wx-temp"):
                            temp_display = gr.Markdown()

                    # Description pill
                    description_text = gr.Markdown(elem_classes="wx-desc")

                    # Glass divider
                    gr.HTML('<div class="wx-glass-divider"></div>')

                    # Stats row
                    with gr.Row(elem_classes="wx-stats-row"):

                        with gr.Column(min_width=56, elem_classes="wx-stat"):
                            gr.Markdown("💧", elem_classes="wx-stat-icon")
                            humidity_text = gr.Markdown(elem_classes="wx-stat-val")
                            gr.Markdown("Humidity", elem_classes="wx-stat-lbl")

                        gr.HTML('<div class="wx-stat-sep"></div>')

                        with gr.Column(min_width=56, elem_classes="wx-stat"):
                            gr.Markdown("💨", elem_classes="wx-stat-icon")
                            wind_text = gr.Markdown(elem_classes="wx-stat-val")
                            gr.Markdown("Wind", elem_classes="wx-stat-lbl")

                        gr.HTML('<div class="wx-stat-sep"></div>')

                        with gr.Column(min_width=56, elem_classes="wx-stat"):
                            gr.Markdown("🌡️", elem_classes="wx-stat-icon")
                            feels_like_text = gr.Markdown(elem_classes="wx-stat-val")
                            gr.Markdown("Feels Like", elem_classes="wx-stat-lbl")

    # ══════════════════════════════════════════════════════════════
    #  LOGIC
    # ══════════════════════════════════════════════════════════════
    def search_weather(city: str):
        city = city.strip()

        if not city:
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                "⚠️ Please enter a city name.",
                "", "", "", "", "", "", {}
            )

        data = get_weather(city)

        if "error" in data:
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                f"❌ {data['error']}",
                "", "", "", "", "", "", {}
            )

        loc  = data["location"]
        curr = data["current"]

        return (
            gr.update(visible=False),
            gr.update(visible=True),
            "",
            f"📍 {loc['name']}, {loc['country']}",
            curr["icon"],
            f"# {curr['temperature']}°",
            curr["description"].capitalize(),
            f"{curr['humidity']}%",
            f"{curr['wind_speed']} km/h",
            f"{curr['feels_like']}°C",
            data,
        )

    # ══════════════════════════════════════════════════════════════
    #  EVENT BINDINGS
    # ══════════════════════════════════════════════════════════════
    outputs = [
        error_container,
        weather_card,
        error_msg,
        location_text,
        weather_icon,
        temp_display,
        description_text,
        humidity_text,
        wind_text,
        feels_like_text,
        weather_state,
    ]

    search_btn.click(
        fn=search_weather,
        inputs=[city_input],
        outputs=outputs,
        show_progress="full"
    )
    city_input.submit(
        fn=search_weather,
        inputs=[city_input],
        outputs=outputs,
        show_progress="full"
    )

    return weather_state