import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time as pytime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Lunar Energy Autonomy Dashboard",
    layout="wide"
)

# -----------------------------
# MATLAB-STYLE SIMULATION LOGIC
# -----------------------------
dt = 1
time = np.arange(25)

battery_capacity = 100
initial_battery = 76

solar = np.array([
    0, 0, 0, 0, 0, 0, 20, 40, 58, 70, 77, 80,
    77, 68, 56, 35, 18, 0, 0, 0, 0, 0, 0, 0, 0
])

load = np.array([
    38, 40, 35, 41, 37, 38, 47, 40, 35, 43, 35, 41,
    32, 35, 41, 43, 41, 40, 39, 34, 37, 38, 39, 44, 43
])

charge_efficiency = 0.85
discharge_factor = 0.08

battery = np.zeros(len(time))
battery[0] = initial_battery

for i in range(1, len(time)):
    net_power_step = solar[i - 1] - load[i - 1]

    if net_power_step >= 0:
        battery[i] = battery[i - 1] + net_power_step * charge_efficiency * discharge_factor
    else:
        battery[i] = battery[i - 1] + net_power_step * discharge_factor

    battery[i] = max(0, min(battery_capacity, battery[i]))

net_power = solar - load

# -----------------------------
# LIVE WEBSITE ITERATION
# -----------------------------
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "running" not in st.session_state:
    st.session_state.running = True

current_step = st.session_state.current_step

time_view = time[:current_step]
battery_view = battery[:current_step]
solar_view = solar[:current_step]
load_view = load[:current_step]
net_power_view = net_power[:current_step]

battery_level = battery_view[-1]
solar_input = solar_view[-1]
power_load = load_view[-1]

predicted_battery = battery_level + ((solar_input - power_load) * discharge_factor)
predicted_battery = max(0, min(100, predicted_battery))

# -----------------------------
# AUTONOMOUS DECISION LOGIC
# -----------------------------
if battery_level < 50:
    system_state = "CRITICAL"
    detected_condition = "Battery below critical threshold"
    recommended_action = "Enter emergency survival mode"
    decision_confidence = 0.98
elif battery_level < 65 and solar_input < power_load:
    system_state = "WARNING"
    detected_condition = "Low solar input and negative power balance"
    recommended_action = "Enter energy conservation mode"
    decision_confidence = 0.95
elif battery_level < 75:
    system_state = "CAUTION"
    detected_condition = "Battery margin decreasing"
    recommended_action = "Reduce non-essential science activity"
    decision_confidence = 0.88
else:
    system_state = "NOMINAL"
    detected_condition = "Energy state stable"
    recommended_action = "Continue planned operations"
    decision_confidence = 0.82

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
.stApp {
    background-color: #000000;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #000000 !important;
    color: white !important;
}

.dashboard-title {
    font-size: 36px;
    font-weight: 800;
    color: white;
    margin-bottom: 12px;
}

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
    font-size: 24px;
    letter-spacing: 0.08em;
    font-weight: 700;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 34px;
    font-weight: 900;
}

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

label {
    color: white !important;
    font-weight: 700 !important;
}

div[data-baseweb="select"] > div {
    background-color: #0b1220 !important;
    color: white !important;
    border: 2px solid #4ea8de !important;
    border-radius: 14px !important;
    min-height: 64px !important;
    font-size: 22px !important;
    box-shadow: 0px 0px 8px rgba(78,168,222,0.25);
}

div[data-baseweb="select"] svg {
    fill: #4ea8de !important;
    transform: scale(1.25);
}

div[data-baseweb="select"] span {
    color: white !important;
    font-size: 22px !important;
    font-weight: 800 !important;
}

div[data-baseweb="select"]:hover > div {
    border: 2px solid #ffffff !important;
}

div[data-testid="stSelectbox"] label {
    color: #4ea8de !important;
    font-size: 26px !important;
    font-weight: 900 !important;
    letter-spacing: 0.06em !important;
}

.stButton > button {
    background-color: #1f2937 !important;
    color: white !important;
    border: 2px solid #4ea8de !important;
    border-radius: 14px !important;
    padding: 18px 26px !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    width: 100% !important;
    margin-top: 14px !important;
    box-shadow: 0px 0px 10px rgba(78,168,222,0.25);
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    background-color: #4ea8de !important;
    border: 2px solid #ffffff !important;
    color: black !important;
    box-shadow: 0px 0px 18px rgba(78,168,222,0.6);
}

.stButton > button:active {
    transform: scale(0.97);
}

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

    ax.plot(time_view, battery_view, linewidth=3, label="Battery (%)")
    ax.plot(time_view, solar_view, linewidth=3, label="Solar Input (W)")
    ax.plot(time_view, load_view, linewidth=3, label="Power Load (W)")
    ax.plot(time_view, net_power_view, linewidth=2, linestyle="--", label="Net Power Balance")

    ax.scatter(time_view[-1], battery_view[-1], s=90)
    ax.scatter(time_view[-1], solar_view[-1], s=90)
    ax.scatter(time_view[-1], load_view[-1], s=90)
    ax.scatter(time_view[-1], net_power_view[-1], s=90)

    ax.set_xlim(0, len(time) - 1)
    ax.set_ylim(min(net_power) - 10, max(solar) + 15)

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

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Battery Prediction Detail</div>', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    fig2.patch.set_facecolor("#000000")
    ax2.set_facecolor("#000000")

    ax2.plot(time_view, battery_view, linewidth=3, label="Battery History")
    ax2.scatter(time_view[-1], battery_view[-1], s=100, label="Current Battery")
    ax2.scatter(time_view[-1] + 1, predicted_battery, s=100, label="Predicted Next Battery")

    ax2.set_xlim(0, len(time))
    ax2.set_ylim(0, 100)

    ax2.tick_params(colors="white")
    ax2.set_xlabel("Time (hours)", color="white")
    ax2.set_ylabel("Battery (%)", color="white")

    for spine in ax2.spines.values():
        spine.set_color("#333333")

    ax2.grid(alpha=0.2)

    legend2 = ax2.legend(
        facecolor="#111111",
        edgecolor="#222222"
    )

    for text in legend2.get_texts():
        text.set_color("white")

    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RIGHT PANEL
# -----------------------------
with right:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Autonomous Recommendation</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="alert-panel">

<div class="alert-label">DETECTED CONDITIONS</div>
<div class="alert-accent">{detected_condition}</div>

<div class="alert-label">RECOMMENDED ACTION</div>
<div class="alert-value">{recommended_action}</div>

<div class="alert-label">PREDICTED NEXT BATTERY STATE</div>
<div class="alert-critical">{predicted_battery:.1f}%</div>

<div class="alert-label">DECISION CONFIDENCE</div>
<div class="alert-value">{decision_confidence:.2f}</div>

<div class="alert-box">
Autonomous energy decision generated from live simulation logic
</div>

</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # OPERATOR CONTROLS
    # -----------------------------
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Operator Controls</div>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # SIMULATION RESULTS SUMMARY
    # -----------------------------
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Simulation Results</div>', unsafe_allow_html=True)

    st.write(f"Current Time: {time_view[-1]} hours")
    st.write(f"Initial Battery: {initial_battery:.1f}%")
    st.write(f"Current Battery: {battery_level:.1f}%")
    st.write(f"Current Net Power: {net_power_view[-1]:.1f} W")
    st.write(f"Predicted Next Battery: {predicted_battery:.1f}%")
    st.write(f"System State: {system_state}")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# AUTO LIVE WEBSITE LOOP
# -----------------------------
if st.session_state.running:
    pytime.sleep(0.6)

    st.session_state.current_step += 1

    if st.session_state.current_step > len(time):
        st.session_state.current_step = 1

    st.rerun()