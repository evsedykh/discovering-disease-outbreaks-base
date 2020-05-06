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
del names['Of'], names['Come']


def find_city(city, pattern, string):
    if re.search(city_pattern, string):
        return True
    return None


def prepare_cre(city):
    return re.compile(r'\b' + city + r'\b', re.ASCII | re.IGNORECASE)


cities_in_headings = {}
for city in names.keys():
    city_pattern = prepare_cre(city)
    for headline in headlines:
        if find_city(city, city_pattern, headline):
            if headline not in cities_in_headings:
                cities_in_headings[headline] = [city]
            else:
                cities_in_headings[headline].append(city)

df = pd.DataFrame(columns=['Heading', 'City', 'Country code'])
for i, headline in enumerate(cities_in_headings):
    cities_candidates = cities_in_headings[headline]
    print(cities_candidates)
    cities_candidates.sort(key=lambda s: len(s), reverse=True)
    cities_list = gc.get_cities_by_name(cities_candidates[0])
    if not cities_list:
        cities_list = gc.get_cities_by_name(alternative_names[cities_candidates[0]])
    sorted_by_population = []
    for city in cities_list:
        sorted_by_population.append((int(list(city.keys())[0]), list(city.values())[0]['population']))
    sorted_by_population.sort(key=itemgetter(1), reverse=True)
    found_city = cities[str(sorted_by_population[0][0])]
    df.loc[i] = [headline, found_city['name'], found_city['countrycode']]

df.to_csv("data/cities.csv", index=False)
print(df)

# print(set(headlines) - set(city_candidates.keys()))