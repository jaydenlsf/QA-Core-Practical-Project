from flask import Flask
import requests
from bs4 import beautifulsoup

app = Flask(__name__)

@app.route('/get_stat')
def get_stat():
    while True:
        country = requests.get('http://country_api:5001/get_country').text
        country_name = response.split('-')[1].replace(' ', '+')
        page = requests.get("https://www.worldometers.info/coronavirus/country/" + country_name)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('title').text
        if '404' in title:
            continue
        else:
            stat = soup.find('li', class_='news_li').text
            new_cases = stat.split(' ')[0]
            return new_cases

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)