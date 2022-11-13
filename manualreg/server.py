from flask import Flask, jsonify, make_response
from flask import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def test():
    return ("something")

@app.route("/api", methods=['POST'])
def activate():
    print("Recieved")
    myResponse = make_response('success')
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.status_code = 200
    return myResponse

if __name__ == '__main__':
    app.run(debug = True)