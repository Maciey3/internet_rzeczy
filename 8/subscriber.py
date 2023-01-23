import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    # print("Message Received: ", str(message.payload.decode("utf-8")))
    # print(message)
    print("Topic: ", message.topic)

def on_log(client, userdata, level, buf):
    print("log: ", buf)


client = mqtt.Client('MCH3')
client.on_message=on_message
client.connect('test.mosquitto.org')

client.subscribe('For test x32')
client.loop_forever()

client.disconnect()