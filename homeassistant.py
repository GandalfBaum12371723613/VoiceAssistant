import requests
from logger import *

HA_URL = "http://192.168.1.111:8123"
with open("HOMEASSISTANT_TOKEN", "r") as file:
    TOKEN = file.read().strip()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def heating_on():
    response = requests.post(
        f"{HA_URL}/api/services/switch/turn_on",
        headers=HEADERS,
        json={"entity_id": "switch.heatingoutlet_switch"},
    )
    log_info(f"{response.status_code} {response.text}")

def heating_off():
    response = requests.post(
        f"{HA_URL}/api/services/switch/turn_off",
        headers=HEADERS,
        json={"entity_id": "switch.heatingoutlet_switch"},
    )
    log_info(f"{response.status_code} {response.text}")
