import streamlit as st
import numpy as np
import requests
import time
from PIL import Image
import ast
from multimedia_function import take_shots

# Get some data.
accel_data = np.random.randn(1, 3)
light_data = np.random.randn(1, 1)

st.sidebar.title("Controls")

stop_button_exist = False
stop_button = False
if st.sidebar.button("start"):
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
            stop_button = st.sidebar.button("stop")
            stop_button_exist = True
        if stop_button:
            break

if st.sidebar.button("Shot"):
    take_shots("image.jpg")
    image = Image.open('image.jpg')
    st.image(image, caption='Your Picture', use_column_width=True)