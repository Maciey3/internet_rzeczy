import csv
import json

class csvToJson:
    def convertToJson(self):
        jsonArray = []
        with open(self.datasetName, 'r+') as f:
            csvReader = csv.DictReader(f)
            for row in csvReader:
                jsonArray.append(row)

        return json.dumps(jsonArray, indent=4)

    def dataInCsv(self):
        with open(self.datasetName, 'r+') as f:
            return f.read()

    def __init__(self, datasetName):
        self.datasetName = 'datasets/'+datasetName
        self.dataInCsv = self.dataInCsv()
        self.dataInJson = self.convertToJson()

