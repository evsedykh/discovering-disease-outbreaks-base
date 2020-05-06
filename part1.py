import re
import geonamescache
import pandas as pd
from unidecode import unidecode
from operator import itemgetter

headlines_file = open('data/headlines.txt')
# headlines_file = open('data/problematic.txt')
headlines = headlines_file.read().splitlines()
headlines_file.close()

gc = geonamescache.GeonamesCache()
cities = gc.get_cities()
ascii_cities = [city['geonameid'] for city in cities.values() if city['name'] == unidecode(city['name'])]
names = {cities[str(id)]['name']: cities[str(id)]['geonameid'] for id in ascii_cities}
accented_cities = [city['geonameid'] for city in cities.values() if city['name'] != unidecode(city['name'])]
alternative_names = {unidecode(cities[str(id)]['name']): cities[str(id)]['geonameid'] for id in accented_cities}
names.update(alternative_names)
alternative_names = {unidecode(cities[str(id)]['name']): cities[str(id)]['name'] for id in accented_cities}

sorted_by_len = list(names.keys())
sorted_by_len.sort(key=lambda s: len(s), reverse=True)
giant_cities_regex = ''
for city in sorted_by_len:
    giant_cities_regex += f'\\b{city}\\b|'
giant_cities_regex = giant_cities_regex[:-1]
cities_cre = re.compile(giant_cities_regex, re.ASCII)

cities_in_headings = {}
for headline in headlines:
    found = re.search(cities_cre, headline)
    if found:
        cities_in_headings[headline] = found.group()

df = pd.DataFrame(columns=['Heading', 'City', 'Country code'])
for i, headline in enumerate(cities_in_headings):
    city_candidate = cities_in_headings[headline]
    cities_list = gc.get_cities_by_name(city_candidate)
    if not cities_list:
        cities_list = gc.get_cities_by_name(alternative_names[city_candidate])
    sorted_by_population = []
    for city in cities_list:
        sorted_by_population.append((int(list(city.keys())[0]), list(city.values())[0]['population']))
    sorted_by_population.sort(key=itemgetter(1), reverse=True)
    found_city = cities[str(sorted_by_population[0][0])]
    df.loc[i] = [headline, found_city['name'], found_city['countrycode']]

df.to_csv("data/cities.csv", index=False)
print(df)

# print(set(headlines) - set(cities_in_headings.keys()))