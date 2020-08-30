from flask import Flask, jsonify
from github import github_token

import requests
import os
from pprint import pprint
import difflib

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

    # total
    i = 0
    ratios = []
    for l in match:
        j = i + 1
        if j != len(match):
            aux = difflib.SequenceMatcher(None, match[i], match[j])
            ratios.append(aux.ratio())
        
        i += 1

    average = sum(ratios) / len(ratios)
    
    return jsonify(total="{:.2f}".format(average * 100))

if __name__ == '__main__':
    app.run()


