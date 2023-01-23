import json

class Configuration:
    filename = 'cfg.json'

    def __init__(self):
        options = self.getOptions()
        for key, val in options.items():
            setattr(self, key, val)

    def __str__(self):
        options = self.__dict__
        result = 'Configuration:\n'
        for key, val in options.items():
            result += f"{key}: {val}\n"
        return result

    def getOptions(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
        return data['options']

    def saveOptions(self):
        cfg = {"options": self.__dict__}
        data = json.dumps(cfg, indent=4)
        with open(self.filename, 'w') as f:
            f.write(data)

    def changeAttr(self, attr, val):
        setattr(self, attr, val)
        self.saveOptions()

    def getFirstUnworkingDataset(self):
        dataset = self.datasets
        file = ""
        for key, value in dataset.items():
            if not value:
                file = key
                self.datasets[key] = 1
                break
        if file:
            self.saveOptions()
            return file
        return False

    def unmarkDataset(self, datasetName):
        self.datasets[datasetName] = 0
        self.saveOptions()


