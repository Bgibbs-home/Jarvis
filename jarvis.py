from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get('TOKEN')
HOME_ASSISTANT_URL = os.environ.get('HOME_ASSISTANT_URL')

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    cmd = data.get('command', '').lower()

    if "turn on the lights" in cmd:
        service_url = f"{HOME_ASSISTANT_URL}/services/light/turn_on"
        payload = {"entity_id": "light.living_room"}
        response = requests.post(service_url, json=payload, headers=headers)
        if response.status_code == 200:
            return jsonify({"status": "ok", "message": "Turning on the lights."})
        else:
            return jsonify({"status": "error", "message": "Failed to turn on the lights."}), 500

    return jsonify({"status": "error", "message": "Unknown command."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
