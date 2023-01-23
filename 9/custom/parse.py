from argparse import ArgumentParser

def parse(empty=False):
    items = ['request', 'title', 'address', 'send_frequency', 'MQTT_topic', 'dataset']
    tmp = {}
    if empty:
        for item in items:
            tmp[item] = ""
    else:
        parser = ArgumentParser()
        for item in items:
            parser.add_argument(item, type=str)
        args = parser.parse_args()
        for item in items:
            tmp[item] = getattr(args, item)

    return tmp