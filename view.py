import streamlit as st
import numpy as np
import requests
import time
from PIL import Image
import ast
from multimedia_function import take_shots, enable_torch, disable_torch, zoom
import os
import paho.mqtt.client as mqtt
import os
import numpy as np
from PIL import Image
import streamlit as st
import time

from utils.helpers import byte_array_to_pil_image, get_now_string, get_config
from utils.mqtt import get_mqtt_client

# broker configs
CONFIG_FILE_PATH = os.getenv("MQTT_CAMERA_CONFIG", "./config/config.yml")
CONFIG = get_config(CONFIG_FILE_PATH)

MQTT_BROKER = CONFIG["mqtt"]["broker"]
MQTT_PORT = CONFIG["mqtt"]["port"]
MQTT_QOS = CONFIG["mqtt"]["QOS"]

MQTT_TOPIC = CONFIG["save-captures"]["mqtt_topic"]

VIEWER_WIDTH = 600

def get_random_numpy():
    return np.random.randint(0, 100, size=(32, 32))


viewer = st.image(get_random_numpy(), width=VIEWER_WIDTH)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    st.write(f"Connected with result code {str(rc)} to MQTT broker on {MQTT_BROKER}")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic != MQTT_TOPIC:
        return
    image = byte_array_to_pil_image(msg.payload)
    image = image.convert("RGB")
    viewer.image(image, width=VIEWER_WIDTH)

###



# Get some data.
accel_data = np.random.randn(1, 3)
light_data = np.random.randn(1, 1)

st.sidebar.title("Controls")

stop_button_exist = False
stop_button = False
if st.sidebar.button("Start"):
    # Show the data as a chart.
    light_chart = st.line_chart(light_data)
    accel_chart = st.line_chart(accel_data)

    while True:
        # Grab some more data.
        r = requests.get("http://192.168.0.7:8080/sensors.json")
        response_str = r.content.decode("utf-8")
        response = ast.literal_eval(response_str)
        t, accel = [x[0] for x in response['lin_accel']['data']], [x[1:][0] for x in response['lin_accel']['data']]

        light = [x[1:][0] for x in response['light']['data']]

        accel_data = np.array([np.array(xi) for xi in accel])
        # Append the new data to the existing chart.

        accel_chart.add_rows(np.expand_dims(np.mean(accel_data, axis=0), axis=0))
        light_chart.add_rows(np.mean(light, axis=0))

        #time.sleep(0.01)

        if not stop_button_exist:
            stop_button = st.sidebar.button("Stop")
            stop_button_exist = True
        if stop_button:
            break

if st.sidebar.button("Shot"):
    take_shots("image.jpg")
    image = Image.open('image.jpg')
    st.image(image, caption='Your Picture', use_column_width=True)

value = st.sidebar.slider("Zoom", min_value=1, max_value=15)
zoom(value)

if st.sidebar.checkbox("Torch"):
    enable_torch()
else:
    disable_torch()

#if st.sidebar.button("Stream Video"):
client = get_mqtt_client()
client.on_message = on_message
client.connect(MQTT_BROKER, port=MQTT_PORT)
client.subscribe(MQTT_TOPIC)
time.sleep(4)  # Wait for connection setup to complete
client.loop_forever()