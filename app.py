from flask import Flask, render_template, request
import json
import urllib.error as err
import urllib.request as req
import redis
from constants import API_KEY

app = Flask(__name__)
r = redis.Redis()


def get_weather_service(location):
    endpoint = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={API_KEY}'

    responce = req.urlopen(endpoint)
    content = responce.read()
    json_data = json.loads(content)

    if len(json_data) > 0:
        data = {'city': json_data['resolvedAddress']   ,
                'temperature': (int(json_data['days'][0]['temp']) - 32) * 5 / 9,
                'weather': json_data['days'][0]['description'],
                'humidity': json_data['days'][0]['humidity'],
                'wind_speed': json_data['days'][0]['windspeed']}
        return data


def get_weather_cache(location):
    if location:
        hash = r.hgetall(location)
        data = {key.decode('utf-8'): value.decode('utf-8') 
                for key, value in hash.items()}
        return data


def store_weather_cache(location, data):
    # ex = 43200
    r.hset(location, mapping=data)
    r.expire(location, 60)
    r.close()


@app.route('/', methods=['GET'])
def main():
    template = 'base.html'
    location = request.args.get('city')
    if not location:
        return render_template(template, city=None)
    if location != '':
        data = get_weather_cache(location)
        r.close()
        print('get from cache')
        print(data)
        if not data:
            data = get_weather_service(location)
            store_weather_cache(location, data)
            print('store in cache')
    if data:
        print('DATA!')
        return render_template(template,
                               city=data['city'],
                               temperature=data['temperature'],
                               weather=data['weather'],
                               humidity=data['humidity'],
                               wind_speed=data['wind_speed'])
    else:
        print('NO DATA')
        return render_template(template, city=None, err='No weather found.')

if __name__ == '__main__':
    app.run(port=8000, debug=True)