import json
import datetime
import random
import urllib3
from urllib.request import urlopen



def writeFile(name):
    with open(name, 'wb+') as f:
        x = 343123
        # f.write(f.to_bytes(1, byteorder='big'))
        f.write(x.to_bytes(10, byteorder='big'))

def readFile(name):
    with open(name, 'rb') as f:
        print(f.readlines())
        for x in f.readlines():
            print(int.from_bytes(x, byteorder='big'))

def readJson(fileName):
    try:
        with open(fileName, encoding='utf-8') as file:
            json_file = json.load(file)
    except FileNotFoundError:
        with open(fileName, 'w+', encoding='utf-8') as file:
            json.dump(json_file := [], file, ensure_ascii=False, indent=4)

    return json_file

def writeJson(fileName):
    json_file = readJson(fileName)
    json_file.append({'data': datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), 'content': random.randint(1, 100002)})

    with open(fileName, 'w+', encoding='utf-8') as file:
        json.dump(json_file, file, ensure_ascii=False, indent=4)

def getJsonHttp(url):
    with urlopen(url) as f:
        resp = json.load(f)
    print(resp)
    resp.sort(key=lambda x: x['id'], reverse=True)
    print(resp)


file1 = 'binary.bin'
file2 = 'test.json'
url = "https://jsonplaceholder.typicode.com/posts"

writeFile(file1)
writeJson(file2)
getJsonHttp(url)
