import fastapi
from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np
import ast
import json
from fastapi.encoders import jsonable_encoder
import pickle


# Endpoints:
# --------------------------- #
#  1 - cantidad_filmaciones_mes/{mes}
#  2 - cantidad_filmaciones_dia/{dia}
#  3 - score_titulo/{titulo_de_la_filmacion}
#  4 - votos_titulo/{titulo_de_la_filmacion}
#  5 - get_actor/{nombre_actor}
#  6 - get_director/{nombre_director}
#  7 - recomendacion/{titulo}
# --------------------------- #



#Importamos el dataframe ya procesado - Utilizado por los endpoints del 1 al 6.
df = pd.read_csv("DataSets/dataframe_final.csv")



#Importamos los archivos PKL - Utilizado por el endpoint 7
peliculas = pickle.load(open("PKL/lista_peliculas.pkl", "rb"))
similaridad = pickle.load(open("PKL/similaridad.pkl", "rb"))

#Instanciamos en una variable.
app = FastAPI()

#Mensaje de Bienvenida.
@app.get("/")
def inicio():
        return "Bienvenido al proyecto de MLOps"

#Endpoints.
# 1) cantidad_filmaciones_mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    
 
    """
    Funcion creada para retornar la cantidad de peliculas que fueron estrenadas en el mes consultado.
    Siendo el idioma predefinido de la mayoria de los IDE en ingles, se crean 2 listas una que contiene
    los meses del año en ingles y otra con los meses del año en español, ya que son listas paralelas por
    medio de un index generado por el mes ingresado en español hacemos un cambio para asi poder obtener 
    el total de peliculas estrenadas en el mes ingresado en español.
    
    Args:
        mes: Es el nombre del mes del año en español por el cual se realizara la busqueda.
    """
    
    
    meses_esp = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    meses_ing = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    mes = mes.title() #Mes con la primera letra en mayuscula
    #Index
    if mes in meses_esp:
        indice_ing = meses_esp.index(mes) #Indice del mes en español
        conversion_mes = meses_ing[indice_ing] #Conversion del index para extraer el mes en ingles
    else:
        return f'{mes} no es un mes'
    
    encontrado = False #Comodin
    
    for indice, elemento in enumerate(meses_esp):
        if mes == elemento:
            encontrado = True
            break
    cantidad_mes = df[df["release_month"]== conversion_mes].shape[0]

    if encontrado:
        return {'mes': mes, "cantidad": cantidad_mes}


# 2) cantidad_filmaciones_dia
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    
    
    """
    Funcion creada para retornar la cantidad de peliculas que fueron estrenadas en el dia consultado.
    Siendo el idioma predefinido de la mayoria de los IDE en ingles, se crean 2 listas una que contiene
    los dias de la semana en ingles y otra con los dias de la semana en español, ya que son listas paralelas por
    medio de un index generado por el dia ingresado en español hacemos un cambio para asi poder obtener 
    el total de peliculas estrenadas en el dia ingresado en español.
    
    Args:
        dia: Es el nombre del dia de la semana en español por el cual se realizara la busqueda.
    """
    
    
    dia = dia.title()
    #Listas
    dias_esp = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    dias_ing = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    #Index
    if dia in dias_esp:
        indice_ing = dias_esp.index(dia) #Indice del mes en español
        conversion_dia = dias_ing[indice_ing] #Conversion del index para extraer el mes en ingles
    elif dia == "":
            return (f'El campo no puede quedar vacio')
    else:
        return f'{dia} no es un dia'
    
    encontrado = False #Comodin

    for indice, elemento in enumerate(dias_esp):
        if dia == elemento:
            encontrado = True
            break
   
    estrenos_dia = df[df["release_day"] == conversion_dia].shape[0]
   
    if encontrado:
        return {"dia": dia, "cantidad": estrenos_dia}


# 3) score_titulo
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    
    
    """
    Esta funcion realiza el procedo de encontrar un titulo dentro de la columna 'title':
    En caso de encontrar la coincidencia retorna el nombre del titulo, año de estreno y popularidad del mismo.
    En caso no se encuentre el titulo o el campo este vacio la funcion retorna un mensaje para hacer saber
    que algo no esta bien.

    Args:
        titulo_de_la_filmacion: Es el nombre del titulo por el cual se realizara la busqueda.
    """
    
    
    titulo_de_la_filmacion = titulo_de_la_filmacion.title()
    encontrado = False

    for indice, elemento in enumerate(df["title"]):
        if titulo_de_la_filmacion == elemento:
            encontrado = True
            break
        
    anio_estreno = df.loc[indice, "release_year"]
    popularidad = df.loc[indice, "popularity"]
    anio_estreno = int(anio_estreno)
    popularidad = float(popularidad)

    if encontrado:
        return {"titulo": titulo_de_la_filmacion, "anio": anio_estreno ,"popularidad":popularidad}
    

# 4) votos_titulo
@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    """
    Funcion creada para retornar por medio del titulo el año de estreno, valoraciones y promedio de votos.
    Args:
        titulo_de_la_filmacion (_type_): _description_
    """
    

    titulo_de_la_filmacion = titulo_de_la_filmacion.title()
    encontrado = False

    for indice, elemento in enumerate(df["title"]):
        if titulo_de_la_filmacion == elemento:
            encontrado = True
            break

    votos = df.loc[indice, "vote_count"]
    promedio_votos = df.loc[indice, "vote_average"]
    anio = df.loc[indice, "release_year"]
    votos = int(votos)
    promedio_votos = float(promedio_votos)
    anio = int(anio)

    if encontrado and votos > 2000:
        return {'titulo':titulo_de_la_filmacion, 
                "anio": anio,
                "voto_total": votos,
                "voto_promedio": promedio_votos
                }
    elif encontrado and votos < 2000:
        return None


# 5) get_actor
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    """
    Funcion creada para retornar la cantidad de filmaciones hechas, el retorno y promedio de retorno por filmacion.
    Para retornar se utiliza el parametro nombre_actor

    Args:
        nombre_actor: nombre del actor para realizar la busqueda

    """
    df.cast=df.cast.fillna(" ")
    nombre_actor = nombre_actor.title()
    apariciones = 0
    indice_actor = []
    #Obtener indices y contar las apariciones del mismo.
    for indice, elemento in enumerate(df.cast):
        if nombre_actor in df.cast[indice]:
            apariciones+=1
            indice_actor.append(indice)
            # print(indice, actor, apariciones)
            
    retorno = df.loc[indice_actor, ["return"]].sum()[0]
    retorno_promedio = df.loc[indice_actor, ["return"]].mean()[0]

    return {'actor':nombre_actor, 'cantidad_filmaciones':apariciones, 'retorno_total':retorno, 'retorno_promedio':retorno_promedio}


# 6) get_director
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):

    nombre_director = nombre_director.title()
    indice_director = []

    for indice, elemento in enumerate(df.director):
        if nombre_director in df.director[indice]:
            indice_director.append(indice)
            # print(indicpipe, elemento)
     
    retorno_total = df.loc[indice_director, "return"].sum()        
    titulo = df.loc[indice_director, "title"]
    retorno_individual = df.loc[indice_director, "return"]
    fecha_lanzamiento = df.loc[indice_director, "release_date"]
    costo = df.loc[indice_director, "budget"]
    ganancia = df.loc[indice_director, "revenue"]  

    return {'director':nombre_director, 
            'retorno_total_director':retorno_total, 
            'peliculas':titulo, 
            'anio':fecha_lanzamiento, 
            'retorno_pelicula':retorno_individual, 
            'budget_pelicula':costo, 
            'revenue_pelicula':ganancia}   


# 7) recomendacion
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    titulo=titulo.title()
    indice = df[df["title"] == titulo].index[0]
    distancia = sorted(list(enumerate(similaridad[indice])), reverse=True, key=lambda vector:vector[1])
    lista_peliculas = []
    for i in distancia[1:6]:
        lista_peliculas.append(df.iloc[i[0]].title)
    
    return lista_peliculas
                   
        


        
       
        
        
