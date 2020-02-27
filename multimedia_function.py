import requests
from PIL import Image
import io

IP = "192.168.0.7"
def take_shots(save_path):
    ip = "http://"+IP+":8080/shot.jpg"
    r = requests.get(ip)
    image = Image.open(io.BytesIO(r.content))
    image.save(save_path)


def record_audio(save_path):
    ip = "http://" + IP + ":8080/audio.wav"
    r = requests.get(ip, stream=True)
    objmp3 = io.BytesIO(r.content)


def enable_torch():
    ip = "http://" + IP + ":8080/enabletorch"
    r = requests.get(ip)

def disable_torch():
    ip = "http://" + IP + ":8080/disabletorch"
    r = requests.get(ip)

def zoom(X):
    ip = "http://"+IP+":8080/ptz?zoom="+str(X)
    try:
        r = requests.get(ip)
        return True
    except:
        return False

if __name__ == "__main__":
    #take_shots("image.jpg")
    record_audio("")