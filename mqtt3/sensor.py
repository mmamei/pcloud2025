# For this example we rely on the Paho MQTT Library
# for Python
# You can install it through the following command:
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import time


# The callback for when the client receives a CONNACK response from the server.
def my_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(command_topic)

def my_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def my_message(client, userdata, message):
    print(message,userdata)
    print("\n##########################################################")
    print("message received: ", str(message.payload.decode("utf-8")))
    print("##########################################################")



# Full MQTT client creation with all the parameters. The only one mandatory in the ClientId that should be unique
# mqtt_client = Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=”tcp”)

# Configuration variables
client_id = "client1"

#broker_ip = "127.0.0.1"
#broker_ip = "34.159.67.93"
#broker_port = 1883

broker_ip = 'broker.emqx.io'
broker_port = 1883

telemetry_topic = "/telemetry/1"
command_topic = '/command/1'


mqtt_client = mqtt.Client(client_id)
mqtt_client.on_connect = my_connect
#mqtt_client.on_publish = my_publish
mqtt_client.on_message = my_message

print("Connecting to "+ broker_ip + " port: " + str(broker_port))
#mqtt_client.tls_set()
#mqtt_client.username_pw_set(username="pcloud23", password="pcloud23")
mqtt_client.connect(broker_ip, broker_port)


mqtt_client.loop_start()

# MQTT Paho Publish method with all the available parameters
# mqtt_client.publish(topic, payload=None, qos=0, retain=False)
message_limit = 1000
for message_id in range(message_limit):
    payload_string = f'message {message_id}'
    infot = mqtt_client.publish(telemetry_topic, payload_string, qos=0)
    infot.wait_for_publish()
    print(f"Message Sent: {message_id}")
    time.sleep(1)

mqtt_client.loop_stop()