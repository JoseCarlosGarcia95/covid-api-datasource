#!/usr/bin/python
import io
import csv
import json
import requests
from datetime import datetime

CONFIRMED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
DEATH_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
RECOVERED_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

def read_url(url):
    return requests.get(url).text

def serialize_csv_from_url(url):
    csv_data = read_url(url)
    return list(csv.DictReader(io.StringIO(csv_data)))

def read_country_population_data():
    with open('data/country-by-population-and-density.json', 'r') as country_density_file:
        return json.loads(country_density_file.read())

def get_country_population_data(country, population_data = None):
    if population_data == None:
        population_data = read_country_population_data()

    for country_data in population_data['data']:
        if country_data['name'] == country:
            return {'density': country_data['Density'], 'poblation': country_data['pop2019'], 'area': country_data['area']}

    return None

def format_data_from_url(url):
    formatted_data = {}

    raw_data = serialize_csv_from_url(url)

    population_data = read_country_population_data()

    for data in raw_data:
        formatted_one_data = {}

        formatted_one_data['country'] = data['Country/Region']
        del data['Country/Region']

        formatted_one_data['province'] = data['Province/State']
        del data['Province/State']

        del data['Lat']
        del data['Long']

        formatted_one_data['dates'] = {}
        formatted_one_data['cum_dates'] = {}

        formatted_one_data['country_population_data'] = get_country_population_data(formatted_one_data['country'], population_data=population_data)

        total = 0
        for i in range(0, len(data)):
            date = list(data.keys())[i]
            date_data = list(data.values())[i]

            formatted_date = datetime.strptime(date, '%m/%d/%y')
            timestamp = int(datetime.timestamp(formatted_date))

            previous = 0

            if i != 0:
                previous = int(list(data.values())[i - 1])

            total = int(date_data)
            formatted_one_data['dates'][timestamp] = total - previous
            formatted_one_data['cum_dates'][timestamp] = total

        formatted_one_data['total'] = total
        formatted_data[formatted_one_data['country']] = formatted_one_data

    return formatted_data

confirmed_data = format_data_from_url(CONFIRMED_URL)
with open('data/confirmed.json', 'w') as outfile:
    json.dump(confirmed_data, outfile)

death_data = format_data_from_url(DEATH_URL)
with open('data/death_data.json', 'w') as outfile:
    json.dump(death_data, outfile)

recovered_data = format_data_from_url(RECOVERED_URL)
with open('data/recovered_data.json', 'w') as outfile:
    json.dump(recovered_data, outfile)