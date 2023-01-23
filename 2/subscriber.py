import paho.mqtt.client as mqtt
import requests
import json


def sendJson(customMessage):
    data, date = customMessage.split('|')
    tmp = {
        'message': data,
        'date': date
    }
    if requests.post('http://127.0.0.1:5000/json/send', data={'json': json.dumps(tmp)}):
        return True


def on_message(client, userdata, message):
    print("Message Received: ", str(message.payload.decode("utf-8")))
    print("Topic: ", message.topic)
    print()
    if sendJson(str(message.payload.decode("utf-8"))): print('JSON send to the server')
    else: print('There was problem with the local server')

def on_log(client, userdata, level, buf):
    print("log: ", buf)


client = mqtt.Client('myId2')
client.on_message=on_message
client.connect('test.mosquitto.org')

client.subscribe("For test x32")
client.loop_forever()

client.disconnect()