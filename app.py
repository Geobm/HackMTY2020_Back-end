from flask import Flask, jsonify

from token import github_token

import requests
import os
from pprint import pprint

app = Flask(__name__)

@app.route('/users/<usernames>')
def analyze_match(usernames):
    token = os.getenv('GITHUB_TOKEN', github_token)

    result = []

    for username in usernames:
        query_url = f"https://api.github.com/users/{username}/repos"
        params = {
            "state": "open",
        }
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url, headers=headers, params=params)
        x = (r.json())

        y = []
        for i in range(len(x)):
            if x[i]["language"] is not None:
                y.append(x[i]["language"])
        
        result.append(y)

    return jsonify(data=result)


if __name__ == '__main__':
    app.run()