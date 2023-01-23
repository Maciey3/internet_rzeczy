import paho.mqtt.client as mqtt
import datetime
import requests
import GPUtil
import time



def on_publish(client, userdata, message):
    print("Data published\n")

client = mqtt.Client('myId1')
client.on_publish = on_publish

def interval(client):
    temperatures = []
    while True:
        temp = GPUtil.getGPUs()[0].temperature
        if not len(temperatures):
            message = temp
            client.connect('test.mosquitto.org')
            client.publish('For test x32', f"{message}|{datetime.datetime.now()}")
            client.disconnect()

            temperatures.append(temp)
            time.sleep(3)
            print(temperatures)
            continue
        if temp != temperatures[-1]:
            message = temp
            client.connect('test.mosquitto.org')
            client.publish('For test x32', f"{message}|{datetime.datetime.now()}")
            client.disconnect()

        temperatures.append(temp)
        time.sleep(3)
        print(temperatures)

interval(client)

# print(requests.get('http://127.0.0.1:5000/json/get').text)




