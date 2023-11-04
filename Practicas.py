import requests
import json
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates


#------------------------------------------------TRENDING - MOVIE - DAY---------------------------------------------------------
# API de The Movie Database (TMDB), página web de cine y televisión. https://www.themoviedb.org/
# En este código se recogen los datos de las películas de mayor tendencia del día.

# Cada consulta a la API recoge un máximo de 20 resultados (que constituyen una página), por lo que 
# se realizan muchas consultas iterativamente y luego se unen las tablas (o páginas) para tener un mayor conjunto de resultados en una sola tabla.


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

# Creo el diccionario 'pages' para almacenar los datos de cada página.
# n_pages: número total de páginas a leer. Máximo posible: 500.
pages = {}
n_pages = 1
for i in range(1,n_pages+1):
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
        
        
# Uno las paginas con 'merge' y las almaceno en 'fullpage'.
fullpage = pages[f'df_{1}']
for i in range(1,n_pages+1):
    fullpage = fullpage.merge(pages[f'df_{i}'], how = 'outer')

# Los valores de la columna 'release_date' que estén vacíos, los reemplazamos por un valor genérico "default_date" para que no generen errores.
default_date = '1900-01-01'
fullpage['release_date'] = fullpage['release_date'].replace('', default_date)

# Los valores "True" y "False" de 'Adult' los reemplazamos por "1" y "0" para que se carguen correctamente a la tabla en Redshift, donde estarán en una columna de tipo INT.
fullpage['adult'] = fullpage['adult'].replace({True: 1, False: 0})

#print(fullpage)

# Ordeno por fecha de estreno.
print(fullpage.sort_values(by=['release_date']))
re_pop=fullpage[['release_date', 'popularity']]

# Asegúrate de que la columna 'release_date' sea del tipo datetime
re_pop['release_date'] = pd.to_datetime(re_pop['release_date'])
# Establecer 'release_date' como índice
re_pop.set_index('release_date', inplace=True)
print(re_pop)
# Graficar
fig, ax = plt.subplots()
ax.plot(re_pop.index, re_pop['popularity'])
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gcf().autofmt_xdate()
plt.show()