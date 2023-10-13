import requests
import json
import pprint
import pandas as pd



#------------------------------------------------TRENDING - MOVIE - DAY---------------------------------------------------------
# URL de la API
url = "https://api.themoviedb.org/3/trending/movie/day"

# Clave API
api_key = "256fcaa48a42faf31d52b502826de42e"

# Token de acceso de lectura de la API
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNTZmY2FhNDhhNDJmYWYzMWQ1MmI1MDI4MjZkZTQyZSIsInN1YiI6IjY1MWVjOWJjYzUwYWQyMDEyYzFiYjZlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.wwK5ebY9K7RKjnbeW4XZjmhw9cXXjzdDHtKl45UsEBI"

# Configura el encabezado de autorización
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Ingreso del nombre de la película que quiero buscar
#movie = "star wars" #input("Please input a show name.  ")

# Creo el diccionario 'pages' para almacenar los datos de cada página.
pages = {}

for i in range(1,4+1):
    # Configura los parámetros de la solicitud
    params = {
        "api_key": api_key, "page":{i}
    }

    # Realiza la solicitud GET
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        results=data['results']
        df = pd.DataFrame(results)
        #print(df.columns)
        pages[f'df_{i}'] = df[['id', 'title', 'release_date', 'media_type', 'adult', 'original_language', 'overview', 'popularity', 'vote_average', 'vote_count']]
        
    else:
        print(f"Error: {response.status_code}")

# Uno las tablas con 'merge'.
print(pages[f'df_{1}'].merge(pages[f'df_{2}'], how = 'outer').merge(pages[f'df_{3}'], how = 'outer').merge(pages[f'df_{4}'], how = 'outer'))





"""
#------------------------------------------------TRENDING - TV - DAY---------------------------------------------------------
# URL de la API
url = "https://api.themoviedb.org/3/trending/tv/day"

# Clave API
api_key = "256fcaa48a42faf31d52b502826de42e"

# Token de acceso de lectura de la API
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNTZmY2FhNDhhNDJmYWYzMWQ1MmI1MDI4MjZkZTQyZSIsInN1YiI6IjY1MWVjOWJjYzUwYWQyMDEyYzFiYjZlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.wwK5ebY9K7RKjnbeW4XZjmhw9cXXjzdDHtKl45UsEBI"

# Configura el encabezado de autorización
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Ingreso del nombre de la película que quiero buscar
#movie = "star wars" #input("Please input a show name.  ")

# Creo el diccionario 'pages' para almacenar los datos de cada página.
pages = {}

for i in range(1,4+1):
    # Configura los parámetros de la solicitud
    params = {
        "api_key": api_key, "page":{i}
    }

    # Realiza la solicitud GET
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        results=data['results']
        df = pd.DataFrame(results)
        print(df.columns)
        pages[f'df_{i}'] = df[['id', 'original_name', 'first_air_date', 'media_type', 'adult', 'overview', 'popularity', 'vote_average', 'vote_count']]
        
    else:
        print(f"Error: {response.status_code}")

# Uno las tablas con 'merge'.
print(pages[f'df_{1}'].merge(pages[f'df_{2}'], how = 'outer').merge(pages[f'df_{3}'], how = 'outer').merge(pages[f'df_{4}'], how = 'outer'))
"""









"""
#------------------------------------------------BUSCAR PELÍCULAS---------------------------------------------------------
# URL de la API
url = "https://api.themoviedb.org/3/search/movie"

# Clave API
api_key = "256fcaa48a42faf31d52b502826de42e"

# Token de acceso de lectura de la API
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNTZmY2FhNDhhNDJmYWYzMWQ1MmI1MDI4MjZkZTQyZSIsInN1YiI6IjY1MWVjOWJjYzUwYWQyMDEyYzFiYjZlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.wwK5ebY9K7RKjnbeW4XZjmhw9cXXjzdDHtKl45UsEBI"

# Configura el encabezado de autorización
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Ingreso del nombre de la película que quiero buscar
movie = "star wars" #input("Please input a show name.  ")

# Creo el diccionario 'pages' para almacenar los datos de cada página.
pages = {}

for i in range(1,4+1):
    # Configura los parámetros de la solicitud
    params = {
        "api_key": api_key, "query":movie, "page":{i}
    }

    # Realiza la solicitud GET
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        results=data['results']
        df = pd.DataFrame(results)
        pages[f'df_{i}'] = df[['title', 'release_date', 'original_language', 'overview', 'popularity', 'vote_average', 'vote_count']]
        #pprint.pprint(data)
        #print(df[['title', 'release_date', 'original_language', 'overview', 'popularity', 'vote_average', 'vote_count']])
        
    else:
        print(f"Error: {response.status_code}")

# Uno las tablas con 'merge'.
print(pages[f'df_{1}'].merge(pages[f'df_{2}'], how = 'outer').merge(pages[f'df_{3}'], how = 'outer').merge(pages[f'df_{4}'], how = 'outer'))
"""