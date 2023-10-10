import requests
import json
import pprint
import pandas as pd


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

# Configura los parámetros de la solicitud
params = {
    "api_key": api_key, "query":movie
}

# Realiza la solicitud GET
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    #pprint.pprint(data)
    df = pd.DataFrame(data)
    df.columns
    
else:
    print(f"Error: {response.status_code}")
