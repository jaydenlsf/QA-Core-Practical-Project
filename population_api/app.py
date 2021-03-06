from flask import Flask, request
from flask.json import jsonify
import requests
import json

app = Flask(__name__)

@app.route('/get_population', methods=['POST'])
def get_population():
    country_code = request.data.decode('utf-8')
    population_url = "https://restcountries.eu/rest/v2/alpha/" + country_code
    response = requests.get(population_url)
    if response.status_code != 200: return str(response.status_code)
    else:
        population = json.loads(response.text)['population']
        alpha3code = json.loads(response.text)['alpha3Code']
        return jsonify({'population': f"{population:,d}", 'alpha3code': alpha3code})

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)