import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

today = datetime.today().strftime("%d/%m/%Y")

def scrape_atletismo_gal():
    base_url = "https://atletismo.gal/competicions/?cp_date={}/{}/{}"
    day, month, year = today.split('/')
    urls = [
        base_url.format("01", month, year),
        base_url.format("01", str(int(month) + 1).zfill(2), year),
        base_url.format("01", str(int(month) + 2).zfill(2), year)
    ]
    events = []

    for url in urls:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for article in soup.find_all('article', class_=re.compile(r'\bcompetition\b')):
                date_tag = article.select_one('div.bg-red span')
                if date_tag:
                    raw_date = date_tag.text.strip()
                    date_parts = raw_date.split('/')
                    date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                else:
                    date = None

                title_tag = article.select_one('h2 a')
                title = title_tag.text.strip() if title_tag else None
                url = title_tag['href'] if title_tag and title_tag.has_attr('href') else None

                place_div = article.select_one('div.text-base')
                place = place_div.text.strip() if place_div else ""

                events.append({
                    'title': title,
                    'place': place,
                    'url': url,
                    'start': date,
                })
        else:
            print(f"Error {response.status_code} al obtener la página.")
    return events

def save_to_file(data, filename='data/calendario_fga.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    data = scrape_atletismo_gal()
    save_to_file(data)
    print("Archivo actualizado correctamente.")
