import pandas as pd
import geonamescache

df = pd.read_csv('data/cities.csv')

gc = geonamescache.GeonamesCache()
cities = gc.get_cities()

df['Latitude'], df['Longitude'] = None, None
for i in df.index:
    city_name = df['City'][i]
    countrycode = df['Country code'][i]
    cities_list = gc.get_cities_by_name(city_name)
    for city_candidate in cities_list:
        city = list(city_candidate.values())[0]
        if city['countrycode'] == countrycode:
            lat = city['latitude']
            lon = city['longitude']
            df['Latitude'][i] = lat
            df['Longitude'][i] = lon

print(df)

df.to_csv("data/coordinates.csv", index=False)
