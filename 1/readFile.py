import requests

req = requests.get('http://127.0.0.1:5000/file/read', data={'line': 6})
print(req.content.decode('utf-8'))
