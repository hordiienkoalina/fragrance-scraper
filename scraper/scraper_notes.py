import csv
import requests
import time
from bs4 import BeautifulSoup
from collections import defaultdict

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
            perfume_url = perfume_link.get('href', '')
            perfumes.append((brand, country, perfume_url))
    
    # Print statement to make sure the script is running
    print('get_perfumes executed')

    return perfumes

# Scrapes all notes of each perfume above
def get_notes(perfume_info):
    country, perfume_url = perfume_info
    response = requests.get(perfume_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    notes = [img.get('alt', '') for img in soup.find_all('img', class_='np np0')]
    
    # Print statement to make sure the script is running
    print('get_notes executed')

    return country, notes

url = 'https://www.parfumo.com/Brands'
brands_and_countries = get_brands_and_countries(url)

# Empty dict for storing perfume_count and notes
perfume_note_data = defaultdict(lambda: {"perfume_count": 0, "notes": defaultdict(int)})

# Total perfume number + note usage per country couters
for brand_info in brands_and_countries:
    perfumes = get_perfumes(brand_info)
    for perfume_info in perfumes:
        country, notes = get_notes(perfume_info)
        perfume_note_data[country]["perfume_count"] += 1
        for note in notes:
            perfume_note_data[country]["notes"][note] += 1
        # Pauses for 1 second
        time.sleep(1)

# Writes the brands, total perfume count, notes, note count to a CSV file
with open('data/country_notes.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Perfume Count", "Note", "Note Count"])
    for country, data in perfume_note_data.items():
        for note, count in data["notes"].items():
            writer.writerow([country, data["perfume_count"], note, count])