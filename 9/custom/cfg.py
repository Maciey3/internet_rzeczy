import json
import datetime

class Configuration:
    def __init__(self, status, port):
        self.history = {}
        self.status = status
        self.port = port

    def __str__(self):
        options = self.__dict__
        result = 'Configuration:\n'
        for key, val in options.items():
            result += f"{key}: {val}\n"
        return result

    @classmethod
    def reload(cls, id):
        database = cls.getDatabase()
        cfg = database[str(id)]
        return cls(cfg, status=cfg['status'], port=cfg['port'])

    @classmethod
    def getDatabase(cls):
        with open(cls.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @classmethod
    def getCfgById(cls, id):
        return cls.reload(id)

    def getLastId(self):
        if data := self.getDatabase():
            return int(sorted(data)[-1])
        return 0

    @classmethod
    def save(cls, args, id=None):
        if not id:
            id = cls.getLastId(cls)+1
        cfg = {id: cls(args).__dict__}
        database = cls.getDatabase()
        data = json.dumps({**database, **cfg}, indent=4, ensure_ascii=False)

        with open(cls.filename, 'w', encoding='utf-8') as f:
            f.write(data)
        return id

    def delete(self, id):
        database = self.getDatabase()
        del database[id]

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)

    def insertPort(self, id, port):
        self.update(id=id, updatePort=port)

    def deletePort(self, id):
        self.update(id=id, updatePort=-1)

    def addElementToHistory(self, data):
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        if date in self.history:
            self.history[date].append(data)
        else:
            self.history[date] = [data]


class Generator(Configuration):
    filename = 'database/generators.json'

    def __init__(self, args, status=False, port=""):
        super().__init__(status, port)
        self.request = args['request']
        self.title = args['title']
        self.address = args['address']
        self.send_frequency = args['send_frequency']
        self.MQTT_topic = args['MQTT_topic']
        self.dataset = args['dataset']

    def update(self, id, updateStatus=False, updateArgs=False, updatePort=False):
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
        elif updatePort:
            if updatePort == -1:
                database[id]['port'] = ''
            else:
                database[id]['port'] = updatePort

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)

        self.__init__(self.getCfgById(id).__dict__, status=database[id]['status'])

class Aggregator(Configuration):
    filename = 'database/aggregators.json'

    def __init__(self, args, status=False, port=""):
        super().__init__(status, port)
        self.title = args['title']
        self.address = args['address']
        self.send_frequency = args['send_frequency']
        self.destination_form = args['destination_form']

    def update(self, id, updateStatus=False, updateArgs=False, updatePort=False):
        database = self.getDatabase()

        if updateStatus:
            status = database[id]['status']
            database[id]['status'] = not status
        elif updateArgs:
            database[id]['title'] = updateArgs['title']
            database[id]['address'] = updateArgs['address']
            database[id]['send_frequency'] = updateArgs['send_frequency']
            database[id]['destination_form'] = updateArgs['destination_form']
        elif updatePort:
            if updatePort == -1:
                database[id]['port'] = ''
            else:
                database[id]['port'] = updatePort

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)

        self.__init__(self.getCfgById(id).__dict__, status=database[id]['status'])


class Filter(Configuration):
    filename = 'database/filters.json'

    def __init__(self, args, status=False, port=""):
        super().__init__(status, port)
        self.title = args['title']
        self.address = args['address']
        self.filter_target = args['filter_target']

    def update(self, id, updateStatus=False, updateArgs=False, updatePort=False):
        database = self.getDatabase()

        if updateStatus:
            status = database[id]['status']
            database[id]['status'] = not status
        elif updateArgs:
            database[id]['title'] = updateArgs['title']
            database[id]['address'] = updateArgs['address']
            database[id]['filter_target'] = updateArgs['filter_target']
        elif updatePort:
            if updatePort == -1:
                database[id]['port'] = ''
            else:
                database[id]['port'] = updatePort

        data = json.dumps(database, indent=4, ensure_ascii=False)
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(data)

        self.__init__(self.getCfgById(id).__dict__, status=database[id]['status'])
