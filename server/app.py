from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    country_response = requests.get("http://country_api:5001/get_country").text
    country_code = country_response.split('-')[0]
    country_name = country_response.split('-')[1]

    population_response = requests.get("http://population_api:5001/get_population").text
    return render_template("index.html", country_code=country_code, country_name=country_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
