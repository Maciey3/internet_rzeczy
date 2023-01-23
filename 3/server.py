from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def recive():
    # print(request.form['json'])
    print('Data recived')
    return 'OK'


app.run()