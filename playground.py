import random
import string
import requests
import json
from bs4 import BeautifulSoup

country_url = "http://country.io/names.json"
countries = json.loads(requests.get(country_url).text)

worldometers_url = "https://www.worldometers.info/coronavirus/country/"

population_url = "https://restcountries.eu/rest/v2/alpha/"


def random_country():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'ACCEPT-ENCODING' : 'gzip, deflate, br',
    'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'REFERER' : 'https://www.google.com/'
}
    country_url = "http://country.io/names.json"
    response = requests.get(country_url, headers=headers)
    countries = json.loads(response.text)
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries:
            continue
        else:
            return random_country_code, countries[random_country_code]

print(random_country())

def extract_stats():
    while True:
        country = random_country()[1].replace(" ", "+")
        page = requests.get(worldometers_url + country)
        soup = BeautifulSoup(page.content, "html.parser")
        title = soup.find("title").text
        if "404" in title:
            continue
        else:
            statement = soup.find("li", class_="news_li").text
            new_cases = statement.split(" ")[0]
            return new_cases, statement


print(extract_stats())


def find_population():
    while True:
        country = random_country()
        country_code = country[0]
        response = requests.get(population_url + country_code)
        if response.status_code == "404":
            print("not found")
            continue
        else:
            content = json.loads(response.text)
            population = content["population"]
            return population, country


print(find_population())
