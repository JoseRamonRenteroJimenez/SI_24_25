import pandas as pd
import numpy as np
movies = pd.read_csv(r"C:\SI_24_25\PR1\movies_metadata.csv" ,dtype={ 10 : 'str'})
credits = pd.read_csv(r"C:\SI_24_25\PR1\credits.csv")
print(credits.keys())
bruce = credits[credits["cast"] == ""]
print(bruce)

# Escribe aqui el ejercicio 1
movies["id"] = movies["id"].astype(str)
credits["id"] = credits["id"].astype(str)
movie_credits = pd.merge(movies,credits,how='inner',on=('id'))
actores = movie_credits[["title","cast"]].copy()
#display(actores.head(2))

tested = 'bruce willis'
#Hacemos una subselección de los dos campos que nos interesan y los copiamos a otro dataframe

# Nos creamos una máscara con el método applymap que nos indica que campos contienen una condición que establecemos mediante una lambda
mask = actores.applymap(lambda x:  tested.lower() in str(x).lower())
# Aplicamos la mascara para encontrar que campos nos interesan usando la función any
df1 = actores[mask.any(axis=1)]
#Any nos devuelve la fila o columna (dependiendo del axis) que al menos tenga un campo a true de la máscara. Axis 1 indica
# la columna en este caso. Si queremos devolver la fila, sería axis = 0
display(df1)