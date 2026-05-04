# Nasa-Orbit-Project-2026

Github project for Nasa Orbit 2026 competition



To run the dashboard:

```
streamlit run dashboard.py
```

To run the api:
```
uvicorn api:app --reload
```

Lunar Energy Autonomy Dashboard

A real-time simulation dashboard for energy-aware autonomous decision-making in space missions, inspired by lunar surface operations.

This project visualizes how a spacecraft or rover manages power under changing environmental conditions (solar input vs. load), and demonstrates autonomous system behavior under resource constraints.

🚀 Features

📈 Live Time-Series Visualization
Battery level
Solar input
Power load
Net power balance
(Updates automatically like a stock market chart)

🤖 Autonomous Decision Engine
Detects system state (Nominal, Caution, Warning, Critical)
Generates recommended actions
Outputs decision confidence

🔋 Battery Prediction
Predicts next time-step energy state
Visualized alongside historical data

🎛️ Operator Controls
Autonomy mode selection
Mission priority selection
Alert acknowledgment

🌑 NASA-style UI
Dark themed interface
Mission control–style layout
High readability for decision-making
