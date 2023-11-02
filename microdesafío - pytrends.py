import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
pytrends = TrendReq(retries=3)
keywords = ["Fin del mundo", "Calentamiento global", "Terremoto",'Tsunami']
pytrends.build_payload(keywords, cat=0, geo='', gprop='') # Datos de los ultimos 5 años
stop_queries = pytrends.interest_over_time()[keywords]
print(stop_queries.head())

stop_queries.plot(kind='line',figsize=(12,6), xlabel='Fecha',ylabel='Interés de audiencia',title='Interés en el tiempo')
plt.show()