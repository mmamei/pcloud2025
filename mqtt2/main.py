from flask import Flask, jsonify, request
from flask_mqtt import Mqtt

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  # Change to your broker
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TOPIC'] = '/test/#'

mqtt = Mqtt(app)

# Flask route
@app.route('/')
def home():
    return "Flask App with Flask-MQTT Integration!"

# Callback for MQTT message received
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    msg_payload = message.payload.decode()
    print(f"Received MQTT message: {msg_payload} on topic {message.topic}")

    # Call a Flask endpoint programmatically
    with app.test_request_context():
        response = mqtt_callback({"topic": message.topic, "message": msg_payload})
        print("Flask callback response:", response.get_json())

# Flask route to handle MQTT-triggered action
@app.route('/mqtt_callback', methods=['POST'])
def mqtt_callback(data=None):
    if data is None:
        data = request.json  # Get data from request if manually triggered
    print(f"Flask received MQTT callback: {data}")
    return jsonify({"status": "success", "received_data": data})

# Subscribe to MQTT topic on startup
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    mqtt.subscribe(app.config['MQTT_TOPIC'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)