# blueprints/hana_control.py

from flask import Blueprint, jsonify
import requests
from config import REGION, INSTANCE_ID, CLIENT_ID, CLIENT_SECRET

hana_bp = Blueprint('hana', __name__, url_prefix='/hana')

AUTH_URL = f"https://{REGION}.authentication.sap.hana.ondemand.com/oauth/token"
API_BASE_URL = f"https://api.{REGION}.hana.ondemand.com/hanacloud/instances"

def get_oauth_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(AUTH_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def get_instance_status(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{API_BASE_URL}/{INSTANCE_ID}", headers=headers)
    response.raise_for_status()
    return response.json()["status"]

def start_instance(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{API_BASE_URL}/{INSTANCE_ID}/start", headers=headers)
    response.raise_for_status()
    return response.json()

@hana_bp.route('/start-if-stopped', methods=['POST'])
def start_if_stopped():
    try:
        token = get_oauth_token()
        status = get_instance_status(token)

        if status == "STOPPED":
            result = start_instance(token)
            return jsonify({"message": "HANA DB was stopped and has been started.", "details": result}), 200
        elif status == "RUNNING":
            return jsonify({"message": "HANA DB is already running."}), 200
        else:
            return jsonify({"message": f"HANA DB is in transitional state: {status}. No action taken."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
