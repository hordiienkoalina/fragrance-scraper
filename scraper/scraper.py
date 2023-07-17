import csv
import requests
from bs4 import BeautifulSoup

def get_brands_and_countries(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    brands_and_countries = {}

    # Scrapes brand names directly and country names from IMG ALTs
    for link in soup.find_all('a', class_='p-box mb-1 pl-1 pr-1'):
        brand = link.text.strip()
        img_tag = link.find('img', class_='flag')
        
        # Sets country to Unknown if no ALT available
        if img_tag is not None:
            country = img_tag.get('alt', '')
        else:
            country = "Unknown"

        brands_and_countries[brand] = country

    return brands_and_countries

url = 'https://www.parfumo.com/Brands'
brands_and_countries = get_brands_and_countries(url)

# Writes the brands and countries to a CSV file
with open('brands_and_countries.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Country"])
    for brand, country in brands_and_countries.items():
        writer.writerow([brand, country])