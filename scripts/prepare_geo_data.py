from datapackage import Package
import geopandas as gpd
import urllib.parse

package = Package('https://datahub.io/core/geo-countries/datapackage.json')

# Creates an absolute URL for each resource
geojson_url = None
for resource in package.resources:
    if resource.descriptor['format'] == 'geojson':
        geojson_url = urllib.parse.urljoin('https://datahub.io/', resource.descriptor['path'])

# Loads the GeoJSON data into a GeoDataFrame
gdf = gpd.read_file(geojson_url)

# Saves the GeoDataFrame to a CSV file in the data directory
gdf.to_csv('data/geo_countries.csv')
print('CSV generated')