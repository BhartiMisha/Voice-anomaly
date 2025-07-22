from flask import Blueprint, jsonify, request
from db.crud import get_recent_alerts, mark_alert_valid

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/", methods=["GET"])
def fetch_alerts():
    alerts = get_recent_alerts()
    for alert in alerts:
        alert["_id"] = str(alert["_id"])
    return jsonify(alerts)

@alerts_bp.route("/mark-valid/<alert_id>", methods=["POST"])
def mark_valid(alert_id):
    updated = mark_alert_valid(alert_id)
    return jsonify({"status": "success" if updated else "failed"})
