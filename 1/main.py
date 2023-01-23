import os
from flask import Flask, request
from werkzeug.datastructures import FileStorage

UPLOAD_FOLDER = r"C:\Users\sznop\Desktop\internet rzeczy\1\pliki"
fileName = 'tekst.txt'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['fileName'] = fileName
# app.secret_key = 'dej5'

@app.route('/file/save', methods=['POST'])
def save():
    name = app.config['fileName']
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return 'OK'

@app.route('/file/read', methods=['GET'])
def load():
    x = request.form['line']
    name = app.config['fileName']
    tmp = ''

    path = UPLOAD_FOLDER + "\\" + name
    with open(path, 'r+', encoding='utf8') as f:
        for i, line in enumerate(f):
            if int(i) == int(x):
                tmp = line
    return tmp

app.run()