from dash import Dash, html, dcc
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import pycountry
import country_converter as coco

# Load GeoJSON data
with urlopen('https://datahub.io/core/geo-countries/r/countries.geojson') as response:
    countries_geojson = json.load(response)

# Loads perfume data, removes Unknown countries and standardises known ones
df = pd.read_csv('data/country_notes.csv')
df = df.loc[df['Country'] != 'Unknown']
df['Country'] = coco.convert(names=df['Country'], to='name_short')

# Converts perfume country names to country codes to match GeoJSON
def get_country_code(country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except AttributeError:
        return None
df['Country Code'] = df['Country'].apply(get_country_code)

# Creates a Dash app
app = Dash(__name__)

if __name__ == '__main__':
    app.run_server(debug=True)