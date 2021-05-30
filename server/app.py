from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    country_code = requests.get("http://country_api:5000/get_country_code")
    return render_template("index.html", country_code=country_code)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
