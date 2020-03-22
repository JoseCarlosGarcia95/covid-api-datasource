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

    x = []
    y = []

    k = 0
    for date, data in country_data['from_startdate'].items():
        date_obj = datetime.datetime.fromtimestamp(int(date))
        x.append(k)
        y.append(data)

        k = k + 1

    plt.plot(x,y,label=country)
    plt.gcf().autofmt_xdate()

plt.legend()
plt.show()