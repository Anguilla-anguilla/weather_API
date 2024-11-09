from flask import Flask, render_template, request
import json
import urllib.error as err
import urllib.request as req
import redis
from constants import API_KEY

app = Flask(__name__)


def get_weather_service(location):
    endpoint = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={API_KEY}'

    responce = req.urlopen(endpoint)
    content = responce.read()
    json_data = json.loads(content)
    
    if len(json_data) > 0:
        city = json_data['resolvedAddress']
        temperature = (int(json_data['days'][0]['temp']) - 32) * 5 / 9
        weather = json_data['days'][0]['description']
        humidity = json_data['days'][0]['humidity']
        wind_speed = json_data['days'][0]['windspeed']
    
    return city


def get_weather_cache():
    pass

@app.route('/', methods=['GET'])
def main():
    template = 'base.html'
    if request.method == 'GET':
        location = request.args.get('city')
        print(location)
        city = get_weather_service(location)
    else:
        city = 'No city'
    temperature = '8'
    weather = 'Cloudy'
    humidity = '40'
    wind_speed = '16'

    return render_template(template, 
                           city=city,
                           temperature=temperature,
                           weather=weather,
                           humidity=humidity,
                           wind_speed=wind_speed)


if __name__ == '__main__':
    app.run(port=8000, debug=True)