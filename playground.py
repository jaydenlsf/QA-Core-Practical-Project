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
    letters = string.ascii_uppercase
    while True:
        random_country_code = "".join(random.choice(letters) for i in range(2))
        if random_country_code not in countries:
            continue
        else:
            return random_country_code, countries[random_country_code]


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
