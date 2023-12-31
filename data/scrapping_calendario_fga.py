import requests
from bs4 import BeautifulSoup
import re
import json


def save_to_file(data, filename='calendario_fga2.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def scrape_atletismo_gal():
    urls = ["https://atletismo.gal/competicions/",
    "https://atletismo.gal/competicions/?cp_date=01%2F01%2F2024",
    "https://atletismo.gal/competicions/?cp_date=01%2F02%2F2024",
    "https://atletismo.gal/competicions/?cp_date=01%2F03%2F2024"]
    events = []

    for url in urls:
    
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for event_div in soup.find_all('div', class_='row archive__body__row'):
                print(event_div)
                
                date_div = event_div.find('div', class_='archive__body__item__date')
                date_span = date_div.find('span')
                #cambiar el formato de este 02/12/2023 a este 2023-12-02
                date = date_span.text.strip() if date_span else None
                date = date.split('/')
                date = date[2]+'-'+date[1]+'-'+date[0]


                category_span = event_div.find('div', class_='archive__body__item')
                category = category_span.text.strip() if category_span else None

                if (event_div.find('div', class_='col-xl-2 archive__body__item')):
                    place_span = event_div.find('div', class_='col-xl-2 archive__body__item').find('span')
                    place = place_span.text.strip() if place_span else None
                else:
                    place = ""
                
                title_a = event_div.find('div', class_='archive__body__item__title').find('a')
                title = title_a.text.strip() if title_a else None
                url = title_a['href'] if title_a and 'href' in title_a.attrs else None

                
                events.append({
                    'title': title,
                    'place': place,
                    'url': url,
                    'start': date,
                })

            
        else:
            print(f"Error {response.status_code} al obtener la página.")
    return events        


if __name__ == "__main__":
    scraped_data = scrape_atletismo_gal()
    # Guardar los datos en un archivo JSON
    save_to_file(scraped_data, 'calendario_fga.json')