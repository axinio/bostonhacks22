from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/")
def test():
    return ("something")

@app.route("/api", methods=['POST'])
def activate():
    print("Receieved")
    Flask.make_response("success", 200)

if __name__ == '__main__':
    app.run(debug = True)