from fastapi import FastAPI

app = FastAPI()

# from dashboard3.
def get_system_state(battery_percent):
    if battery_percent < 50:
        return "CRITICAL"
    
    if battery_percent < 65:
        return "WARNING"

    if battery_percent < 75:
        return "CAUTION"

    return "NOMINAL"

# FIXME: sample values, delete later
sample_battery_percent = 61.8
sample_input_watts = 11.2
sample_load_watts = 43.5
#sample_current_mode = ""
sample_system_state = get_system_state(sample_battery_percent)
sample_battery_prediction = 59.8
sample_action_recommendation = "Immediate conservation action recommended"
sample_action_confidence = 0.95

state_battery_percent = sample_battery_percent
state_input_watts = sample_input_watts
state_load_watts = sample_load_watts
#state_current_mode = sample_current_mode
state_system_state = sample_system_state
state_battery_prediction = sample_battery_prediction # should be a function
state_action_recommendation = sample_action_recommendation # should be a function?
state_action_confidence = sample_action_confidence # should be a function?

def gather_data():
    gathered_data = {
            "battery_percent": state_battery_percent, 
            "input_watts": state_input_watts, 
            "load_watts": state_load_watts, 
            #"current_mode": state_current_mode, 
            "system_state": state_system_state, 
            "battery_prediction": state_battery_prediction, 
            "action_recomendation": state_action_recommendation, 
            "action_confidence": state_action_confidence
            }

    return gathered_data

@app.get("/values")
def return_values():
    return gather_data()
