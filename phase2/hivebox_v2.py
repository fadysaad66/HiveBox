"""Flask app that fetches average temperature from OpenSenseMap."""

from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
APP_VERSION = "2.0.1"

def get_cutoff_iso(hours):
    """Return ISO 8601 timestamp from `hours` ago in UTC."""
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

def is_recent(timestamp_iso, cutoff_iso):
    """Check if a given ISO timestamp is more recent than the cutoff."""
    try:
        ts = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
        cutoff = datetime.fromisoformat(cutoff_iso)
        return ts > cutoff
    except ValueError as e:
        print(f"[ERROR] Timestamp parse failed: {e}")
        return False

def is_valid_temp_sensor(sensor):
    """Determine if the sensor likely reports temperature data."""
    title = sensor.get('title', '').lower()
    return any(k in title for k in ['temp', '°c', 'air']) and isinstance(sensor.get('lastMeasurement'), dict)

@app.route('/version')
def version():
    """Return app version."""
    return jsonify({'version': APP_VERSION})

@app.route('/temperature')
def temperature():
    """Fetch and average temperature values updated within cutoff time."""
    try:
        hours = float(request.args.get('hours', 12))
        cutoff_iso = get_cutoff_iso(hours)
        response = requests.get(
            'https://api.opensensemap.org/boxes?phenomenon=temperature',
            timeout=10
        )
        response.raise_for_status()
        boxes = response.json()

        temps = []
        for box in boxes:
            for sensor in box.get('sensors', []):
                if not is_valid_temp_sensor(sensor):
                    continue
                meas = sensor['lastMeasurement']
                ts = meas.get('createdAt')
                val = meas.get('value')
                if ts and val is not None and is_recent(ts, cutoff_iso):
                    try:
                        temps.append(float(val))
                    except (ValueError, TypeError):
                        continue

        if temps:
            return jsonify({
                'average_temperature': round(sum(temps) / len(temps), 2),
                'unit': '°C',
                'count': len(temps),
                'cutoff_time': cutoff_iso
            })

        return jsonify({
            'message': f'No recent temperature data found in the last {int(hours)} hours.',
            'cutoff_time': cutoff_iso
        }), 404

    except requests.RequestException as err:
        return jsonify({'error': f'Request failed: {err}'}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
