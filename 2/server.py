from flask import Flask, request
import json

app = Flask(__name__)

UPLOAD_FOLDER = r"C:/Users/sznop/Desktop/internet rzeczy/2/serverData"
fileName = 'data.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['fileName'] = fileName

@app.route('/json/send', methods=['POST'])
def sendJson():
    def wczytaj_wpisy(file_name):
        try:
            with open(file_name, encoding='utf-8') as file:
                json_file = json.load(file)
        except FileNotFoundError:
            with open(file_name, 'w+', encoding='utf-8') as file:
                json.dump(json_file := [], file, ensure_ascii=False, indent=4)

        return json_file

    def zapisz_wpis(data):
        filePath = f"{UPLOAD_FOLDER}/{fileName}"
        json_file = wczytaj_wpisy(filePath)
        json_file.append(json.loads(data))

        with open(filePath, 'w', encoding='utf-8') as file:
            json.dump(json_file, file, ensure_ascii=False, indent=4)

    recivedJson = request.form['json']
    zapisz_wpis(recivedJson)

    return 'OK'

@app.route('/json/get', methods=['GET'])
def getJson():
    def wczytaj_wpisy(file_name):
        try:
            with open(file_name, encoding='utf-8') as file:
                json_file = json.load(file)
        except FileNotFoundError:
            with open(file_name, 'w+', encoding='utf-8') as file:
                json.dump(json_file := [], file, ensure_ascii=False, indent=4)

        return json_file


    filePath = f"{UPLOAD_FOLDER}/{fileName}"
    return wczytaj_wpisy(filePath)
app.run()