# Weather API

A simple Flask-based web application that fetches and displays weather data for a given location. The application uses the [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api) to retrieve weather information and caches the data using Redis to reduce API calls.

#### Features
- **Weather Data Retrieval**: Fetches current weather data for a specified location.
- **Caching**: Caches weather data in Redis to reduce API calls and improve performance.

#### Prerequisites
- **Python 3.6** or higher
- **Visual Crossing Weather API Key**: Required to fetch weather data.

#### Installation
1. Clone the repository:
```
git clone https://github.com/Anguilla-anguilla/weather_API.git
cd weather_API
```
2. Set up a virtual environment:
```
python3 -m venv venv
source venv/Scripts/activate
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Set up environment variables:
Create a `.env` file in the root directory of the project. Add the following environment variables to the `.env` file:

```
API_KEY=your_visual_crossing_api_key_here
REDIS_HOST=localhost # Optional
REDIS_PORT=your_redis_port # Optional
REDIS_PASSWORD=your_redis_password_here # Optional
```

#### Running the Application
1. Start the Redis server:
Ensure Redis is installed and running on your machine. You can start the Redis server with:
```
redis-server
```
2. Run the Flask application:
```
python app.py
```
3. Access the application:
Open your web browser and go to `http://127.0.0.1:8000/`.

#### Usage
- **Form**: The form allows you to enter a city name to fetch the weather data.
- **Weather Data**: The application displays the current temperature, weather description, humidity, and wind speed for the specified city.
- **Caching**: The weather data is cached in Redis for 12 hours to reduce API calls.

[Project URL](https://roadmap.sh/projects/weather-api-wrapper-service)