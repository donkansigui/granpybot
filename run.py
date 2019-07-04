from flask import *
from parser import *
from GoogleMapApi import *
from WikipediaApi import *
app = Flask(__name__)

KEY = 'AIzaSyAefulviC3pPj_Sjjtj53Y8WpPNjDDDqsY'

@app.route('/')
def hello_world():
    return render_template('index.html')

app.run()

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