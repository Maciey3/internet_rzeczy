import requests

files = {'file': open('tekst.txt', 'r', encoding='utf8')}
req = requests.post('http://127.0.0.1:5000/file/save', files=files)
print(req.content.decode('utf-8'))

