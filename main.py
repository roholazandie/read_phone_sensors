import requests
import ast
import numpy as np
import time

while True:
    r = requests.get("http://192.168.0.7:8080/sensors.json")

    response_str = r.content.decode("utf-8")
    response = ast.literal_eval(response_str)

    #t, gyro = [x[0] for x in response['mag']['data']], [x[1:][0] for x in response['mag']['data']]
    t, accel = [x[0] for x in response['accel']['data']], [x[1:][0] for x in response['accel']['data']]
    t, light = [x[0] for x in response['light']['data']], [x[1:][0] for x in response['light']['data']]

    gyro_data = np.array([np.array(xi) for xi in accel])
    print(gyro_data.shape)

    print(np.max(gyro_data))
    time.sleep(0.1)