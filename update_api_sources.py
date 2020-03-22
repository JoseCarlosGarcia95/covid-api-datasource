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

def format_data_from_url(url):
    formatted_data = {}

    raw_data = serialize_csv_from_url(url)

    for data in raw_data:
        formatted_one_data = {}

        formatted_one_data['country'] = data['Country/Region']
        del data['Country/Region']

        formatted_one_data['province'] = data['Province/State']
        del data['Province/State']

        del data['Lat']
        del data['Long']

        formatted_one_data['dates'] = {}

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