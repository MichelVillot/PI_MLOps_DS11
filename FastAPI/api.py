#Importamos todas las librerias necesarias para poder trabajar con nuestros dataset.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ast
import json
import time
#Importamos el dataset_final
archivo = pd.read_csv(r"C:\Users\miche\OneDrive\Escritorio\Proyecto_MLOps\dataframe_final.csv", parse_dates=["release_date"])
df = pd.DataFrame(archivo)


def cantidad_filmaciones_mes(mes):
    
    
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
    indice_ing = meses_esp.index(mes) #Indice del mes en español
    conversion_mes = meses_ing[indice_ing] #Conversion del index para extraer el mes en ingles
    encontrado = False #Comodin
    
    for indice, elemento in enumerate(meses_esp):
        if mes == elemento:
            encontrado = True
            break
        
    if encontrado:
        return f'{df[df["release_month"]== conversion_mes].shape[0]} peliculas fueron estrenadas en el mes de {mes}'



def cantidad_filmaciones_dia(dia):
    
    
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
    indice_ing = dias_esp.index(dia) #Indice del mes en español
    conversion_dia = dias_ing[indice_ing] #Conversion del index para extraer el mes en ingles
    encontrado = False #Comodin

    for indice, elemento in enumerate(dias_esp):
        if dia == elemento:
            encontrado = True
            break
   
    estrenos_dia = df[df["release_day"] == conversion_dia].shape[0]
   
    if encontrado:
        return f'{estrenos_dia} peliculas fueron estrenadas el dia {dia}'
    elif not encontrado:
        if dia == "":
            return (f'El campo no puede quedar vacio')
        elif dia != elemento:
            return (f"El dia {dia} no se encontro en nuestra base de datos")


def score_titulo(titulo_de_la_filmacion):
    
    
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

    if encontrado:
        return f'La pelicula {titulo_de_la_filmacion} fue estrenada en el año {anio_estreno} con un score/popularidad de {popularidad}'
    elif not encontrado:
        if titulo_de_la_filmacion == "":
            return (f'El campo no puede quedar vacio')
        elif titulo_de_la_filmacion != elemento:
            return (f"El titulo {titulo_de_la_filmacion} no se encontro en nuestra base de datos")
        


def votos_titulo(titulo_de_la_filmacion):
    """
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

    if encontrado and votos > 2000:
        return f'La pelicula {titulo_de_la_filmacion} fue estrenada en el año {anio}. La misma cuenta con un total de {int(votos)} valoraciones, con un promedio de {promedio_votos}'
    elif encontrado and votos < 2000:
        return f"La pelicula {titulo_de_la_filmacion} no cumple con el requisitos de 2000 valoraciones"
   

def get_actor(nombre_actor):
    """_summary_

    Args:
        nombre_actor (_type_): _description_

    Returns:
        _type_: _description_
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

    return (f'El actor {nombre_actor} ha participado de {apariciones} cantidad de filmaciones, el mismo ha conseguido un retorno de {round(retorno,3)} con un promedio de {round(retorno_promedio,3)} por filmacion')


def get_director(nombre_director):

    nombre_director = nombre_director.title()
    indice_director = []

    for indice, elemento in enumerate(df.director):
        if nombre_director in df.director[indice]:
            indice_director.append(indice)
            # print(indice, elemento)

    todo_director = df.loc[indice_director ,["title", "release_date", "return", "budget", "revenue"]]
    titulo = df["title"]
    fecha_lanzamiento = df["release_date"]
    retorno = df["return"]
    presupuesto = df["budget"]
    ganancia = df["revenue"]

    decision = int(input("1 para print y 2 para dataframe"))
    if decision == 1:
        for ind in indice_director:
            print(f"El director {nombre_director} ha dirigido la pelicula {titulo[ind]}, fecha de lanzamiento {fecha_lanzamiento[ind].date()} un retorno de {retorno[ind]}, costo {presupuesto[ind]} y una ganancia de {ganancia[ind]}")
    elif decision == 2:
        print(f"El director {nombre_director} ha dirigido las siguientes peliculas:")
        return todo_director
