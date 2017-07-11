import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

import requests


def get_liitynta_katalogi_data():
    organization_dict = {}

    for i in range(1, 4):

        url = 'https://liityntakatalogi.suomi.fi/organization?q=&sort=title+asc&page={}'.format(
            i)
        print(url)
        data = requests.get(url).text

        parse_data(data, organization_dict)

    with open('data/json/liitynta_katalogi/organizations.json', 'w') as outfile:
        json.dump(organization_dict, outfile)


def parse_data(file, organization_dict):
    soup = BeautifulSoup(file, 'html.parser')

    organizations = soup.find_all('li', {'class': 'kapa-item'})
    print(len(organizations))
    for org in organizations:
        name = org.find('strong')
        name = name.contents[0]
        try:
            count = org.find('strong', {'class': 'count'})
            count = count.contents[0]
            count = [int(s) for s in count.split() if s.isdigit()][0]
        except AttributeError:
            count = 0

        organization_dict[name] = count


def get_html_from_file():
    with open('data/html/liitynta_katalogi_sample.html', 'r') as file:
        return file.read()
