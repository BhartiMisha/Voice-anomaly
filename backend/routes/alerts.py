from flask import Blueprint, jsonify, request
from db.crud import get_recent_alerts, mark_alert_valid

alerts_bp = Blueprint("alerts", __name__)

from bson import ObjectId
from flask import Blueprint, jsonify
from db.crud import mark_alert_valid

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/", methods=["GET"])
def fetch_alerts():
    alerts = get_recent_alerts()
    for alert in alerts:
        alert["_id"] = str(alert["_id"])
    return jsonify(alerts)

@alerts_bp.route("/mark-valid/<alert_id>", methods=["POST"])
def mark_valid(alert_id):
    try:
        obj_id = ObjectId(alert_id)  # Ensure correct type
        result = mark_alert_valid(obj_id)
        if result:
            return jsonify({"status": "success"})
        return jsonify({"status": "failed"}), 404
    except Exception as e:
        print(f"Error marking alert valid: {e}")
        return jsonify({"status": "failed"}), 400

