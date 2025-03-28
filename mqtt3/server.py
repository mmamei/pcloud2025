# For this example we rely on the Paho MQTT Library for Python
# You can install it through the following command: pip install paho-mqtt
import time

import paho.mqtt.client as mqtt


# Full MQTT client creation with all the parameters. The only one mandatory in the ClientId that should be unique
# mqtt_client = Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(telemetry_topic)
    print("Subscribed to: " + telemetry_topic)

def on_disconnect(client, userdata, rc):
    print("disConnected with result code ")


database = []

# Define a callback method to receive asynchronous messages
def on_message(client, userdata, message):
    database.append(str(message.payload.decode("utf-8")))
    

# Configuration variables
client_id = "subscriber1"

broker_ip = 'broker.emqx.io'
broker_port = 1883

telemetry_topic = "/telemetry/#"
command_topic = '/command/1'

# Create a new MQTT Client
mqtt_client = mqtt.Client(client_id)
# Attack Paho OnMessage Callback Method
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect

# Connect to the target MQTT Broker
print('connect',broker_ip, broker_port)
#mqtt_client.username_pw_set(username="pcloud23", password="pcloud23")
mqtt_client.connect(broker_ip, broker_port, keepalive=600)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

mqtt_client.loop_start()

while True:
    c = input('inserisci comando: SHOW, ON, OFF, END\n')
    if c == 'END':
        break
    elif c == 'SHOW':
        print('Database:', database)
    else:
        infot = mqtt_client.publish(command_topic, c, qos=2)
        infot.wait_for_publish()

mqtt_client.loop_stop()