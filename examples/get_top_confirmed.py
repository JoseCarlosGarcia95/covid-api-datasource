import json

def read_confirmed():
    with open('../data/confirmed.json', 'r') as confirmed_file:
        return json.loads(confirmed_file.read())


confirmed_data = read_confirmed().values()

confirmed_sort = sorted(confirmed_data, key=lambda x: x['total'], reverse=True)
confirmed_sort = confirmed_sort[0:10]

k = 0
for country in confirmed_sort:
    poblation = 0
    if country['country_population_data'] != None:
        poblation = float(country['country_population_data']['poblation']) * 1000
    k = k + 1
    print("#{} Country={} Poblation={} Confirmed={}".format(k, country['country'], poblation, country['total']))