import requests

url = 'https://api.darksky.net/forecast/8cf0d9b4c83a4030bfaf2c73491334cf/48.1651,17.1457?units=auto'

r = requests.get(url.format()).json()

weather = {
    'temperature' : r['currently']['temperature'],
    'summary' : r['currently']['summary'],
    'icon' : r['currently']['icon']
}

print(weather)