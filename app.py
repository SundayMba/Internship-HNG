from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/api/hello")
def greeting():
    # Get client IP address, considering proxies and load balancers
    # if request.headers.getlist("X-Forwarded-For"):
    #     client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    # else:
    client_ip = request.remote_addr
    visitor_name = request.args.get("visitor_name", default='Guest', type=str)
    response = {
        "client_ip": client_ip,
        "location": get_client_city(client_ip),
        "greeting": "Hello, {}!, the temperature is 11 degrees celcius in new York.".format(visitor_name.strip('"'))
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
        city = response.get("city")
    except:
        city = "california"
    return response
