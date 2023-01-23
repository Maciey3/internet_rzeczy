import threading
import requests

from custom.cfg import Configuration
from custom.parse import parse
from custom.customThread import customThread

from flask import Flask, request, render_template, url_for, redirect



app = Flask(__name__)

@app.route('/')
def index():
    cfg = Configuration(parse(empty=True))
    database = cfg.getDatabase()

    return render_template('index.html', database=database)

@app.route('/show/<id>')
def show(id):
    cfg = Configuration(parse(True))
    cfg.getCfgById(id)

    return render_template('show.html', cfg=cfg.__dict__, id=id)

@app.route('/activate/<id>', methods=['GET'])
def activate(id):
    cfg = Configuration(parse(True))
    cfg.getCfgById(id)
    cfg.update(id, updateStatus=True)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/start/{id}')
    else:
        requests.post(f'http://127.0.0.1:8000/stop/{id}')

    return redirect(url_for('index'))

@app.route('/receive', methods=['POST'])
def receive():
    print('Data received')
    return 'Data received'

@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    cfg = Configuration(parse(True))
    cfg.getCfgById(id)
    cfg.delete(id)

    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/edit/<id>')
def edit(id):
    cfg = Configuration(parse(empty=True))
    cfg.getCfgById(id)

    datasets = [
        'beach-water-quality-automated-sensors-1.csv',
        'Dollar-billionaires-per-million-people.csv',
        'earnings.csv',
        'surnames_en.csv',
        'zip-code-breakdowns-1.csv'
    ]

    return render_template('edit.html', cfg=cfg.__dict__, datasets=datasets, id=id)

@app.route('/update/', methods=['POST'])
def update():
    id = request.form['id']
    args = {
        'request': request.form['request'],
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'MQTT_topic': request.form['MQTT_topic'],
        'dataset': request.form['dataset']
    }


    cfg = Configuration(parse(empty=True))
    cfg.getCfgById(id)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/stop/{id}')

    cfg.update(id, updateArgs=args)

    if cfg.status:
        requests.post(f'http://127.0.0.1:8000/start/{id}')

    return redirect(url_for('index'))

@app.route('/addObject', methods=["POST"])
def addObject():
    args = {
        'request': request.form['request'],
        'title': request.form['title'],
        'address': request.form['address'],
        'send_frequency': request.form['send_frequency'],
        'MQTT_topic': request.form['MQTT_topic'],
        'dataset': request.form['dataset']
    }

    cfg = Configuration(args=args)
    cfg.save()

    return redirect(url_for('index'))


app.run(debug=True)