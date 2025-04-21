# blueprints/hana_control.py

from flask import Blueprint, jsonify
import requests
import logging
from config import IDENTITY_ZONE,REGION, INSTANCE_ID, CLIENT_ID, CLIENT_SECRET

hana_bp = Blueprint('hana', __name__, url_prefix='/hana')

AUTH_URL = f"https://{IDENTITY_ZONE}.authentication.{REGION}.sap.hana.ondemand.com/oauth/token"
API_BASE_URL = f"https://api.{REGION}.hana.ondemand.com/hanacloud/instances"

logging.basicConfig(level=logging.INFO)

def get_oauth_token():
    logging.info("Attempting to obtain OAuth token")
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(AUTH_URL, data=data, headers=headers)
        response.raise_for_status()
        logging.info("Successfully obtained OAuth token")
        return response.json()["access_token"]
    except Exception as e:
        logging.error(f"Failed to obtain OAuth token: {str(e)}")
        raise

def get_instance_status(token):
    logging.info(f"Checking status for HANA instance {INSTANCE_ID}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"{API_BASE_URL}/{INSTANCE_ID}", headers=headers)
        response.raise_for_status()
        status = response.json()["status"]
        logging.info(f"HANA instance status: {status}")
        return status
    except Exception as e:
        logging.error(f"Failed to get instance status: {str(e)}")
        raise

def start_instance(token):
    logging.info(f"Attempting to start HANA instance {INSTANCE_ID}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(f"{API_BASE_URL}/{INSTANCE_ID}/start", headers=headers)
        response.raise_for_status()
        logging.info("Successfully initiated HANA instance start")
        return response.json()
    except Exception as e:
        logging.error(f"Failed to start instance: {str(e)}")
        raise

@hana_bp.route('/start-if-stopped', methods=['POST'])
def start_if_stopped():
    logging.info("Received request to start HANA instance if stopped")
    try:
        token = get_oauth_token()
        status = get_instance_status(token)

        if status == "STOPPED":
            logging.info("HANA instance is stopped, initiating start")
            result = start_instance(token)
            return jsonify({"message": "HANA DB was stopped and has been started.", "details": result}), 200
        elif status == "RUNNING":
            logging.info("HANA instance is already running")
            return jsonify({"message": "HANA DB is already running."}), 200
        else:
            logging.warning(f"HANA instance is in transitional state: {status}")
            return jsonify({"message": f"HANA DB is in transitional state: {status}. No action taken."}), 200

    except Exception as e:
        logging.error(f"Error in start-if-stopped endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
