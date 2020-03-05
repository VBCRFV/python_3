from flask import Flask, abort
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1")
def error():
    abort(502)

if __name__ == "__main__":
    app.run(port=443)
    #app.run(host='0.0.0.0') # todo слушать на всех ip (интерфейсах).