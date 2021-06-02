from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@34.105.152.58/covid_19_app'
db = SQLAlchemy(app)

class CovidStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(30), nullable=False)
    country_name = db.Column(db.String(60), nullable=False)
    population = db.Column(db.String(30))
    new_cases = db.Column(db.String(30))


@app.route("/")
@app.route("/home")
def home():
    country_response = requests.get("http://country_api:5000/get_country").text
    country_code = country_response.split('-')[0]
    country_name = country_response.split('-')[1]
    country_name_adjusted = country_name.replace(' ', '-')

    population = requests.post("http://population_api:5000/get_population", data=country_code).text
    
    if country_code == 'UK' or country_code == 'US':
        new_cases = requests.post('http://stats_api:5000/get_stats', data=country_code).text
    else:
        new_cases = requests.post('http://stats_api:5000/get_stats', data=country_name_adjusted).text

    if len(new_cases) > 6:
        return redirect(url_for('home'))

    new_country_stats = CovidStats(
        country_code=country_code,
        country_name=country_name,
        population=population,
        new_cases=new_cases
    )
    db.session.add(new_country_stats)
    db.session.commit()

    return render_template("index.html", country_code=country_code, country_name=country_name, population=population, new_cases=new_cases)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
