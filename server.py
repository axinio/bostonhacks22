from flask import Flask, jsonify, make_response,render_template
from flask import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api", methods=['POST'])
def activate():
    print("Recieved")
    myResponse = make_response('success')
    myResponse.headers['customHeader'] = 'This is a custom header'
    myResponse.status_code = 200
    return myResponse

if __name__ == '__main__':
    app.run(host="0.0.0.0",port = '8080')