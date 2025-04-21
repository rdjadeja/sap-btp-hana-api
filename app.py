# app.py

from flask import Flask
from blueprints.hana_control import hana_bp

app = Flask(__name__)
app.register_blueprint(hana_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
