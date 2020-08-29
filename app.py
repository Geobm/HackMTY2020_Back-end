from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def say_hello():
    return jsonify(data="Hello World")


if __name__ == '__main__':
    app.run()