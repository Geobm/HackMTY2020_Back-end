from flask import Flask, jsonify
from flask_cors import CORS
from github import github_token

import requests
import os
from pprint import pprint
import difflib

app = Flask(__name__)
CORS(app)

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

    # Combinations
    i = 0
    info = []
    for i in range(len(match)):
        if i < len(match):
            j = i + 1
            
            ratios = {}
            user_data = {}

            for j in range(len(match)):
                if names[i] != names[j]:
                    aux = difflib.SequenceMatcher(None, match[i], match[j])
                    ratios[names[j]] = aux.ratio()

                j += 1

            maximum = max(ratios.values())

            keys = list(ratios.keys())
            values = list(ratios.values())

            person = keys[values.index(maximum)]

            user_data['user_name'] = names[i]
            user_data['person'] = person
            user_data['ratio'] = "{:.2f}".format(maximum * 100)

            query_url = f"https://api.github.com/users/{names[i]}/repos"
            params = {
                "state": "open",
            }
            headers = {'Authorization': f'token {token}'}
            response = requests.get(query_url, headers=headers, params=params)
            result = response.json()

            if result:
                user_data['avatar'] = result[0]['owner']['avatar_url']
            else:
                user_data['avatar'] = None

            info.append(user_data)
    
    return jsonify(total="{:.2f}".format(average * 100), combinations=info)

if __name__ == '__main__':
    app.run()


