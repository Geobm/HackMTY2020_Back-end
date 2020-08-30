from flask import Flask, jsonify
from github import github_token
import requests
import os
from pprint import pprint

app = Flask(__name__)

@app.route('/users/<usernames>')
def analyze_match(usernames):
    return jsonify(data=usernames)

if __name__ == '__main__':
    app.run()


