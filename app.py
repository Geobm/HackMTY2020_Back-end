from flask import Flask, jsonify
from flask_cors import CORS

from github import github_token

import requests
import os
import difflib

import nltk
from nltk.tokenize import word_tokenize 
from nltk import FreqDist

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

    # Total
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

@app.route('/user/<username>')
def text_mining(username):
    token = os.getenv('GITHUB_TOKEN', github_token)
    repo_description = []
    repo_name = []
    final_list = []

    query_url = f"https://api.github.com/users/{username}/repos"
    params = {
        "state": "open",
    }
    headers = {'Authorization': f'token {token}'}
    response = requests.get(query_url, headers=headers, params=params)
    result = response.json()

    for i in range(len(result)):
      if result[i]['description'] is not None:
        repo_name.append(result[i]['name'])
        repo_description.append(result[i]['description'])
    final_results = list(zip(repo_name,repo_description))

    tokenized_text = [word for word in nltk.tokenize.word_tokenize(str(repo_description)[1:]) if len(word) > 1]

    fdist = FreqDist(tokenized_text)
    text1 = ''.split(str(tokenized_text))
    fdist1 = nltk.FreqDist(tokenized_text)
    
    return jsonify(data = fdist1.most_common(10))

if __name__ == '__main__':
    app.run()


