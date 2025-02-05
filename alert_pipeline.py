import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory suppression rules (can be expanded to use a database)
suppression_rules = {}

# Function to process alerts
def process_alert(alert):
    alert_id = alert.get('id')
    if alert_id in suppression_rules:
        return {'status': 'suppressed', 'alert': alert}
    # Simulate sending an email notification
    print(f"Alert Triggered: {alert}")
    return {'status': 'processed', 'alert': alert}

# API to receive alerts
@app.route('/alerts', methods=['POST'])
def receive_alert():
    alert = request.json
    result = process_alert(alert)
    return jsonify(result)

# API to manage suppression rules
@app.route('/suppress', methods=['POST'])
def suppress_alert():
    data = request.json
    alert_id = data.get('alert_id')
    suppression_rules[alert_id] = True
    return jsonify({'status': 'suppressed', 'alert_id': alert_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

