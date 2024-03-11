from github import Github
# Authentication is defined via github.Auth
from github import Auth
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time


# using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo("Toimil/AtletismoSantiago")
contents = repo.get_contents("data/calendario_fga.json")

today = datetime.today().strftime("%d/%m/%Y")




def save_to_file(data, filename='calendario_fga.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def open_file(filename='calendario_fga.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
        return json.dumps(json_content)


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
    
        response = requests.get(url)
        
        if response.status_code == 200:
            print("Datos scrapeados con exito a la url ", url, "en la fecha ", today)

            soup = BeautifulSoup(response.text, 'html.parser')

            for event_div in soup.find_all('div', class_='row archive__body__row'):
                
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



scraped_data = scrape_atletismo_gal()
# Guardar los datos en un archivo JSON
save_to_file(scraped_data, 'calendario_fga.json')


repo.update_file(contents.path, "actualizacion calendario " + today, open_file('calendario_fga.json'), contents.sha)
print ("Datos actualizados con exito en github en el archivo calendario_fga.json")
g.close()
print ("Esperando 1 min y 30 segundos a que se actualice el archivo calendario_fga.json")
time.sleep(90)
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
# using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo("Toimil/AtletismoSantiago")
contents = repo.get_contents("data/output.json")


def split_name(full_name):
    # Dividir el nombre completo en partes (asumiendo que el formato es "Apellido1 Apellido2, Nombre")
    name_parts = full_name.split(', ')
    
    if len(name_parts) == 2:
        last_name = name_parts[0]
        first_name = name_parts[1]
    else:
        # Si el formato no es el esperado, asignar el nombre completo como el primer nombre
        last_name = ''
        first_name = full_name

    return first_name, last_name


def extract_athlete_id(string):
    # Buscar el patrón 'id=XXX' en la cadena
    match = re.search(r'id=([^&]+)', string)
    
    # Si se encuentra el patrón, devolver la parte coincidente (el ID)
    if match:
        return match.group(1)
    else:
        # Si no se encuentra el patrón, devolver None o un valor predeterminado
        return None




def generate_url(temporada, tp, sx):
    base_url = "http://ranking.atletismo.gal/ranking_lista.asp"
    params = {
        'opcion': '3',
        'prueba': 'completo',
        'tp': tp,
        'sx': sx,
        'club': 'STOC',
        'cat': '0', 
        'nreg': '10000',
        'comp': '0',
        'temporada': temporada
    }
    return f"{base_url}?{('&'.join(f'{key}={value}' for key, value in params.items()))}"

# Lista de temporadas a considerar
temporadas = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

# Lista de tipos de prueba (tp) y géneros (sx) a considerar
tipos_prueba = ['AL', 'PC', 'RU']
generos = ['H', 'M']

# Crear una lista para almacenar los datos de todas las tablas
data_list = []

# Iterar sobre las temporadas, tipos de prueba y géneros
for temporada in temporadas:
    for tp in tipos_prueba:
        for sx in generos:
            # Generar la URL para la combinación actual
            url = generate_url(temporada, tp, sx)

            # Realizar la solicitud y obtener el contenido de la página
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            

            # Encuentra todas las tablas en la página
            tables = soup.find_all('table', {'border': '1'})

            

            for table in tables:
                # Encontrar el título de la tabla
                title = table.find('tr').find('td', {'align': 'left'}).text.strip()

                # Encontrar los campos en el siguiente tr con la clase calendario_cab_mes
                header_row = table.find('tr', {'class': 'calendario_cab_mes'})
                headers = [header.text.strip() for header in header_row.find_all('td')]

                # Buscar la posición de la columna con título 'Atleta'
                athlete_index = None
                for i, header in enumerate(headers):
                    if 'Atleta' in header:
                        athlete_index = i
                        break
                    
                # Encontrar todas las filas de datos en la tabla
                data_rows = table.find_all('tr', class_=lambda x: x and ('calendario_linea1' in x or 'calendario_linea-1' in x))


                # Crear una lista para almacenar los datos de la tabla actual
                table_data = []

                for row in data_rows:
                    columns = row.find_all(['td', 'b'])
                    del columns[0]
                    del columns[1]



                    # Verificar que el número de columnas coincida con el número de encabezados
                    if len(columns) == len(headers):
                        # Extraer el nombre y enlace de acceso del atleta desde la columna 'Atleta'
                        athlete_column = columns[athlete_index]
                        athlete_name = athlete_column.find('a').text.strip()
                        onclick_attribute = athlete_column.find('a')['onclick']
                        # Extraer el ID del atleta
                        athlete_id = extract_athlete_id(onclick_attribute)
                        # Separar el nombre y apellidos
                        first_name, last_name = split_name(athlete_name)

                        # Crear un diccionario con la información del atleta
                        athlete_info = {
                            'Nombre': first_name,
                            'Apellido': last_name,
                            'ID': athlete_id
                        }

                        row_data = {headers[i]: column.text.strip() for i, column in enumerate(columns)}
                        row_data['Atleta'] = athlete_info
                        table_data.append(row_data)
                    else:
                        print(f"Advertencia: El número de columnas ({len(columns)}) no coincide con el número de encabezados ({len(headers)})")

                # Almacenar los datos de la tabla en un diccionario
                table_info = {
                    'Temporada': temporada,
                    'TipoPrueba': tp,
                    'Genero': sx,
                    'Title': title,
                    'Data': table_data
                    
                }

                # Agregar el diccionario a la lista principal
                data_list.append(table_info)
    print("Datos scrapeados con exito de la temporada ", temporada, "en la fecha", today)
            


# Reemplazar caracteres especiales en todos los campos de texto
for entry in data_list:
    for key, value in entry.items():
        if isinstance(value, str):
            entry[key] = value.replace('\u00a0', ' ')

with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)


repo.update_file(contents.path, "actualizacion estadisticas atletas " + today, open_file('output.json'), contents.sha)
print ("Datos actualizados con exito en github en el archivo output.json")

g.close()





print ("Esperando 1 min y 30 segundos a que se actualice el archivo de estadisticas de atletas output.json")
time.sleep(90)
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

# using an access token
auth = Auth.Token("")

# Public Web Github
g = Github(auth=auth)

repo = g.get_repo("Toimil/AtletismoSantiago")
contents = repo.get_contents("data/output2.json")


categorias_2024 = {

    "20092010": "SUB 16",
    "20072008": "SUB 18",
    "20052006": "SUB 20",
    "20022004": "SUB 23",
    "19002001": "Absoluto",
    "19851989": "M 35",
    "19801984": "M 40",
    "19751979": "M 45",
    "19701974": "M 50",
    "19651969": "M 55",
    "19601964": "M 60",
    "19551959": "M 65",
    "19501954": "M 70",
    "19451949": "M 75",
    "19401944": "M 80",
    "19351939": "M 85",
    "19301934": "M 90"
}

categorias_2023 = {

    "20082009": "SUB 16",
    "20062007": "SUB 18",
    "20042005": "SUB 20",
    "20012003": "SUB 23",
    "19002000": "Absoluto",
    "19841988": "M 35",
    "19791983": "M 40",
    "19741978": "M 45",
    "19691973": "M 50",
    "19641968": "M 55",
    "19591963": "M 60",
    "19541958": "M 65",
    "19491953": "M 70",
    "19441948": "M 75",
    "19391943": "M 80",
    "19341938": "M 85",
    "19391933": "M 90"
}

categorias_2022 = {

    "20072008": "SUB 16",
    "20052006": "SUB 18",
    "20032004": "SUB 20",
    "20002002": "SUB 23",
    "19001999": "Absoluto",
    "19831987": "M 35",
    "19781982": "M 40",
    "19731977": "M 45",
    "19681972": "M 50",
    "19631967": "M 55",
    "19581962": "M 60",
    "19531957": "M 65",
    "19481952": "M 70",
    "19431947": "M 75",
    "19381942": "M 80",
    "19331937": "M 85",
    "19381932": "M 90"
}


categorias_2021 = {

    "20062007": "SUB 16",
    "20042005": "SUB 18",
    "20022003": "SUB 20",
    "19992001": "SUB 23",
    "19001998": "Absoluto",
    "19821986": "M 35",
    "19771981": "M 40",
    "19721976": "M 45",
    "19671971": "M 50",
    "19621966": "M 55",
    "19571961": "M 60",
    "19521956": "M 65",
    "19471951": "M 70",
    "19421946": "M 75",
    "19371941": "M 80",
    "19321936": "M 85",
    "19271931": "M 90"
}

categorias_2020 = {

    "20052006": "SUB 16",
    "20032004": "SUB 18",
    "20012002": "SUB 20",
    "19982000": "SUB 23",
    "19001997": "Absoluto",
    "19811985": "M 35",
    "19761980": "M 40",
    "19711975": "M 45",
    "19661970": "M 50",
    "19611965": "M 55",
    "19561960": "M 60",
    "19511955": "M 65",
    "19461950": "M 70",
    "19411945": "M 75",
    "19361940": "M 80",
    "19311935": "M 85",
    "19261930": "M 90"
}

categorias_2019 = {

    "20042005": "SUB 16",
    "20022003": "SUB 18",
    "20002001": "SUB 20",
    "19971999": "SUB 23",
    "19001996": "Absoluto",
    "19801984": "M 35",
    "19751979": "M 40",
    "19701974": "M 45",
    "19651969": "M 50",
    "19601964": "M 55",
    "19551959": "M 60",
    "19501954": "M 65",
    "19451949": "M 70",
    "19401944": "M 75",
    "19351939": "M 80",
    "19301934": "M 85",
    "19251939": "M 90"
}


categorias_2018 = {

    "20032004": "SUB 16",
    "20012002": "SUB 18",
    "19992000": "SUB 20",
    "19961998": "SUB 23",
    "19001995": "Absoluto",
    "19781982": "M 35",
    "19731977": "M 40",
    "19681972": "M 45",
    "19631967": "M 50",
    "19581962": "M 55",
    "19531957": "M 60",
    "19481952": "M 65",
    "19431947": "M 70",
    "19381942": "M 75",
    "19331937": "M 80",
    "19271932": "M 85",
    "19231927": "M 90"
}

categorias_2017 = {

    "20022003": "SUB 16",
    "20002001": "SUB 18",
    "19981999": "SUB 20",
    "19951997": "SUB 23",
    "19001994": "Absoluto",
    "19781982": "M 35",
    "19731977": "M 40",
    "19681972": "M 45",
    "19631967": "M 50",
    "19581962": "M 55",
    "19531957": "M 60",
    "19481952": "M 65",
    "19431947": "M 70",
    "19381942": "M 75",
    "19331937": "M 80",
    "19271932": "M 85",
    "19231927": "M 90"
}
categorias_2016 = {

    "20012002": "SUB 16",
    "19992000": "SUB 18",
    "19971998": "SUB 20",
    "19941996": "SUB 23",
    "19001993": "Absoluto",
    "19761980": "M 35",
    "19711974": "M 40",
    "19661970": "M 45",
    "19611965": "M 50",
    "19561960": "M 55",
    "19511955": "M 60",
    "19461950": "M 65",
    "19411945": "M 70",
    "19361940": "M 75",
    "19311935": "M 80",
    "19261930": "M 85",
    "19211925": "M 90"
}
categorias_2015 = {

    "20002001": "SUB 16",
    "19981999": "SUB 18",
    "19961997": "SUB 20",
    "19931995": "SUB 23",
    "19001992": "Absoluto",
    "19751979": "M 35",
    "19701974": "M 40",
    "19651969": "M 45",
    "19601964": "M 50",
    "19551959": "M 55",
    "19501954": "M 60",
    "19451949": "M 65",
    "19401944": "M 70",
    "19351939": "M 75",
    "19301934": "M 80",
    "19251929": "M 85",
    "19201924": "M 90"
}
categorias_2014 = {

    "19992000": "SUB 16",
    "19971998": "SUB 18",
    "19951996": "SUB 20",
    "19921994": "SUB 23",
    "19001991": "Absoluto",
    "19751979": "M 35",
    "19701974": "M 40",
    "19651969": "M 45",
    "19601964": "M 50",
    "19551959": "M 55",
    "19501954": "M 60",
    "19451949": "M 65",
    "19401944": "M 70",
    "19351939": "M 75",
    "19301934": "M 80",
    "19251929": "M 85",
    "19201924": "M 90"
}


import requests
from bs4 import BeautifulSoup
import re

def split_name(full_name):
    # Dividir el nombre completo en partes (asumiendo que el formato es "Apellido1 Apellido2, Nombre")
    name_parts = full_name.split(', ')
    
    if len(name_parts) == 2:
        last_name = name_parts[0]
        first_name = name_parts[1]
    else:
        # Si el formato no es el esperado, asignar el nombre completo como el primer nombre
        last_name = ''
        first_name = full_name

    return first_name, last_name

def extract_athlete_id(string):
    # Buscar el patrón 'id=XXX' en la cadena
    match = re.search(r'id=([^&]+)', string)
    
    # Si se encuentra el patrón, devolver la parte coincidente (el ID)
    if match:
        return match.group(1)
    else:
        # Si no se encuentra el patrón, devolver None o un valor predeterminado
        return None

def generate_url(temporada, tp, sx, categoria):
    base_url = "http://ranking.atletismo.gal/ranking_lista.asp"
    params = {
        'opcion': '3',
        'prueba': 'completo',
        'tp': tp,
        'sx': sx,
        'club': 'STOC',
        'cat': categoria, 
        'nreg': '10000',
        'comp': '0',
        'temporada': temporada
    }
    return f"{base_url}?{('&'.join(f'{key}={value}' for key, value in params.items()))}"

# Lista de temporadas a considerar
temporadas = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

# Lista de tipos de prueba (tp) y géneros (sx) a considerar
tipos_prueba = ['AL', 'PC', 'RU']
generos = ['H', 'M']

# Diccionario de categorías por temporada
categorias_por_temporada = {
    '2014': categorias_2014,
    '2015': categorias_2015,
    '2016': categorias_2016,
    '2017': categorias_2017,
    '2018': categorias_2018,
    '2019': categorias_2019,
    '2020': categorias_2020,
    '2021': categorias_2021,
    '2022': categorias_2022,
    '2023': categorias_2023,
    '2024': categorias_2024  
}

# Crear una lista para almacenar los datos de todas las tablas
data_list = []

# Iterar sobre las temporadas, tipos de prueba y géneros
for temporada in temporadas:
    for categoria, genero in categorias_por_temporada[temporada].items():
        print ("Haciendo scrapping a la temporada ", temporada, "y categoria de nombre ", categorias_por_temporada[temporada][categoria] )
        for tp in tipos_prueba:
            for sx in generos:
                url = generate_url(temporada, tp, sx, categoria)
               # print("Haciendo scrapping a la url: ", url)


                # Realizar la solicitud y obtener el contenido de la página
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Encuentra todas las tablas en la página
                tables = soup.find_all('table', {'border': '1'})

                for table in tables:
                    # Encontrar el título de la tabla
                    title = table.find('tr').find('td', {'align': 'left'}).text.strip()

                    # Encontrar los campos en el siguiente tr con la clase calendario_cab_mes
                    header_row = table.find('tr', {'class': 'calendario_cab_mes'})
                    headers = [header.text.strip() for header in header_row.find_all('td')]

                    # Buscar la posición de la columna con título 'Atleta'
                    athlete_index = None
                    for i, header in enumerate(headers):
                        if 'Atleta' in header:
                            athlete_index = i
                            break
                        
                    # Encontrar todas las filas de datos en la tabla
                    data_rows = table.find_all('tr', class_=lambda x: x and ('calendario_linea1' in x or 'calendario_linea-1' in x))

                    # Crear una lista para almacenar los datos de la tabla actual
                    table_data = []

                    for row in data_rows:
                        columns = row.find_all(['td', 'b'])
                        del columns[0]
                        del columns[1]

                        # Verificar que el número de columnas coincida con el número de encabezados
                        if len(columns) == len(headers):
                            # Extraer el nombre y enlace de acceso del atleta desde la columna 'Atleta'
                            athlete_column = columns[athlete_index]
                            athlete_name = athlete_column.find('a').text.strip()
                            onclick_attribute = athlete_column.find('a')['onclick']
                            # Extraer el ID del atleta
                            athlete_id = extract_athlete_id(onclick_attribute)
                            # Separar el nombre y apellidos
                            first_name, last_name = split_name(athlete_name)

                            # Crear un diccionario con la información del atleta
                            athlete_info = {
                                'Nombre': first_name,
                                'Apellido': last_name,
                                'ID': athlete_id
                            }

                            row_data = {headers[i]: column.text.strip() for i, column in enumerate(columns)}
                            row_data['Atleta'] = athlete_info
                            table_data.append(row_data)
                        else:
                            print(f"Advertencia: El número de columnas ({len(columns)}) no coincide con el número de encabezados ({len(headers)})")

                    # Almacenar los datos de la tabla en un diccionario
                    table_info = {
                        'Temporada': temporada,
                        'TipoPrueba': tp,
                        'Genero': sx,
                        'Categoria': categorias_por_temporada[temporada][categoria],  # Asignar el valor de la categoría

                        'Title': title,
                        'Data': table_data
                    }

                    # Agregar el diccionario a la lista principal
                    data_list.append(table_info)

# Guardar los datos en un archivo JSON
import json

# Reemplazar caracteres especiales en todos los campos de texto
for entry in data_list:
    for key, value in entry.items():
        if isinstance(value, str):
            entry[key] = value.replace('\u00a0', ' ')

with open('output2.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)


repo.update_file(contents.path, "actualizacion ranking estadisticas " + today, open_file('output2.json'), contents.sha)
print ("Datos actualizados con exito en github en el archivo output.json")

g.close()

time.sleep(10)


