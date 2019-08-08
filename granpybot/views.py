from flask import *
from granpybot.objects.wikipedia_api import WikipediaApi
import logging
from .objects.parser import Parser
from .objects.google_map_api import GoogleMapApi
from .stopwords.config import GMAK

logging.basicConfig(level=logging.DEBUG)

import re
from granpybot.stopwords.config import STOPWORDS



app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

# import flask

@app.route('/process', methods=['POST'])
def process():
    parser = Parser()
    question = request.form['question']
    if not question:
        return jsonify({'error':"question vide"})

    rep = parser.parse_sentence(question)
    if not rep:
        return jsonify({'error': "question incompréhensible"})

    google_map = GoogleMapApi(GMAK)
    wikipedia = WikipediaApi()
    result = google_map.request_search(rep)

    if not result:
        return jsonify({'error': "impossible de trouver cet endroit"})

    place_id = google_map.request_details(result['place_id'])
    if not place_id:
        return jsonify({'error': "impossible de trouver cet endroit"})
    ret_gmap = google_map.request_map(place_id['address'],15,"400x400")
    ret_wiki = wikipedia.get_data(place_id['address'])
    story = parser.remove_titles(ret_wiki['text'])
    return jsonify({'map':ret_gmap.url,'story':story,'address':place_id['address'],'url':ret_wiki['url']})

