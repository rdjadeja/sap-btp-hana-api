# 🚀 SAP HANA Cloud Control API (Flask)

This project provides a lightweight REST API to manage your **SAP HANA Cloud database instance** hosted on **SAP BTP**. It includes an endpoint to **start the DB only if it's currently stopped**, using **OAuth2** authentication and SAP HANA Cloud Management APIs.

---

## 📦 Features

- 🌐 REST API built with Flask + Blueprints
- 🔐 Secure OAuth2 authentication via SAP BTP XSUAA
- 📡 Retrieves current DB instance status
- ▶️ Starts DB instance if status is `STOPPED`
- 🧪 Postman collection included for easy testing

---

## 🏗️ Project Structure

hana_api/ ├── app.py # Flask app entry point ├── blueprints/ │ └── hana_control.py # Blueprint with logic ├── config.py # SAP BTP credentials & region config ├── requirements.txt # Python dependencies ├── hana_postman_collection.json # Postman collection └── README.md # You're here!


---

## ⚙️ Configuration

Edit the `config.py` file with your SAP BTP values:

```python
REGION = "eu10"  # Example: us10, ap10, etc.
INSTANCE_ID = "<your_hana_instance_id>"
CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"

💻 Installation & Usage
1. Clone the repo
bash
Copy
Edit
git clone https://github.com/your-username/hana-cloud-control-api.git
cd hana-cloud-control-api
2. Set up virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the Flask app
bash
Copy
Edit
python app.py
The API will now be available at:
http://localhost:5000/hana/start-if-stopped

🔄 API Endpoint
POST /hana/start-if-stopped
Checks the HANA DB instance status and starts it if it is stopped.

✅ Example Response (DB started):

{
  "message": "HANA DB was stopped and has been started.",
  "details": { ... }
}
✅ Already running:
{
  "message": "HANA DB is already running."
}
⚠️ In transitional state:
{
  "message": "HANA DB is in transitional state: STARTING. No action taken."
}
🧪 Testing with Postman
Use the provided Postman collection:

➤ Steps
Open Postman

Import hana_postman_collection.json

Send request to POST http://localhost:5000/hana/start-if-stopped

🔐 Security Note
For production use:

Do not store credentials in config.py. Use environment variables or a vault.

Secure the endpoint (API keys, basic auth, OAuth2).

Add HTTPS and proper access control.

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute.

🤝 Contributing
Pull requests are welcome! Feel free to open issues or feature requests as well.

🧠 Author
Ravi
Made with ❤️ for SAP HANA Cloud & Flask

PS: README generated using a bot !
