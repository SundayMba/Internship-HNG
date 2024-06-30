from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/api/hello")
def greeting():
    # Get client IP address, considering proxies and load balancers
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        client_ip = request.remote_addr
    visitor_name = request.args.get("visitor_name", default='Guest', type=str)
    client_info = get_client_city(client_ip)
    city = client_info.get("city")
    lat = client_info.get("lat")
    lon = client_info.get('lon')
    weather_info = get_temp(lon, lat)
    temp = weather_info['main']['temp']
    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": "Hello, {}!, the temperature is {} degree celcius in {}.".format(visitor_name.strip('"'), int(temp), city)
    }
    return jsonify(response)

@app.route("/")
def index():
    return jsonify({
        "Message": "Welcome to Home Page"
    })

def get_client_city(ip_address):
    url = f"https://ipinfo.io/{ip_address}"
    params = {
        "token": "6a11f15ed06812"
    }
    try:
        response = requests.get(url, params).json()
        city = response.get("city", "Aba")
        axis = response.get('loc').split(",")
        longitude = axis[0]
        latitude  = axis[1]
        
        data = {
            "city": city,
            "lon": longitude,
            "lat": latitude
            }
        return data
    except:
        pass

def get_temp(longitude, latitude):
    WEATHER_API_KEY = 'a4db38eb81b0c028caca64dafd8ffb89'
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None
