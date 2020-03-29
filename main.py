import requests
from bs4 import BeautifulSoup
import json
from time import strftime, localtime
import os.path
import emoji

INFECTED = 'ЗАРАЖЁННЫЕ'
DEATHS = 'УМЕРЛО'
RECOVERED = 'ИЗЛЕЧИЛОСЬ'

coronavirus = {
    "total_cases": 0,
    "total_deaths": 0,
    "total_recovered": 0,
    "timestamp": ""
}

convert = ''


def load_covid19_from_net():
    global convert
    SITE_URL = 'https://www.worldometers.info/coronavirus/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    page = requests.get(SITE_URL, headers=headers)
    print("Статистика в Мире по COVID-19")
    soup = BeautifulSoup(page.content, 'html.parser')
    convert = soup.findAll("div", {"class": "maincounter-number"})


def show_stats():
    print(
        f'{INFECTED}={coronavirus["total_cases"]}, {DEATHS}={coronavirus["total_deaths"]}, {RECOVERED}={coronavirus["total_recovered"]}')


def show_stats_change():
    print(
        f'{INFECTED}+{coronavirus["total_cases"] - old_cases} '
        f'{DEATHS}+{coronavirus["total_deaths"] - old_deaths} '
        f'{RECOVERED}+{coronavirus["total_recovered"] - old_recovered}')


print(emoji.emojize('Сделано с :blue_heart:'))

if os.path.isfile('covid19.json'):
    with open('covid19.json', 'r') as f:
        coronavirus = json.load(f)

print(f'Прошлая статистика на момент {coronavirus["timestamp"]} ')
show_stats()

load_covid19_from_net()

old_cases = coronavirus["total_cases"]
old_deaths = coronavirus["total_deaths"]
old_recovered = coronavirus["total_recovered"]
coronavirus["total_cases"] = int(convert[0].text.replace(',', ''))
coronavirus["total_deaths"] = int(convert[1].text.replace(',', ''))
coronavirus["total_recovered"] = int(convert[2].text.replace(',', ''))
coronavirus["timestamp"] = strftime("%d.%m.%Y %H:%M:%S", localtime())

print(f'Актуальная статистика на момент {coronavirus["timestamp"]} ')
show_stats()
show_stats_change()

with open('covid19.json', 'w') as f:
    json.dump(coronavirus, f)

os.system('pause')