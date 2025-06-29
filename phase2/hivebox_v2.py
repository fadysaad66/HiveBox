("""Flask app that fetches and returns average temperature from
 OpenSenseMap using RFC3339-compliant timestamps.""")

from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify
import requests

app = Flask(__name__)
APP_VERSION = "1.0.0"

def get_rfc3339_zulu(hours=1):
    ("""Return RFC3339 timestamp without microseconds
      and Z for UTC (e.g., 2025-06-28T18:22:00Z)""")
    return ((datetime.now(timezone.utc) -
             timedelta(hours=hours)).replace(microsecond=0).isoformat().replace('+00:00', 'Z'))

@app.route('/version')
def version():
    """Return app version."""
    return jsonify({'version': APP_VERSION})

@app.route('/temperature')
def temperature():
    """Return average temperature from sensors titled 'temperature' in the last 1 hour."""
    try:
        # Generate proper RFC3339 timestamps for date range
        cutoff_iso = get_rfc3339_zulu(1)  # 1 hour ago
        now_iso = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'))

        # Construct API URL
        url = (f"https://api.opensensemap.org/boxes?"
               f"phenomenon=temperature&date={cutoff_iso},{now_iso}")
        print(f"[DEBUG] Requesting: {url}")

        # Fetch data
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        boxes = response.json()

        temps = []
        for box in boxes:
            for sensor in box.get('sensors', []):
                title = sensor.get('title', '').lower()
                if title != 'temperature':  # strict match
                    continue

                measurement = sensor.get('lastMeasurement', {})
                value = measurement.get('value')

                if value is not None:
                    try:
                        temps.append(float(value))
                    except (ValueError, TypeError):
                        continue

        if temps:
            average = round(sum(temps) / len(temps), 2)
            return jsonify({
                'average_temperature': average,
                'unit': '°C',
                'sensor_count': len(temps),
                'cutoff_time_start': cutoff_iso,
                'cutoff_time_end': now_iso
            })

        return jsonify({
            'message': 'No temperature data found within the last 1 hour.',
            'cutoff_time_start': cutoff_iso,
            'cutoff_time_end': now_iso
        }), 404

    except requests.RequestException as err:
        return jsonify({'error': f'Failed to fetch data: {err}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
