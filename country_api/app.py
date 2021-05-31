from flask import Flask
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
        if random_country_code not in countries:
            continue
        else:
            return f"{random_country_code}-{countries[random_country_code]}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
