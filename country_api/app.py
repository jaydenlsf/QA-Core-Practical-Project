from flask import Flask
from flask.json import jsonify
import random
import string
import requests
import json

app = Flask(__name__)


@app.route("/get_country", methods=["GET"])
def get_country():
    country_url = "http://country.io/names.json"
    response = requests.get(country_url)
    countries = json.loads(response.text)
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries: continue
        else:
            return jsonify({'country_code': random_country_code, 'country_name': countries[random_country_code]})


if __name__ == "__main__": app.run(host="0.0.0.0", port=5000, debug=True)