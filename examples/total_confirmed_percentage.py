import json
import datetime
import argparse
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-whitegrid')

def read_confirmed():
    with open('../data/confirmed.json', 'r') as confirmed_file:
        return json.loads(confirmed_file.read())
confirmed_data = read_confirmed()

parser = argparse.ArgumentParser(description='Graph total covid 19 data')
parser.add_argument('country', type=str, help='countries')

args = parser.parse_args()

if args.country == 'all':
    countries = confirmed_data.keys()
else:
    countries = args.country.split(',')

for country in countries:
    country_data = confirmed_data[country]

    if country_data['country_population_data'] == None:
        continue
    
    x = []
    y = []

    for date, data in country_data['cum_dates'].items():
        date_obj = datetime.datetime.fromtimestamp(int(date))
        x.append(date_obj)
        y.append(data / (float(country_data['country_population_data']['poblation'])*1000) * 100)

    plt.plot(x,y,label=country)
    plt.gcf().autofmt_xdate()

plt.legend()
plt.show()