import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Lunar Mission Energy Console",
    page_icon="🌘",
    layout="wide"
)

# -------------------------
# GLOBAL DARK STYLE
# -------------------------

st.markdown("""
<style>

.stApp {
    background-color: #050a14;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0c1425;
    color: white;
}

html, body, [class*="css"] {
    color: white !important;
}

h1, h2, h3, h4 {
    color: white !important;
}

.panel {
    background-color: #0f172a;
    border-radius: 14px;
    padding: 18px;
}

.metric-box {
    background-color: #0f172a;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
}

.status-safe {
    color: #22c55e;
    font-weight: bold;
}

.status-warning {
    color: #f59e0b;
    font-weight: bold;
}

.status-critical {
    color: #ef4444;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    return pd.read_csv("lunar_energy_dataset.csv")

df = load_data()

# -------------------------
# DERIVED METRICS
# -------------------------

df["Net Energy (kW)"] = df["Solar Output (kW)"] - df["Power Usage (kW)"]

df["Predicted Battery (%)"] = (
    df["Battery Charge (%)"] +
    df["Net Energy (kW)"] * 0.2
).clip(0, 100)

# -------------------------
# AUTONOMOUS STATUS ENGINE
# -------------------------

def classify(row):

    score = 0
    issues = []

    if row["Battery Charge (%)"] < 50:
        score += 1
        issues.append("Battery below preferred reserve")

    if row["Battery Charge (%)"] < 35:
        score += 2
        issues.append("Battery low")

    if row["Solar Output (kW)"] < 20:
        score += 2
        issues.append("Low solar generation")

    if row["Power Usage (kW)"] > 60:
        score += 2
        issues.append("High load demand")

    if row["Net Energy (kW)"] < 0:
        score += 2
        issues.append("Negative energy balance")

    if row["Battery Charge (%)"] < 25 and row["Net Energy (kW)"] < -10:
        score += 3
        issues.append("Critical reserve depletion risk")

    if score <= 2:
        status = "SAFE"
        action = "Continue nominal science operations."
        confidence = 0.92

    elif score <= 5:
        status = "WARNING"
        action = "Reduce non-essential loads."
        confidence = 0.87

    else:
        status = "CRITICAL"
        action = "Enter survival energy mode."
        confidence = 0.95

    return pd.Series([status, ", ".join(issues), action, confidence])


df[
    ["System Status",
     "Detected Issues",
     "Recommended Action",
     "Confidence"]
] = df.apply(classify, axis=1)

latest = df.iloc[-1]

alerts = df[df["System Status"] != "SAFE"]

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------

st.sidebar.title("Mission Console")

view = st.sidebar.radio(
    "Navigation",
    ["Overview", "Autonomy", "Telemetry", "Alerts"]
)

override = st.sidebar.selectbox(
    "Operator Override Mode",
    [
        "Autonomous",
        "Approve AI Decision",
        "Delay Decision",
        "Manual Control"
    ]
)

# -------------------------
# HEADER
# -------------------------

st.title("🌘 Lunar Energy Management Interface")

st.caption(
    "Autonomous energy monitoring, anomaly detection, and decision support"
)

# -------------------------
# KPI ROW
# -------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Battery", f"{latest['Battery Charge (%)']:.0f}%")
c2.metric("Solar Output", f"{latest['Solar Output (kW)']:.1f} kW")
c3.metric("Power Load", f"{latest['Power Usage (kW)']:.1f} kW")
c4.metric("Net Energy", f"{latest['Net Energy (kW)']:.1f} kW")
c5.metric("Confidence", f"{latest['Confidence']:.2f}")

# -------------------------
# OVERVIEW PAGE
# -------------------------

if view == "Overview":

    left, right = st.columns([2, 1])

    with left:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Time (hours)"],
            y=df["Battery Charge (%)"],
            mode="lines+markers",
            name="Battery"
        ))

        fig.add_trace(go.Scatter(
            x=df["Time (hours)"],
            y=df["Solar Output (kW)"],
            mode="lines",
            name="Solar"
        ))

        fig.add_trace(go.Scatter(
            x=df["Time (hours)"],
            y=df["Power Usage (kW)"],
            mode="lines",
            name="Load"
        ))

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        net_fig = px.bar(
            df,
            x="Time (hours)",
            y="Net Energy (kW)",
            template="plotly_dark"
        )

        st.plotly_chart(net_fig, use_container_width=True)

    with right:

        st.subheader("AI Recommendation")

        st.write("Conditions:", latest["Detected Issues"])
        st.write("Recommendation:", latest["Recommended Action"])
        st.write("Predicted Battery:", latest["Predicted Battery (%)"])
        st.write("Override Mode:", override)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=float(latest["Battery Charge (%)"]),
            title={'text': "Battery Gauge"},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 25], 'color': "#7f1d1d"},
                    {'range': [25, 50], 'color': "#78350f"},
                    {'range': [50, 100], 'color': "#14532d"}
                ]
            }
        ))

        gauge.update_layout(template="plotly_dark")

        st.plotly_chart(gauge, use_container_width=True)

# -------------------------
# AUTONOMY PAGE
# -------------------------

elif view == "Autonomy":

    st.subheader("Autonomous Decision Summary")

    st.write("System Status:", latest["System Status"])
    st.write("Issues:", latest["Detected Issues"])
    st.write("Action:", latest["Recommended Action"])
    st.write("Confidence:", latest["Confidence"])
    st.write("Override:", override)

# -------------------------
# TELEMETRY PAGE
# -------------------------

elif view == "Telemetry":

    st.subheader("Telemetry Table")

    st.dataframe(df, use_container_width=True)

# -------------------------
# ALERT PAGE
# -------------------------

elif view == "Alerts":

    st.subheader("Detected Alerts")

    if alerts.empty:
        st.success("No alerts detected")

    else:
        st.dataframe(alerts, use_container_width=True)