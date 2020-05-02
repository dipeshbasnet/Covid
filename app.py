from flask import Flask, render_template
import requests

from constants import DEVA_DICT, STAT_DATA
from env import RAPID_API_KEY

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


def convert_to_devanagari_num(_num):
    num = ""
    for n in str(_num):
        num = num + DEVA_DICT.get(n)
    return num


@app.route('/')
def home():
    url = "https://covid-19-data.p.rapidapi.com/country/all"

    querystring = {"format": "json"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return render_template("home.html", countries=response.json())


@app.route('/nepal/')
def nepal():
    url = "https://covid-19-data.p.rapidapi.com/report/country/name"

    querystring = {"date-format": "YYYY-MM-DD", "format": "json", "date": "2020-04-01", "name": "Nepal"}

    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    _data = response.json()[0]['provinces'][0]
    data = {}
    for stat in STAT_DATA:
        data[stat] = convert_to_devanagari_num(_data[stat])
    return render_template("nepal.html", data=data)


if __name__ == '__main__':
    app.run()