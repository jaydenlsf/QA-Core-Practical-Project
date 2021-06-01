from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    country_response = requests.get("http://country_api:5001/get_country").text
    country_code = country_response.split('-')[0]
    country_name = country_response.split('-')[1]
    country_name_adjusted = country_name.replace(' ', '-')

    population = requests.post("http://population_api:5001/get_population", data=country_code).text
    
    if country_code == 'UK' or country_code == 'US':
        stats = requests.post('http://stats_api:5001/get_stats', data=country_code).text
    else:
        stats = requests.post('http://stats_api:5001/get_stats', data=country_name_adjusted).text

    return render_template("index.html", country_code=country_code, country_name=country_name, population=population, stats=stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
