#! venv/bin/python
from flask import Flask, jsonify  # , abort, make_response, request
from flask_cors import CORS

from log import log
from utils import pretty_dumps
from loader import parse_conferences_from_directory

app = Flask(__name__)
CORS(app)

conferences = parse_conferences_from_directory("../conferences")
log.info("Loaded conferences: {conference_ids}".format(
    conference_ids=pretty_dumps(list(conferences.keys()))))

for conference_id, conference in conferences.items():
    print(conference.pretty())


@app.route('/conferences', methods=['GET'])
def get_conferences():
    return jsonify({conf_id: conf.json() for (conf_id, conf) in conferences.items()})

if __name__ == '__main__':
    app.run(debug=True)
