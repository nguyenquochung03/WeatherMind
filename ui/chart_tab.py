"""
ui/chart_tab.py — Analytics & Trends panel
Dark navy theme · Outfit + DM Sans · Plotly dark chart
"""

import gradio as gr
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════
#  CHART TAB CSS
# ══════════════════════════════════════════════════════════════════
CHART_CSS = """
<style>
/* ── Tab section label ──────────────────────────────────────── */
.wx-chart-heading {
    font-family: 'Outfit', sans-serif !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: rgba(110,135,175,0.9) !important;
    margin: 0 0 4px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 7px !important;
}
.wx-chart-heading::before {
    content: '';
    display: inline-block;
    width: 3px; height: 13px;
    background: linear-gradient(180deg, #3a8ef6, #1a55c4);
    border-radius: 99px;
    flex-shrink: 0;
}

.wx-chart-sub {
    font-size: 12px !important;
    color: rgba(140,165,210,0.55) !important;
    margin: 0 0 20px !important;
    padding: 0 !important;
    font-style: italic !important;
}

/* ── Refresh button ─────────────────────────────────────────── */
.wx-refresh-btn button {
    font-family: 'Outfit', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 10px !important;
    color: rgba(180,205,255,0.75) !important;
    padding: 7px 14px !important;
    transition: background 0.15s, color 0.15s, border-color 0.15s !important;
    letter-spacing: 0.03em !important;
}
.wx-refresh-btn button:hover {
    background: rgba(58,142,246,0.18) !important;
    border-color: rgba(58,142,246,0.4) !important;
    color: #a8d4ff !important;
}

/* ── Plot container ─────────────────────────────────────────── */
.wx-chart-wrap .gr-plot,
.wx-chart-wrap .svelte-1ickfnv,
.wx-chart-wrap > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 20px !important;
    overflow: hidden !important;
}

/* ── Empty / loading state card ────────────────────────────── */
.wx-chart-empty {
    background: rgba(255,255,255,0.035) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 20px !important;
    padding: 60px 24px !important;
    text-align: center !important;
}
</style>
"""

# ── Palette ───────────────────────────────────────────────────────
_BG       = "rgba(0,0,0,0)"          # transparent — inherits app bg
_PAPER    = "#111b2e"
_GRID     = "rgba(255,255,255,0.06)"
_BLUE     = "#3a8ef6"
_RED      = "#f87171"
_TEXT_MUT = "rgba(160,185,230,0.6)"
_TEXT_PRI = "#dce8ff"
_FONT     = "Outfit, DM Sans, sans-serif"


def _empty_figure() -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text="🌍  Hãy tra cứu một thành phố ở sidebar bên trái",
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color=_TEXT_MUT, family=_FONT),
    )
    fig.update_layout(
        plot_bgcolor=_PAPER,
        paper_bgcolor=_PAPER,
        height=420,
        margin=dict(l=24, r=24, t=40, b=24),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def create_forecast_chart(weather_data: dict) -> go.Figure:
    if not weather_data or "error" in weather_data or "daily" not in weather_data:
        return _empty_figure()

    daily    = weather_data["daily"]
    dates    = [d["date"]          for d in daily]
    temp_max = [d["temp_max"]      for d in daily]
    temp_min = [d["temp_min"]      for d in daily]
    precip   = [d["precipitation"] for d in daily]
    loc      = weather_data["location"]

    fig = go.Figure()

    # ── Temperature fill band ─────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=dates, y=temp_min,
        name="Thấp nhất (°C)",
        mode="lines+markers",
        line=dict(color=_BLUE, width=2.5),
        marker=dict(size=7, color=_BLUE,
                    line=dict(width=2, color=_PAPER)),
        fill="tozeroy",
        fillcolor="rgba(58,142,246,0.08)",
        hovertemplate="<b>%{x}</b><br>Thấp nhất: %{y}°C<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=temp_max,
        name="Cao nhất (°C)",
        mode="lines+markers",
        line=dict(color=_RED, width=2.5),
        marker=dict(size=7, color=_RED,
                    line=dict(width=2, color=_PAPER)),
        fill="tonexty",
        fillcolor="rgba(248,113,113,0.1)",
        hovertemplate="<b>%{x}</b><br>Cao nhất: %{y}°C<extra></extra>",
    ))

    # ── Precipitation bars ────────────────────────────────────────
    fig.add_trace(go.Bar(
        x=dates, y=precip,
        name="Lượng mưa (mm)",
        marker=dict(
            color="rgba(58,142,246,0.22)",
            line=dict(color="rgba(58,142,246,0.55)", width=1),
        ),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Mưa: %{y}mm<extra></extra>",
    ))

    _axis_common = dict(
        gridcolor=_GRID,
        showgrid=True,
        zeroline=False,
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=12, color=_TEXT_MUT, family=_FONT),
    )

    fig.update_layout(
        title=dict(
            text=f"📍  {loc['name']}, {loc['country']}  —  Dự báo 7 ngày",
            font=dict(size=14, color=_TEXT_PRI, family=_FONT),
            x=0, pad=dict(l=4),
        ),
        plot_bgcolor=_PAPER,
        paper_bgcolor=_PAPER,
        height=420,
        margin=dict(l=16, r=16, t=56, b=16),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.04,
            xanchor="right",  x=1,
            font=dict(size=12, color=_TEXT_MUT, family=_FONT),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(**_axis_common),
        yaxis=dict(
            title=dict(text="Nhiệt độ (°C)",
                       font=dict(size=12, color=_TEXT_MUT, family=_FONT)),
            **_axis_common,
        ),
        yaxis2=dict(
            title=dict(text="Lượng mưa (mm)",
                       font=dict(size=12, color=_BLUE, family=_FONT)),
            overlaying="y", side="right",
            showgrid=False,
            tickfont=dict(size=12, color=_BLUE, family=_FONT),
            zeroline=False,
            linecolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor="#1a2a45",
            bordercolor="rgba(58,142,246,0.4)",
            font=dict(family=_FONT, size=13, color=_TEXT_PRI),
        ),
        font=dict(family=_FONT, color=_TEXT_MUT),
    )
    return fig


def create_chart_tab(weather_state: gr.State):
    """Renders the analytics chart panel."""
    gr.HTML(CHART_CSS)

    with gr.Row(equal_height=False):
        with gr.Column():
            gr.Markdown("Analytics & Trends", elem_classes="wx-chart-heading")
            gr.Markdown("7 ngày tới · Nguồn: Open-Meteo", elem_classes="wx-chart-sub")
        with gr.Column(scale=0, min_width=110):
            refresh_btn = gr.Button(
                "↻  Làm mới",
                elem_classes="wx-refresh-btn",
            )

    with gr.Column(elem_classes="wx-chart-wrap"):
        chart = gr.Plot(
            value=_empty_figure(),
            label="",
            show_label=False,
        )

    def update_chart(data):
        return create_forecast_chart(data)

    refresh_btn.click(fn=update_chart, inputs=[weather_state], outputs=[chart])
    weather_state.change(fn=update_chart, inputs=[weather_state], outputs=[chart])