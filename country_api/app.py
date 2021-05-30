from flask import Flask
import random
import string
import requests
import json

app = Flask(__name__)


@app.route("/")
@app.route("/get_country", methods=["GET"])
def get_country_code():
    country_url = "http://country.io/names.json"
    countries = json.loads(requests.get(country_url).text)
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries:
            continue
        else:
            return random_country_code, countries[random_country_code]


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
