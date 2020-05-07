import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from mpl_toolkits.basemap import Basemap
from haversine import haversine, Unit


def great_circle_distance(p1, p2):
    return haversine(p1, p2, unit='km')


df = pd.read_csv('data/coordinates.csv')
coordinates = df[['Longitude', 'Latitude']]

k_values = range(1, 10)
inertia_values = [KMeans(k).fit(coordinates).inertia_
                  for k in k_values]
plt.plot(k_values, inertia_values)
plt.xlabel('K')
plt.ylabel('Inertia')
plt.show()

map_plotter = Basemap()

map_plotter.drawcoastlines()
map_plotter.drawcountries()

# use_model = 'kmeans'
use_model = 'dbscan'

cluster_model_kmeans = KMeans(n_clusters=7)
predicted_kmeans = cluster_model_kmeans.fit_predict(coordinates)
df['Cluster K-means'] = predicted_kmeans


# cluster_model_dbscan = DBSCAN(eps=9.0, min_samples=3) # 1st try without great circle distance
cluster_model_dbscan = DBSCAN(eps=250.0, min_samples=4, metric=great_circle_distance)
predicted_dbscan = cluster_model_dbscan.fit_predict(coordinates)
# coordinates.plot.scatter('Longitude', 'Latitude', c='cl', colormap='gist_rainbow')
df['Cluster DBSCAN'] = predicted_dbscan

if use_model == 'kmeans':
    cluster_colormap = predicted_kmeans
elif use_model == 'dbscan':
    cluster_colormap = predicted_dbscan

map_plotter.scatter(coordinates['Longitude'], coordinates['Latitude'], c=cluster_colormap, latlon=True, cmap=plt.cm.jet)
plt.show()

df.to_csv("data/clusters.csv", index=False)
