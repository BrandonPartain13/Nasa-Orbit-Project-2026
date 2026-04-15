# lunar_energy_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Lunar Energy Management Interface",
    page_icon="🌘",
    layout="wide"
)

# -----------------------------
# PAGE STYLE
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0b1220;
    color: white;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1500px;
}

.panel {
    background-color: rgba(17, 24, 39, 0.9);
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 0 18px rgba(0,0,0,0.25);
}

.panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: #dbeafe;
    letter-spacing: 0.3px;
}

.metric-box {
    background-color: rgba(17, 24, 39, 0.95);
    border: 1px solid #243041;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    min-height: 115px;
}

.metric-label {
    font-size: 0.9rem;
    color: #9ca3af;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #f9fafb;
}

.metric-sub {
    margin-top: 8px;
    font-size: 0.85rem;
    color: #cbd5e1;
}

.status-safe {
    color: #22c55e;
    font-weight: 800;
    font-size: 1.1rem;
}

.status-warning {
    color: #f59e0b;
    font-weight: 800;
    font-size: 1.1rem;
}

.status-critical {
    color: #ef4444;
    font-weight: 800;
    font-size: 1.1rem;
}

.small-note {
    font-size: 0.82rem;
    color: #94a3b8;
}

.big-header {
    font-size: 2rem;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 0.2rem;
}

.sub-header {
    color: #94a3b8;
    margin-bottom: 1.2rem;
}

hr {
    border: none;
    border-top: 1px solid #1f2937;
    margin: 0.5rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("lunar_energy_dataset.csv")
    return df

df = load_data()

# -----------------------------
# PREPARE DATA
# -----------------------------
df["Net Energy (kW)"] = df["Solar Output (kW)"] - df["Power Usage (kW)"]
df["Battery Change (%)"] = df["Battery Charge (%)"].diff().fillna(0)

# simple prediction columns
df["Predicted Battery Next (%)"] = df["Battery Charge (%)"] + df["Net Energy (kW)"] * 0.15
df["Predicted Battery Next (%)"] = df["Predicted Battery Next (%)"].clip(lower=0, upper=100)

# -----------------------------
# AUTONOMOUS DECISION LOGIC
# -----------------------------
def classify_status(row):
    score = 0
    reasons = []

    if row["Power Usage (kW)"] > 60:
        score += 2
        reasons.append("High power demand")

    if row["Solar Output (kW)"] < 20:
        score += 2
        reasons.append("Low solar input")

    if row["Battery Charge (%)"] < 35:
        score += 3
        reasons.append("Low battery reserve")

    if row["Net Energy (kW)"] < -20:
        score += 3
        reasons.append("Negative energy margin")

    if row["Battery Charge (%)"] < 25 and row["Solar Output (kW)"] < 15:
        score += 4
        reasons.append("Critical battery + low generation")

    if score <= 1:
        status = "SAFE"
        action = "Continue nominal science operations."
        confidence = 0.93
    elif score <= 4:
        status = "WARNING"
        action = "Reduce non-essential loads and monitor energy margin."
        confidence = 0.87
    else:
        status = "CRITICAL"
        action = "Enter energy preservation mode and defer non-critical activity."
        confidence = 0.95

    return pd.Series([status, ", ".join(reasons) if reasons else "Nominal conditions", action, confidence])

df[["System Status", "Detected Issues", "Recommended Action", "Confidence"]] = df.apply(classify_status, axis=1)

latest = df.iloc[-1]
alerts_df = df[df["System Status"] != "SAFE"].copy()

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="big-header">Lunar Energy Management Interface</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Autonomous energy monitoring, anomaly detection, and decision support for lunar mission operations</div>',
    unsafe_allow_html=True
)

# -----------------------------
# TOP STATUS ROW
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Battery Charge</div>
        <div class="metric-value">{latest['Battery Charge (%)']:.0f}%</div>
        <div class="metric-sub">Current stored energy</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Solar Output</div>
        <div class="metric-value">{latest['Solar Output (kW)']:.1f} kW</div>
        <div class="metric-sub">Current generation rate</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Power Usage</div>
        <div class="metric-value">{latest['Power Usage (kW)']:.1f} kW</div>
        <div class="metric-sub">Current load demand</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Net Energy</div>
        <div class="metric-value">{latest['Net Energy (kW)']:.1f} kW</div>
        <div class="metric-sub">Generation minus consumption</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    status_class = "status-safe"
    if latest["System Status"] == "WARNING":
        status_class = "status-warning"
    elif latest["System Status"] == "CRITICAL":
        status_class = "status-critical"

    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-label">Mission Status</div>
        <div class="{status_class}">{latest['System Status']}</div>
        <div class="metric-sub">AI confidence: {latest['Confidence']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# MAIN PANELS
# -----------------------------
left, right = st.columns([1.7, 1])

with left:
    st.markdown('<div class="panel"><div class="panel-title">Energy Timeline</div>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Time (hours)"],
        y=df["Battery Charge (%)"],
        mode="lines+markers",
        name="Battery Charge (%)"
    ))
    fig.add_trace(go.Scatter(
        x=df["Time (hours)"],
        y=df["Solar Output (kW)"],
        mode="lines+markers",
        name="Solar Output (kW)"
    ))
    fig.add_trace(go.Scatter(
        x=df["Time (hours)"],
        y=df["Power Usage (kW)"],
        mode="lines+markers",
        name="Power Usage (kW)"
    ))

    fig.update_layout(
        height=430,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.85)",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", y=1.05, x=0),
        xaxis_title="Time (hours)",
        yaxis_title="Value"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel"><div class="panel-title">Autonomous Recommendation</div>', unsafe_allow_html=True)
    st.write(f"**Detected Conditions:** {latest['Detected Issues']}")
    st.write(f"**Recommended Action:** {latest['Recommended Action']}")
    st.write(f"**Predicted Next Battery State:** {latest['Predicted Battery Next (%)']:.1f}%")
    st.write(f"**Decision Confidence:** {latest['Confidence']:.2f}")

    if latest["System Status"] == "SAFE":
        st.success("Nominal operations can continue.")
    elif latest["System Status"] == "WARNING":
        st.warning("Energy risk rising. Reduce discretionary loads.")
    else:
        st.error("Immediate conservation action recommended.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">Operator Controls</div>', unsafe_allow_html=True)
    override = st.selectbox(
        "Override Mode",
        ["Autonomous", "Approve Recommendation", "Delay Action", "Manual Intervention"]
    )
    st.write(f"**Selected Control Mode:** {override}")
    st.caption("This section simulates human-in-the-loop mission operations.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# SECOND ROW
# -----------------------------
left2, right2 = st.columns([1.2, 1.5])

with left2:
    st.markdown('<div class="panel"><div class="panel-title">Net Energy Balance</div>', unsafe_allow_html=True)
    fig2 = px.line(
        df,
        x="Time (hours)",
        y="Net Energy (kW)",
        markers=True,
        template="plotly_dark"
    )
    fig2.add_hline(y=0, line_dash="dash")
    fig2.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.85)",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right2:
    st.markdown('<div class="panel"><div class="panel-title">Detected Alerts</div>', unsafe_allow_html=True)
    if alerts_df.empty:
        st.success("No warning or critical events detected in the dataset.")
    else:
        st.dataframe(
            alerts_df[[
                "Time (hours)",
                "Battery Charge (%)",
                "Solar Output (kW)",
                "Power Usage (kW)",
                "Net Energy (kW)",
                "System Status",
                "Detected Issues",
                "Recommended Action"
            ]],
            use_container_width=True,
            height=320
        )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FULL DATA
# -----------------------------
st.markdown('<div class="panel"><div class="panel-title">Telemetry Table</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, height=260)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="small-note">Prototype interface for lunar energy awareness, anomaly detection, and explainable mission decision support.</div>',
    unsafe_allow_html=True
)