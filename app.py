from flask import Flask, jsonify
from github import github_token

import requests
import os
from pprint import pprint

app = Flask(__name__)

@app.route('/users/<usernames>')
def analyze_match(usernames):
    token = os.getenv('GITHUB_TOKEN', github_token)

    names = usernames.split(',')

    match = []
    for name in names:
        query_url = f"https://api.github.com/users/{name}/repos"
        params = {
            "state": "open",
        }
        headers = {'Authorization': f'token {token}'}
        response = requests.get(query_url, headers=headers, params=params)
        result = response.json()
    
        languages = []
        for i in range(len(result)):
            if result[i]["language"] is not None:
                languages.append(result[i]["language"])

        match.append(languages)
 
    return jsonify(data=match)

if __name__ == '__main__':
    app.run()


