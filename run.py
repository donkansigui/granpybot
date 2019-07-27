from flask import *
from GoogleMapApi import *
from WikipediaApi import *
import logging
logging.basicConfig(level=logging.DEBUG)
import sys

import re
from files.config import STOPWORDS


class Parser():

    def __init__(self):
        pass

    @staticmethod
    def parse_sentence(string):

        result = ''
        if len(string) > 99:
            return result
        words = string.split()
        for word in words:
            try:
                if int(word):
                    if not result:
                        result += word
                    else:
                        result += ' ' + word
            except ValueError:
                if len(word) > 2 and word not in STOPWORDS:
                    # This part is to get ride of apostrophe
                    word = word.split("'")
                    if not result:
                        result += word[-1]
                    else:
                        result += ' ' + word[-1]
        return result

    @staticmethod
    def remove_number(string):

        result = ''
        words = string.split()
        for word in words:
            try:
                int(word)
            except ValueError:
                if not result:
                    result += word
                else:
                    result += ' ' + word
        return result

    @staticmethod
    def remove_titles(string):

        sentence = re.sub("={2}\s.*\s={2}\s", "", string)
        return sentence

app = Flask(__name__)

KEY = 'AIzaSyD0cQkz8eIF7Ph_QAJxppFEX6kz7i2vVTA '


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    parser = Parser()
    question = request.form['question']
    if not question:
        return jsonify({'error':"question vide"})

    rep = parser.parse_sentence(question)
    if not rep:
        return jsonify({'error': "question incompréhensible"})

    google_map = GoogleMapApi(KEY)
    wikipedia = WikipediaApi()
    result = google_map.request_search(rep)

    if not result:
        return jsonify({'error': "impossible de trouver cet endroit"})

    place_id = google_map.request_details(result['place_id'])
    if not place_id:
        return jsonify({'error': "impossible de trouver cet endroit"})
    ret_gmap = google_map.request_map(result['address'],15,"400x400")
    ret_wiki = wikipedia.get_data(result['route'])
    story = parser.remove_titles(ret_wiki['text'])
    return jsonify({'map':ret_gmap.url,'story':story,'address':place_id['address'],'url':ret_wiki['url']})




app.run(debug=True)