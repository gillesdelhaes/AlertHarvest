import requests
import json
from datetime import datetime, timedelta
import random

url = 'http://127.0.0.1:8000/api/create_alert/'  # Replace with the actual URL of your API endpoint

# Generate timestamps around today's date minus 4 days
start_timestamp = datetime.now() - timedelta(days=1)

# Define a larger set of locations
locations = [
    "Wind Farm", "Nuclear Reactor", "Gas Power Plant", "Solar Panel Array", "Hydroelectric Dam",
    "Biomass Facility", "Geothermal Station", "Coal Power Station", "Natural Gas Plant", 
    "Tidal Power Station"
]

# Define a larger set of messages and sources for each location
messages_and_sources = {
    "Wind Farm": [
        {"message": "Critical wind turbine failure detected", "source": "Turbine Sensors"},
        {"message": "Wind turbine blade damage detected", "source": "Turbine Sensors"},
        {"message": "Wind turbine gearbox malfunction", "source": "Control System"},
        {"message": "Wind turbine generator failure", "source": "Control System"},
        {"message": "Wind turbine yaw system malfunction", "source": "Turbine Sensors"},
        {"message": "Wind farm communication failure", "source": "SCADA System"},
        {"message": "Power fluctuation in wind farm", "source": "Turbine Sensors"},
        {"message": "Bird strike on wind turbine", "source": "Monitoring System"},
        {"message": "Ice accumulation on wind turbine blades", "source": "Turbine Sensors"},
        {"message": "Maintenance required on wind turbine", "source": "Maintenance System"}
    ],
    "Nuclear Reactor": [
        {"message": "Nuclear reactor coolant leak reported", "source": "Plant Monitoring"},
        {"message": "Nuclear reactor core temperature rise", "source": "Plant Control"},
        {"message": "Nuclear reactor pressure anomaly", "source": "Plant Monitoring"},
        {"message": "Nuclear fuel rod failure detected", "source": "Plant Control"},
        {"message": "Emergency shutdown initiated", "source": "Plant Control"},
        {"message": "Radiation level exceeding limits", "source": "Monitoring System"},
        {"message": "Nuclear plant security breach", "source": "Security Cameras"},
        {"message": "Nuclear plant backup generator failure", "source": "Emergency Power"},
        {"message": "Nuclear plant ventilation system malfunction", "source": "Plant Control"},
        {"message": "Nuclear plant turbine trip", "source": "Plant Monitoring"}
    ],
    "Gas Power Plant": [
        {"message": "Gas pressure exceeding limits", "source": "Plant Control"},
        {"message": "Gas turbine fuel pressure drop", "source": "Turbine Control"},
        {"message": "Gas processing unit failure", "source": "Processing Control"},
        {"message": "Gas turbine combustion instability", "source": "Turbine Control"},
        {"message": "Gas compressor failure", "source": "Compressor Monitoring"},
        {"message": "Gas power plant emissions spike", "source": "Monitoring System"},
        {"message": "Gas turbine vibration abnormality", "source": "Vibration System"},
        {"message": "Gas turbine inlet filter clogging", "source": "Turbine Control"},
        {"message": "Gas turbine flameout detected", "source": "Turbine Control"},
        {"message": "Gas power plant security breach", "source": "Security Cameras"}
    ],
    "Solar Panel Array": [
        {"message": "Critical solar inverter failure", "source": "Inverter Monitoring"},
        {"message": "Solar panel array efficiency drop", "source": "Panel Monitoring"},
        {"message": "Solar panel degradation observed", "source": "Panel Monitoring"},
        {"message": "Solar tracking system failure", "source": "Tracking System"},
        {"message": "Solar panel mismatch issues", "source": "Panel Monitoring"},
        {"message": "Power output fluctuation in solar array", "source": "Panel Monitoring"},
        {"message": "Solar panel shading detected", "source": "Panel Monitoring"},
        {"message": "Solar array communication failure", "source": "Array SCADA"},
        {"message": "Bird nesting on solar panels", "source": "Monitoring System"},
        {"message": "Dust accumulation on solar panels", "source": "Panel Monitoring"}
    ],
    "Hydroelectric Dam": [
        {"message": "Hydroelectric turbine malfunction", "source": "SCADA System"},
        {"message": "Hydroelectric generator failure", "source": "SCADA System"},
        {"message": "Water turbine blade imbalance detected", "source": "Turbine Sensors"},
        {"message": "Hydroelectric dam water level rise", "source": "Dam Monitoring"},
        {"message": "Hydroelectric dam structural integrity warning", "source": "Health Monitoring"},
        {"message": "Fish passage system failure", "source": "Monitoring System"},
        {"message": "Sediment buildup in hydroelectric intake", "source": "Dam Monitoring"},
        {"message": "Hydroelectric dam spillway gate malfunction", "source": "Dam Control"},
        {"message": "Power output fluctuation in hydroelectric plant", "source": "SCADA System"},
        {"message": "Hydroelectric plant security breach", "source": "Security Cameras"}
    ],
    "Biomass Facility": [
        {"message": "Biomass combustion chamber overheating", "source": "Facility Sensors"},
        {"message": "Biomass fuel supply disruption", "source": "Facility Sensors"},
        {"message": "Biomass gasifier failure", "source": "Gasification Control"},
        {"message": "Biomass boiler tube leakage", "source": "Boiler Monitoring"},
        {"message": "Biomass conveyor belt jam reported", "source": "Conveyor Sensors"},
        {"message": "Biomass power plant emissions spike", "source": "Monitoring System"},
        {"message": "Biomass gas cleaning system failure", "source": "Facility Control"},
        {"message": "Biomass facility security breach", "source": "Security Cameras"},
        {"message": "Biomass plant feedstock supply shortage", "source": "Facility Control"},
        {"message": "Biomass power plant electrical system malfunction", "source": "Electrical Monitoring"}
    ],
    "Geothermal Station": [
        {"message": "Geothermal well pressure imbalance", "source": "Plant Control"},
        {"message": "Geothermal power plant equipment failure", "source": "Plant Control"},
        {"message": "Geothermal turbine vibration abnormality", "source": "Turbine Sensors"},
        {"message": "Geothermal fluid temperature drop", "source": "Fluid Monitoring"},
        {"message": "Geothermal plant steam leakage detected", "source": "Plant Control"},
        {"message": "Geothermal plant cooling system failure", "source": "Plant Control"},
        {"message": "Geothermal plant security breach", "source": "Security Cameras"},
        {"message": "Geothermal plant automatic shutdown initiated", "source": "Plant Control"},
        {"message": "Geothermal well pump failure", "source": "Well Monitoring"},
        {"message": "Geothermal power plant electrical system malfunction", "source": "Electrical Monitoring"}
    ],
    "Coal Power Station": [
        {"message": "Coal conveyor belt jam reported", "source": "Conveyor Sensors"},
        {"message": "Coal-fired power plant emissions spike", "source": "Monitoring System"},
        {"message": "Coal-fired power plant equipment failure", "source": "Plant Control"},
        {"message": "Coal combustion chamber overheating", "source": "Plant Control"},
        {"message": "Coal pulverizer malfunction", "source": "Plant Control"},
        {"message": "Coal power plant security breach", "source": "Security Cameras"},
        {"message": "Coal power plant automatic shutdown initiated", "source": "Plant Control"},
        {"message": "Coal power plant backup generator failure", "source": "Emergency Power"},
        {"message": "Coal power plant coal supply shortage", "source": "Plant Control"},
        {"message": "Coal power plant electrical system malfunction", "source": "Electrical Monitoring"}
    ],
    "Natural Gas Plant": [
        {"message": "Natural gas pipeline rupture", "source": "Plant Monitoring"},
        {"message": "Natural gas compressor failure", "source": "Compressor Monitoring"},
        {"message": "Natural gas plant emissions spike", "source": "Monitoring System"},
        {"message": "Natural gas turbine vibration abnormality", "source": "Turbine Control"},
        {"message": "Natural gas processing unit failure", "source": "Processing Control"},
        {"message": "Natural gas power plant security breach", "source": "Security Cameras"},
        {"message": "Natural gas power plant automatic shutdown initiated", "source": "Turbine Control"},
        {"message": "Natural gas power plant backup generator failure", "source": "Emergency Power"},
        {"message": "Natural gas plant fuel supply disruption", "source": "Plant Monitoring"},
        {"message": "Natural gas power plant electrical system malfunction", "source": "Electrical Monitoring"}
    ],
    "Tidal Power Station": [
        {"message": "Tidal power generation fluctuation", "source": "Station Monitoring"},
        {"message": "Turbine malfunction detected", "source": "Turbine Control"},
        {"message": "Unusual tidal flow patterns observed", "source": "Station Sensors"},
        {"message": "Security breach in tidal power facility", "source": "Security Cameras"},
        {"message": "Automatic shutdown initiated due to anomaly", "source": "Station Control"},
        {"message": "Backup generator failure in tidal power plant", "source": "Emergency Power"},
        {"message": "Communication disruption within tidal power system", "source": "Station SCADA"},
        {"message": "Equipment malfunction affecting power output", "source": "Station Control"},
        {"message": "Environmental monitoring alert for tidal power facility", "source": "Environmental Monitoring"},
        {"message": "Unplanned maintenance required for tidal turbine", "source": "Station Maintenance"}
    ]
}

selected_alerts = []

for _ in range(30):
    location = random.choice(locations)
    failure_data = random.choice(messages_and_sources[location])
    severity = random.choice(['CRITICAL', 'MAJOR', 'WARNING'])
    random_minutes = random.randint(1, 1440)  # Random minutes within a day
    timestamp = (start_timestamp + timedelta(minutes=random_minutes)).isoformat()
    data = {
        'location': location,
        'severity': severity,
        'message': failure_data['message'],
        'source': failure_data['source'],
        'timestamp': timestamp
    }

    selected_alerts.append(data)

# Shuffle the selected alerts for randomization
random.shuffle(selected_alerts)

# Send the alerts
for index, data in enumerate(selected_alerts):
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.ok:
        result = response.json()
        print(result['message'])
    else:
        print('Request failed with status code', response.status_code)
