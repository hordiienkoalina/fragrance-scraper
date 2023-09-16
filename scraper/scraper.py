import csv
import requests
import time
from bs4 import BeautifulSoup
import random
from concurrent.futures import ThreadPoolExecutor

# Constants for rate limiting and parallelization
MAX_WORKERS = 5
SLEEP_TIME = 2

def get(url, retries=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if retries > 0:
            print("Retrying...")
            time.sleep(random.randint(5, 10))
            return get(url, retries-1)
        else:
            print("Max retries reached. Skipping this URL.")
            return None

def get_brands_and_countries(url):
    response = get(url)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    brands_and_countries = []

    for link in soup.find_all('a', class_='p-box mb-1 pl-1 pr-1'):
        brand = link.text.strip()
        img_tag = link.find('img', class_='flag')
        brand_url = link.get('href', '')

        if img_tag:
            country = img_tag.get('alt', '')
        else:
            country = "Unknown"

        brands_and_countries.append((brand, country, brand_url))
    print("get_brands_and_countries executed")

    return brands_and_countries

def get_perfumes(brand_info):
    brand, country, brand_url = brand_info
    response = get(brand_url)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    perfumes = []

    for div in soup.find_all('div', class_='name'):
        perfume_link = div.find('a')
        if perfume_link:
            perfume_name = perfume_link.text.strip()
            perfume_url = perfume_link.get('href', '')
            release_year_tag = div.find('a', href=lambda x: x and "Release_Years" in x)
            if release_year_tag:
                release_year = release_year_tag.text.strip("()")
            else:
                release_year = "Unknown"
            perfumes.append((brand, brand_url, country, perfume_name, release_year, perfume_url))
    print("get_perfumes executed")

    return perfumes

def get_notes(perfume_info):
    brand, brand_url, country, perfume_name, release_year, perfume_url = perfume_info
    response = get(perfume_url)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    notes = [img.get('alt', '') for img in soup.find_all('img', class_='np np0')]
    print("get_notes executed")

    return brand, brand_url, country, perfume_name, release_year, perfume_url, notes

def batch_write_to_csv(batch_data, file_path):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(batch_data)

def scrape_letter(letter, batch_size=100, checkpoint_file='data/perfume_data_checkpoint.csv'):
    time.sleep(random.randint(1, SLEEP_TIME))  # Random sleep to stagger thread start
    url = f"{base_url}{letter}"
    brands_and_countries = get_brands_and_countries(url)
    batch_data = []

    for brand_info in brands_and_countries:
        perfumes = get_perfumes(brand_info)
        for perfume_info in perfumes:
            data = get_notes(perfume_info)
            if data:
                brand, brand_url, country, perfume_name, release_year, perfume_url, notes = data
                for note in notes:
                    batch_data.append([brand, brand_url, country, perfume_name, release_year, perfume_url, note])
                if len(batch_data) >= batch_size:
                    batch_write_to_csv(batch_data, checkpoint_file)
                    batch_data = []
            time.sleep(random.randint(1, SLEEP_TIME))  # Sleep between requests

    if batch_data:
        batch_write_to_csv(batch_data, checkpoint_file)

start_time = time.time()

base_url = 'https://www.parfumo.com/Brands/'
letters_and_symbols = list('abcdefghijklmnopqrstuvwxyz') + ['0']

# Initialize CSV
with open('data/perfume_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Brand URL", "Country", "Perfume Name", "Release Year", "Perfume URL", "Note"])

# Parallel scraping with limited workers
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(scrape_letter, letters_and_symbols)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time} seconds")