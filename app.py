from flask import Flask, render_template, request
import json
import logging
import urllib.request as req
import urllib.error as err
import redis
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', None)
r = redis.Redis(host=redis_host, 
                port=redis_port, 
                password=redis_password,
                decode_responses=True)

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError('API_KEY environment variable is not set')


def get_weather_service(location):
    endpoint = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}'

    try:
        responce = req.urlopen(endpoint)
        content = responce.read()
        json_data = json.loads(content)

        if json_data and len(json_data) > 0:
            temperature = (int(json_data['days'][0]['temp']) - 32) * 5 / 9

            data = {'city': json_data['resolvedAddress'],
                    'temperature': f'{(temperature):.1f}',
                    'weather': json_data['days'][0]['description'],
                    'humidity': json_data['days'][0]['humidity'],
                    'wind_speed': json_data['days'][0]['windspeed']}
            return data
        else:
            logging.error("Invalid JSON response or missing data")
            return None
    except err.URLError as e:
        logging.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        return None
    except KeyError as e:
        logging.error(f"KeyError: {e} not found in JSON response")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


def get_weather_cache(location):
    if location:
        return r.hgetall(location)
    return None


def store_weather_cache(location, data):
    if data and isinstance(data, dict):
        r.hset(location, mapping=data)
        r.expire(location, 43200)
    else:
        logging.warning(f"No data to store in cache for location: {location}")


@app.route('/', methods=['GET'])
def main():
    template = 'base.html'
    location = request.args.get('city')
    if not location:
        return render_template(template, city=None)
    if location != '':
        data = get_weather_cache(location)
        if not data:
            data = get_weather_service(location)
            store_weather_cache(location, data)
    if data:
        return render_template(template,
                               city=data['city'],
                               temperature=data['temperature'],
                               weather=data['weather'],
                               humidity=data['humidity'],
                               wind_speed=data['wind_speed'])
    else:
        return render_template(template, city=None, err='No weather found.')

if __name__ == '__main__':
    app.run(port=8000, debug=True)