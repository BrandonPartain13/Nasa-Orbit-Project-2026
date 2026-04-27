import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#import json_response

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Lunar Energy Autonomy Dashboard",
    layout="wide"
)

# -----------------------------
# SAMPLE VALUES
# -----------------------------
battery_level = 61.8
solar_input = 11.2
power_load = 43.5
predicted_battery = 59.8
decision_confidence = 0.95

# Dynamic system state priority
if battery_level < 50:
    system_state = "CRITICAL"
elif battery_level < 65:
    system_state = "WARNING"
elif battery_level < 75:
    system_state = "CAUTION"
else:
    system_state = "NOMINAL"

state_class = {
    "CRITICAL": "state-critical",
    "WARNING": "state-warning",
    "CAUTION": "state-caution",
    "NOMINAL": "state-nominal"
}[system_state]

# -----------------------------
# DARK NASA-STYLE CSS
# -----------------------------
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #000000;
}

/* Remove extra white areas */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #000000 !important;
    color: white !important;
}

/* Title */
.dashboard-title {
    font-size: 36px;
    font-weight: 800;
    color: white;
    margin-bottom: 12px;
}

/* Metric cards */
.metric-card {
    background-color: #0a0a0a;
    border: 1px solid #222222;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-label {
    color: #9ca3af;
    font-size: 14px;
    letter-spacing: 0.08em;
    font-weight: 700;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: 900;
}

/* Priority system state colors */
.state-critical {
    color: #ff3b3b;
    font-size: 38px;
    font-weight: 900;
}

.state-warning {
    color: #ff4d4f;
    font-size: 38px;
    font-weight: 900;
}

.state-caution {
    color: #ffd60a;
    font-size: 38px;
    font-weight: 900;
}

.state-nominal {
    color: #4ea8de;
    font-size: 38px;
    font-weight: 900;
}

/* Panels */
.panel-card {
    background-color: #0a0a0a;
    border: 1px solid #222222;
    border-radius: 18px;
    padding: 20px;
    margin-top: 10px;
}

.panel-title {
    color: white;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 14px;
}

/* Right alert panel */
.alert-panel {
    color: #e6f1ff;
    font-size: 20px;
    line-height: 1.5;
}

.alert-label {
    color: #9ca3af;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-top: 16px;
    margin-bottom: 4px;
}

.alert-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
    line-height: 1.2;
}

.alert-critical {
    color: #ff4d4f;
    font-size: 52px;
    font-weight: 900;
    line-height: 1.1;
}

.alert-accent {
    color: #fbbf24;
    font-size: 28px;
    font-weight: 900;
}

.alert-box {
    background: rgba(255, 77, 79, 0.15);
    border: 1px solid rgba(255, 77, 79, 0.45);
    border-radius: 14px;
    padding: 18px;
    margin-top: 18px;
    font-size: 24px;
    font-weight: 900;
    color: #ffd6d6;
}

/* Selectbox styling */
label {
    color: white !important;
    font-weight: 700 !important;
}

div[data-baseweb="select"] > div {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #333333 !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background-color: #111111;
    color: white;
    border: 1px solid #333333;
    border-radius: 10px;
    font-weight: 700;
}

.stButton > button:hover {
    border: 1px solid #777777;
    color: white;
}

/* Info/success boxes */
[data-testid="stAlert"] {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #333333 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="dashboard-title">Lunar Energy Autonomy Dashboard</div>',
    unsafe_allow_html=True
)

# -----------------------------
# TOP METRICS
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">CURRENT BATTERY</div>
        <div class="metric-value">{battery_level:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SOLAR INPUT</div>
        <div class="metric-value">{solar_input:.1f} W</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">POWER LOAD</div>
        <div class="metric-value">{power_load:.1f} W</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SYSTEM STATE</div>
        <div class="{state_class}">{system_state}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -----------------------------
# DATA
# -----------------------------
time = np.arange(24)

battery = np.array([
    76, 75.5, 74.5, 72, 71.5, 69, 67.5, 67.2, 66, 65, 64.8, 63.8,
    64.9, 66.1, 65.4, 65.2, 65.5, 64.4, 64.5, 65.2, 63.0, 62.5, 61.6, 62.2
])

solar = np.array([
    0, 0, 0, 0, 0, 0, 20, 40, 58, 70, 77, 80,
    77, 68, 56, 35, 18, 0, 0, 0, 0, 0, 0, 0
])

load = np.array([
    38, 40, 35, 41, 37, 38, 47, 40, 35, 43, 35, 41,
    32, 35, 41, 43, 41, 40, 39, 34, 37, 38, 39, 44
])

# -----------------------------
# MAIN LAYOUT
# -----------------------------
left, right = st.columns([2.2, 1])

# -----------------------------
# LEFT PANEL
# -----------------------------
with left:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Energy Timeline</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    ax.plot(time, battery, linewidth=3, label="Battery (%)")
    ax.plot(time, solar, linewidth=3, label="Solar Input (W)")
    ax.plot(time, load, linewidth=3, label="Power Load (W)")

    ax.tick_params(colors="white")
    ax.set_xlabel("Time (hours)", color="white")
    ax.set_ylabel("Value", color="white")

    for spine in ax.spines.values():
        spine.set_color("#333333")

    ax.grid(alpha=0.2)

    legend = ax.legend(
        facecolor="#111111",
        edgecolor="#222222"
    )
    for text in legend.get_texts():
        text.set_color("white")

    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RIGHT PANEL
# -----------------------------
with right:

    st.markdown(
        '<div class="panel-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">Autonomous Recommendation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="alert-panel">

<div class="alert-label">DETECTED CONDITIONS</div>
<div class="alert-accent">Low solar input</div>

<div class="alert-label">RECOMMENDED ACTION</div>
<div class="alert-value">Enter energy conservation mode</div>

<div class="alert-label">PREDICTED NEXT BATTERY STATE</div>
<div class="alert-critical">{predicted_battery:.1f}%</div>

<div class="alert-label">DECISION CONFIDENCE</div>
<div class="alert-value">{decision_confidence:.2f}</div>

<div class="alert-box">
Immediate conservation action recommended
</div>

</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # OPERATOR CONTROLS
    # -----------------------------

    st.markdown(
        '<div class="panel-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-title">Operator Controls</div>',
        unsafe_allow_html=True
    )

    mode = st.selectbox(
        "Autonomy Mode",
        ["Automatic", "Human Approval Required", "Manual Override"]
    )

    priority = st.selectbox(
        "Mission Priority",
        [
            "Energy Preservation",
            "Science Collection",
            "Communications",
            "Navigation"
        ]
    )

    if st.button("Apply Setting"):
        st.success(f"Settings updated: {mode} | {priority}")

    if st.button("Acknowledge Alert"):
        st.info("Alert acknowledged.")

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
