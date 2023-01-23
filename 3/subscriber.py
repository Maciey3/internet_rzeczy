from custom.getCfg import Configuration

import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    # print("Message Received: ", str(message.payload.decode("utf-8")))
    # print(message)
    print("Topic: ", message.topic)

def on_log(client, userdata, level, buf):
    print("log: ", buf)

cfg = Configuration()

client = mqtt.Client('MCH3')
client.on_message=on_message
client.connect(cfg.address)

client.subscribe(cfg.MQTT_topic)
client.loop_forever()

client.disconnect()