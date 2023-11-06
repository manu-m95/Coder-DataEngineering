import requests
import json
import pprint
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

host="data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
database="data-engineer-database"
username="m_moyano077_coderhouse"
pwd = "X15l3Pst2D"
port_id= '5439'



#------------------------------------------------TRENDING - MOVIE - DAY---------------------------------------------------------
# API de The Movie Database (TMDB), página web de cine y televisión. https://www.themoviedb.org/
# En este código se recogen los datos de las películas de mayor tendencia del día.

# Cada consulta a la API recoge un máximo de 20 resultados (que constituyen una página), por lo que 
# se realizan muchas consultas iterativamente y luego se unen las tablas (o páginas) para tener un mayor conjunto de resultados en una sola tabla.


# URL de la API para movie
url_movie = "https://api.themoviedb.org/3/trending/movie/day"
# URL de la API para tv
url_tv = "https://api.themoviedb.org/3/trending/tv/day"

# Clave API
api_key = "256fcaa48a42faf31d52b502826de42e"

# Token de acceso de lectura de la API
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNTZmY2FhNDhhNDJmYWYzMWQ1MmI1MDI4MjZkZTQyZSIsInN1YiI6IjY1MWVjOWJjYzUwYWQyMDEyYzFiYjZlYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.wwK5ebY9K7RKjnbeW4XZjmhw9cXXjzdDHtKl45UsEBI"

# Configura el encabezado de autorización
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Creo el diccionario 'pages' para almacenar los datos de cada página.
# n_pages: número total de páginas a leer. Máximo posible: 500.
pages = {}
n_pages = 20

for i in range(1,n_pages+1):
    # Configura los parámetros de la solicitud
    params = {
        "api_key": api_key, "page":{i}
    }

    # Realiza la solicitud GET para movie
    response_movie = requests.get(url_movie, params=params, headers=headers)

    if response_movie.status_code == 200:
        data = json.loads(response_movie.text)
        results=data['results']
        df_movie = pd.DataFrame(results)
        #print(df_movie.columns)
        pages[f'df_movie_{i}'] = df_movie[['id', 'title', 'release_date', 'media_type', 'adult', 'original_language', 'overview', 'popularity', 'vote_average', 'vote_count']]
        
    else:
        print(f"Error: {response.status_code}")
        
    # Realiza la solicitud GET para movie
    response_tv = requests.get(url_tv, params=params, headers=headers)

    if response_tv.status_code == 200:
        data = json.loads(response_tv.text)
        results=data['results']
        df_tv = pd.DataFrame(results)
        #print(df_tv.columns)
        pages[f'df_tv_{i}'] = df_tv[['id', 'original_name', 'first_air_date', 'media_type', 'adult', 'original_language', 'overview', 'popularity', 'vote_average', 'vote_count']]
        
    else:
        print(f"Error: {response.status_code}")
        
        

# Uno las paginas con 'merge' y las almaceno en 'fullpage_movie'.
fullpage_movie = pages[f'df_movie_{1}']
for i in range(1,n_pages+1):
    fullpage_movie = fullpage_movie.merge(pages[f'df_movie_{i}'], how = 'outer')

print(fullpage_movie)



# Uno las paginas con 'merge' y las almaceno en 'fullpage_tv'.
fullpage_tv = pages[f'df_tv_{1}']
for i in range(1,n_pages+1):
    fullpage_tv = fullpage_tv.merge(pages[f'df_tv_{i}'], how = 'outer')

fullpage_tv = fullpage_tv.rename(columns={'original_name': 'title', 'first_air_date':'release_date'})
print(fullpage_tv)

# Hago un merge entre la tabla de peliculas y la de tv. Ordeno la tabla segun 'vote_average'.
fullpage = fullpage_movie.merge(fullpage_tv, how = 'outer')
fullpage = fullpage.sort_values('vote_average', ascending=False)
print(fullpage)

# Los valores de la columna 'release_date' que estén vacíos, los reemplazamos por un valor genérico "default_date" para que no generen errores.
default_date = '1900-01-01'
fullpage['release_date'] = fullpage['release_date'].replace('', default_date)

# Los valores "True" y "False" de 'Adult' los reemplazamos por "1" y "0" para que se carguen correctamente a la tabla en Redshift, donde estarán en una columna de tipo INT.
fullpage['adult'] = fullpage['adult'].replace({True: 1, False: 0})


try:
    conn = psycopg2.connect(
        host=host,
        dbname=database,
        user=username,
        password=pwd,
        port='5439'
    )
    print("Connected to Redshift successfully!")
    
except Exception as e:
    print("Unable to connect to Redshift.")
    print(e)



cur = conn.cursor()
# Define el nombre de la tabla
table_name = 'trending_movie_tv_day'
# Define las columnas
columns = ['id', 'title', 'release_date','media_type','adult','original_language','overview', 'popularity', 'vote_average', 'vote_count']

values = [tuple(x) for x in fullpage.to_numpy()]
insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
# Borro cualquier dato existente en la tabla para dejarla vacía.
cur.execute("TRUNCATE TABLE trending_movie_tv_day;")
# Ejecuto el INSERT para llenar la tabla.
cur.execute("BEGIN")
execute_values(cur, insert_sql, values)
cur.execute("COMMIT")

conn.close()





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