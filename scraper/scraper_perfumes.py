import csv
import requests
import time
from bs4 import BeautifulSoup

# Scrapes countries and brands
def get_brands_and_countries(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    brands_and_countries = []
    
    # Scrapes brand names directly and country names from IMG ALTs
    for link in soup.find_all('a', class_='p-box mb-1 pl-1 pr-1'):
        brand = link.text.strip()
        img_tag = link.find('img', class_='flag')
        brand_url = link.get('href', '')

        # Sets country to Unknown if no ALT available
        if img_tag is not None:
            country = img_tag.get('alt', '')
        else:
            country = "Unknown"

        brands_and_countries.append((brand, country, brand_url))

    return brands_and_countries

# Scrapes all perfumes of each brand above
def get_perfumes(brand_info):
    brand, country, brand_url = brand_info
    response = requests.get(brand_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    perfumes = []
    
    for div in soup.find_all('div', class_='name'):
        perfume_link = div.find('a')
        if perfume_link:
            perfume_name = perfume_link.text.strip()
            perfumes.append((brand, country, perfume_name))
    return perfumes

url = 'https://www.parfumo.com/Brands'
brands_and_countries = get_brands_and_countries(url)

perfumes = []
for brand_info in brands_and_countries:
    perfumes.extend(get_perfumes(brand_info))
    # Pauses for 1 second
    time.sleep(1)  

# Writes the brands, countries, perfumes to a CSV file
with open('../data/raw/country_perfumes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Country", "Perfume"])
    for row in perfumes:
        writer.writerow(row)