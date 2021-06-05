from flask import Flask, request
from flask.json import jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_stats', methods=['POST'])
def get_stats():
        country = request.json['country']
        population = int(request.json['population'].replace(',',''))
        url = "https://www.worldometers.info/coronavirus/country/" + country
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        if response.status_code != 200:
            new_cases = 0
        else:
            try:
                stat = soup.find('li', class_='news_li').text
                new_cases = int(stat.split(' ')[0].replace(',', ''))
            except:
                new_cases = 0
        
        ratio = new_cases /population
        return jsonify({'new_cases': new_cases, 'ratio': ratio})
    

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)