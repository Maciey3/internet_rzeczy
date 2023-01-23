import json

class Configuration:
    filename = 'database/database.json'

    def __init__(self, args, status=False):
        self.request = args['request']
        self.title = args['title']
        self.address = args['address']
        self.send_frequency = args['send_frequency']
        self.MQTT_topic = args['MQTT_topic']
        self.dataset = args['dataset']
        self.status = status

    def __str__(self):
        options = self.__dict__
        result = 'Configuration:\n'
        for key, val in options.items():
            result += f"{key}: {val}\n"
        return result

    def reload(self, id):
        database = self.getDatabase()
        cfg = database[str(id)]
        params = {
            'request': cfg['request'],
            'title': cfg['title'],
            'address': cfg['address'],
            'send_frequency': cfg['send_frequency'],
            'MQTT_topic': cfg['MQTT_topic'],
            'dataset': cfg['dataset']
        }
        self.__init__(params, status=cfg['status'])

    def getDatabase(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def getLastId(self):
        if data := self.getDatabase():
            return int(sorted(data)[-1])
        return 0

    def getCfgById(self, id):
        self.reload(id)

    def save(self, id=None):
        if not id:
            id = self.getLastId()+1
        cfg = {id: self.__dict__}
        database = self.getDatabase()
        data = json.dumps({**database, **cfg}, indent=4, ensure_ascii=False)

        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)
        return id

    def update(self, id, updateStatus=False, updateArgs=False):
        database = self.getDatabase()
        if updateStatus:
            status = database[id]['status']
            database[id]['status'] = not status
        if updateArgs:
            database[id]['request'] = updateArgs['request']
            database[id]['title'] = updateArgs['title']
            database[id]['address'] = updateArgs['address']
            database[id]['send_frequency'] = updateArgs['send_frequency']
            database[id]['MQTT_topic'] = updateArgs['MQTT_topic']
            database[id]['dataset'] = updateArgs['dataset']

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)

        self.reload(id)

    def delete(self, id):
        database = self.getDatabase()
        del database[id]

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)