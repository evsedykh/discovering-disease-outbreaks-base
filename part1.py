import os
import re
import geonamescache
import pandas as pd
from unidecode import unidecode
from operator import itemgetter

os.path.abspath('.')

headlines_file = open('data/headlines.txt')
# headlines_file = open('data/problematic.txt')
headlines = headlines_file.read().splitlines()
headlines_file.close()
# for headline in headlines:
#    print(headline)

gc = geonamescache.GeonamesCache()
cities1 = gc.get_cities()
ascii_cities = [city['geonameid'] for city in cities1.values() if city['name'] == unidecode(city['name'])]
names = {cities1[str(id)]['name']: cities1[str(id)]['geonameid'] for id in ascii_cities}
accented_cities = [city['geonameid'] for city in cities1.values() if city['name'] != unidecode(city['name'])]
alternative_names = {unidecode(cities1[str(id)]['name']): cities1[str(id)]['geonameid'] for id in accented_cities}
names.update(alternative_names)
alternative_names = {unidecode(cities1[str(id)]['name']): cities1[str(id)]['name'] for id in accented_cities}
del names['Of']
del names['Come']

def find_city(city, pattern, string):
    found = re.search(city_pattern, string)
    if found:
        without_city = re.sub(city_pattern, '', string).strip()
        without_city = re.sub(' {2,}', ' ', without_city)
        # print('City ', city, " is found in '", string, "'", sep='')
        return without_city
    return None


def prepare_cre(city):
    return re.compile(r'\b' + city + r'\b', re.ASCII | re.IGNORECASE)


headlines_without_cities = []
headlines_without_found_city = set()

city_candidates = dict()
for city in names.keys():
    city_pattern = prepare_cre(city)
    for headline in headlines:
        found = find_city(city, city_pattern, headline)
        if found:
            headlines_without_cities.append(found)
            if headline not in city_candidates:
                city_candidates[headline] = [city]
            else:
                city_candidates[headline].append(city)

df = pd.DataFrame(columns=['Heading', 'City', 'Country code'])
for i, headline in enumerate(city_candidates):
    cities = city_candidates[headline]
    cities.sort(key=lambda s: len(s), reverse=True)
    cities_list = gc.get_cities_by_name(cities[0])
    if not cities_list:
        cities_list = gc.get_cities_by_name(alternative_names[cities[0]])
    print(i, '. ', headline, sep='', end='')
    sorted_by_population = []
    for city in cities_list:
        sorted_by_population.append((int(list(city.keys())[0]), list(city.values())[0]['population']))
    sorted_by_population.sort(key=itemgetter(1), reverse=True)
    found_city = cities1[str(sorted_by_population[0][0])]
    df.loc[i] = [headline, found_city['name'], found_city['countrycode']]
    print(':', found_city['name'], ':', found_city['countrycode'])

df.to_csv("data/cities.csv", index=False)

# print(set(headlines) - set(city_candidates.keys()))