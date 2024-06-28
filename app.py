from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/api/hello")
def greeting():
    visitor_name = request.args.get("visitor_name", default='Guest', type=str)
    response = {
        "client_ip": request.remote_addr,
        "greeting": "Hello, {}!".format(visitor_name.strip('"'))
    }
    return jsonify(response)

@app.route("/")
def index():
    return jsonify({
        "Message": "Welcome to Home Page"
    })

if __name__ == '__main__':
    app.run()