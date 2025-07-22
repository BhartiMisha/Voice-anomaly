from flask import Flask
from flask_cors import CORS
from routes.user import user_bp
from routes.voice_monitor import monitor_bp
from routes.alerts import alerts_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(monitor_bp, url_prefix="/monitor")
app.register_blueprint(alerts_bp, url_prefix="/alerts")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
