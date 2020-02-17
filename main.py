import requests
import ast
import numpy as np
import time

while True:
    r = requests.get("http://10.5.11.212:8080/sensors.json")

    response_str = r.content.decode("utf-8")
    response = ast.literal_eval(response_str)

    t, gyro = [x[0] for x in response['mag']['data']], [x[1:][0] for x in response['mag']['data']]

    gyro_data = np.array([np.array(xi) for xi in gyro])
    print(gyro_data.shape)

    print(np.max(gyro_data))
    time.sleep(0.1)