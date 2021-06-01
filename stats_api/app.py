from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_stats', methods=['POST'])
def get_stats():
        country_name = request.data.decode('utf-8')
        url = "https://www.worldometers.info/coronavirus/country/" + country_name
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('title').text
        if '404' in title:
            return f"No data found for {country_name}. Please refresh the page."
        else:
            stat = soup.find('li', class_='news_li').text
            new_cases = stat.split(' ')[0]
            return str(new_cases)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)