import pandas as pd
import numpy as np
from haversine import haversine
from pandas import option_context
from sklearn.cluster import KMeans
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def great_circle_distance(p1, p2):
    return haversine(p1, p2, unit='km')


df = pd.read_csv('data/coordinates.csv')

print(df['Heading'].str)
df = df[df.Heading.str.contains('Zika|Mad Cow|MDC') == True]
print(df)

map_plotter = Basemap()

us_df = df[df['Country code'] == 'US']
world_df = df[df['Country code'] != 'US']

coordinates = us_df[['Longitude', 'Latitude']]
cluster_model_kmeans = KMeans(n_clusters=4)
predicted_kmeans = cluster_model_kmeans.fit_predict(coordinates)
us_df['cluster'] = predicted_kmeans
map_plotter.drawcoastlines()
map_plotter.drawcountries()
map_plotter.scatter(coordinates['Longitude'], coordinates['Latitude'], c=predicted_kmeans, latlon=True, cmap=plt.cm.jet)
plt.show()
for cluster_number in range(0, 4):
    cluster = us_df[us_df.cluster == cluster_number]
    mean_lat, mean_lon = np.mean(cluster['Latitude']), np.mean(cluster['Longitude'])
    cluster['Distance'] = None
    for i in cluster.index:
        cluster['Distance'][i] = great_circle_distance((mean_lat, mean_lon), (cluster['Latitude'][i], cluster['Longitude'][i]))
    cluster = cluster.sort_values(by=['Distance'])
    with option_context('display.max_colwidth', 400):
        print(cluster[['Heading', 'Distance']])


coordinates = world_df[['Longitude', 'Latitude']]
cluster_model_kmeans = KMeans(n_clusters=10)
predicted_kmeans = cluster_model_kmeans.fit_predict(coordinates)
world_df['cluster'] = predicted_kmeans
map_plotter.drawcoastlines()
map_plotter.drawcountries()
map_plotter.scatter(coordinates['Longitude'], coordinates['Latitude'], c=predicted_kmeans, latlon=True, cmap=plt.cm.jet)
plt.show()

for cluster_number in range(0, 10):
    cluster = world_df[world_df.cluster == cluster_number]
    mean_lat, mean_lon = np.mean(cluster['Latitude']), np.mean(cluster['Longitude'])
    cluster['Distance'] = None
    for i in cluster.index:
        cluster['Distance'][i] = great_circle_distance((mean_lat, mean_lon), (cluster['Latitude'][i], cluster['Longitude'][i]))
    cluster = cluster.sort_values(by=['Distance'])
    with option_context('display.max_colwidth', 400):
        print(cluster[['Heading', 'Distance']])
