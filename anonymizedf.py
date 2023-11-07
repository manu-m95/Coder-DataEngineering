import pandas as pd
from anonymizedf.anonymizedf import anonymize

df= pd.read_csv('Datos_Microdesafio_Semana8_DE.csv',sep=';')
print(df.head(12))

# Preparo el dataframe
an = anonymize(df)

fake_df = (
    an
    .fake_names("Comisionado", chaining=True)
    .fake_dates("Fecha", chaining=True)
    .fake_whole_numbers("Telefono", chaining=True)
    .show_data_frame()
)
print(fake_df)

#print(fake_df.columns)

# Elijo las columnas que quiero subir a la base de datos, las falsas. Renombro las columnas.
df_final=fake_df[['Pais ','Fake_Comisionado','Reduccion_CO2','Incrmento_P','Inversion_arboles',
                  'Fake_Fecha','Fake_Telefono']]
df_final.columns=[['Pais ', 'Comisionado', 'Reduccion_CO2', 'Incrmento_P',
                   'Inversion_arboles', 'Fecha', 'Telefono',]]
print(df_final)