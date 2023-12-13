import requests
from bs4 import BeautifulSoup
import re
import json


def save_to_file(data, filename='calendario_fga.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def scrape_atletismo_gal():
    url = "https://atletismo.gal/competicions/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []

        for event_div in soup.find_all('div', class_='row archive__body__row'):
            
            date_div = event_div.find('div', class_='archive__body__item__date')
            date_span = date_div.find('span')
            #cambiar el formato de este 02/12/2023 a este 2023-12-02
            date = date_span.text.strip() if date_span else None
            date = date.split('/')
            date = date[2]+'-'+date[1]+'-'+date[0]


            category_span = event_div.find('div', class_='archive__body__item')
            category = category_span.text.strip() if category_span else None

            place_span = event_div.find('div', class_='col-xl-2 archive__body__item').find('span')
            place = place_span.text.strip() if place_span else None

            title_a = event_div.find('div', class_='archive__body__item__title').find('a')
            title = title_a.text.strip() if title_a else None
            url = title_a['href'] if title_a and 'href' in title_a.attrs else None

            
            events.append({
                'title': title,
                'place': place,
                'url': url,
                'start': date,
            })

        return events
    else:
        print(f"Error {response.status_code} al obtener la página.")


if __name__ == "__main__":
    scraped_data = scrape_atletismo_gal()
    # Guardar los datos en un archivo JSON
    save_to_file(scraped_data, 'calendario_fga.json')