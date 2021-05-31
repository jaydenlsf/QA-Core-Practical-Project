from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/get_population')
def get_population():
    while True:
        country = requests.get('http://country_api:5001/get_country').text
        country_code = response.split('-')[0]
        population_url = "https://restcountries.eu/rest/v2/alpha/" + country_code
        response = requests.get(population_url)
        if response.status_code != '200':
            continue
        else:
            population = json.loads(response.text)['population']
            return population
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)