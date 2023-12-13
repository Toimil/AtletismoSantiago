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
temporadas = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

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

# Guardar los datos en un archivo JSON
import json

# Reemplazar caracteres especiales en todos los campos de texto
for entry in data_list:
    for key, value in entry.items():
        if isinstance(value, str):
            entry[key] = value.replace('\u00a0', ' ')

with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("Scraping completado. Los datos se han guardado en output.json.")
