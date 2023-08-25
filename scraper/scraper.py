import csv
import requests
import time
from bs4 import BeautifulSoup

# Scrape countries and brands
def get_brands_and_countries(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    brands_and_countries = []
    
    for link in soup.find_all('a', class_='p-box mb-1 pl-1 pr-1'):
        brand = link.text.strip()
        img_tag = link.find('img', class_='flag')
        brand_url = link.get('href', '')
        
        if img_tag is not None:
            country = img_tag.get('alt', '')
        else:
            country = "Unknown"

        brands_and_countries.append((brand, country, brand_url))

    return brands_and_countries

# Scrape all perfumes, perfume URLs and release years of each brand
def get_perfumes(brand_info):
    brand, country, brand_url = brand_info
    response = requests.get(brand_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    perfumes = []
    
    for div in soup.find_all('div', class_ = 'name'):
        perfume_link = div.find('a')
        if perfume_link:
            perfume_name = perfume_link.text.strip()
            perfume_url = perfume_link.get('href', '')
            release_year_tag = div.find('a', href = lambda x: x and "Release_Years" in x)
            
            if release_year_tag:
                release_year = release_year_tag.text.strip("()")
            else:
                release_year = "Unknown"
            
            perfumes.append((brand, brand_url, country, perfume_name, release_year, perfume_url))

    print('get_perfumes executed')
    return perfumes

# Scrape all notes of each perfume
def get_notes(perfume_info):
    brand, brand_url, country, perfume_name, release_year, perfume_url = perfume_info
    response = requests.get(perfume_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    notes = [img.get('alt', '') for img in soup.find_all('img', class_='np np0')]
    
    print('get_notes executed')
    return brand, brand_url, country, perfume_name, release_year, perfume_url, notes

url = 'https://www.parfumo.com/Brands'
brands_and_countries = get_brands_and_countries(url)

perfume_data = []

for brand_info in brands_and_countries:
    perfumes = get_perfumes(brand_info)
    for perfume_info in perfumes:
        data = get_notes(perfume_info)
        perfume_data.append(data)
        time.sleep(1)

# Write the data to a CSV file
with open('data/perfume_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Brand URL", "Country", "Perfume Name", "Release Year", "Perfume URL", "Note"])
    for data in perfume_data:
        brand, brand_url, country, perfume_name, release_year, perfume_url, notes = data
        for note in notes:
            writer.writerow([brand, brand_url, country, perfume_name, release_year, perfume_url, note])
