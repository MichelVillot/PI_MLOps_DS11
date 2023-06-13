# Labs - Proyecto Data Engineer - Proyecto Integrador 1
Michel Villot - Cohorte Data Science 11.

Junio 2023

# Rol a Desarrollar
Se nos presenta la oportunidad de empezar a trabajar como `Data Scientist` para una startup que provee servicios de agregacion de plataformas de streaming. Nuestra labor es poner en marcha un modelo de ML el cual permita realizar recomendaciones a los usuarios.

Para poder realizar nuestro trabajo nos han entregado los siguientes datasets:
* movies_dataset.csv
* credits.csv

# Presentacion del Proyecto 📽️
Seguiremos los siguientes pasos para realizar nuestro trabajo de forma eficiente: 
1) Realizar un proceso de ETL, para poder obtener una data de calidad con la cual podamos trabajar de forma eficiente y sin errores.
2) Proceder a realizar un EDA para obtener patrones, insights e informacion relevante que nos pueda ayudar para comprender el comportamiento de los usuarios.
3) Poner en marcha nuestro sistema de recomendaciones basado en un modelo de Machine Learning.

# Transformaciones 💻
`ETL`:
 1. Procedemos a desanidar la informacion de todas las columnas que se encuentran con un mal formato en el dataset `movies_dataset.csv` para poder trabajar. Las cuales son las siguientes: `belongs_to_collection, genres, production_companies, production_countries y spoken_languages`.
 2. Se procede a crear columnas por separadas de los desanidadas para obtener un formato aceptable para poder trabajar (nos basamos en las FN) las cuales son: `id_genres, name_genres, id_production_companies, name_production_companies, name_production_countries, name_spoken_languages`.
 3. Relleno de los valores nulos de las columnas `revenue` y `budget` con el numero 0.
 4. Eliminacion de los campos que contengan valores nulos en la columna `release_date`.
 5. Eliminacion de los registros con los indices `19730, 29503, 35587` ya que los mismos tenian un gran cantidad de datos faltantes o errores en sus columnas.
 6. Cambio de formato a `AAAA-mm-dd` en la columna `release_date`.
 7. Creacion de la columna `release_year` la cual contiene el año en que se produjo la pelicula.
 8. Creacion de las columnas `release_month` la cual contiene el mes en que se produjo la pelicula (en ingles).
 9. Creacion de las columnas `release_day` la cual contiene el dia en que se produjo la pelicula (en ingles).
 10. Verificacion y eliminacion de los duplicados en la columna `id` de ambos datasets.
 11. Eliminacion de las columnas solicitadas por el proyecto: `video, imdb_id, adult, original_title, poster_path, homepage`.
 12. Eliminacion de las columnas `belongs_to_collection, genres, production_companies, production_countries, spoken_languages` ya que tenemos todas las creadas para poder trabajar cada registro por sepadado.
 13. Procedemos a desanidar la informacion de todas las columnas que se encuentran con un mal formato en el dataset `credits.csv` para poder trabajar. Las cuales son las siguientes: `cast, crew`. 
 14. Realizamos un cambio de nombre de `crew` a `director`
 15. Hacemos un merge de ambos datasets por el `id` para obtener uno el cual tiene por nombre `dataframe_final.csv`.
 16. Exportamos el archivo con el nombre `dataframe_final.csv`.

`EDA`: Ahora que tenemos nuestros datasets limpios procedemos a buscar informacion relevante.
1. Como primer paso obtuvimos las estadisticas basicas del dataset para tener una idea del mismo asi como ver la cantidad de columnas y dtype de las mismas.
2. Verificamos la cantidad de valores faltantes o nulos
3. Imputacion de los valores nulos o faltantes.
4. Analisis univariable (con graficos)
5. Para realizar un estudio de variables como lo son `revenue` o `budget` se realiza una conversion a miles de millones para que los graficos sea entendibles.
6. Analisis bivariable (con graficos)
7. Cabe destacar que abajo de cada grafico se tiene cada `insight` extraido del mismo.
 
 
`Sistema de Recomendaciones`:
Para el sistema de recomendaciones se utilizaron solo 5mil registros del total de nuestro dataset (45mil), esto debido a que el deploy estaba teniendo errores para poder renderizar y por ende no obteniamos el resultado deseado.

# Deploy
El deploy fue realizado en la plataforma Render, simulando una API (FastApi) para el consumo de cualquier persona externa.
Link: https://labs-mlops.onrender.com/docs

El deploy esta asociado al archivo `main.py` el cual contiene todos los endpoints solicitados para hacer el MVP.

# Manual de Funcionamiento de los endpoints en el Deploy
`Endpoints - Informacion`: 

`Importante`: Tener en cuenta que cualquier endpoint (o funciones) que en su consulta tenga espacios los mismos deben ser reemplazados por %20.

`Ejemplo`: https://labs-mlops.onrender.com/score_titulo/Father%20of%20the%20bride%20part%20II , como podemos ver cada espacio en el URL fue reemplazado por %20

`Endpoints`
*  /cantidad_filmaciones_mes/{mes}:          
   https://labs-mlops.onrender.com/cantidad_filmaciones_mes/mes_escrito_en_español > Donde `mes_escrito_en_español` es el mes que queremos consultar.
   
   Ejemplo de acceso directo:
   https://labs-mlops.onrender.com/cantidad_filmaciones_mes/enero > retorna todas las peliculas estrenadas en el mes de `enero`
   
   
*  /cantidad_filmaciones_dia/{dia}:                       
   https://labs-mlops.onrender.com/cantidad_filmaciones_dia/dia_escrito_en_español > Donde `dia_escrito_en_español` es el dia de la semana que queremos consultar.
   
   Ejemplo de acceso directo:
   https://labs-mlops.onrender.com/cantidad_filmaciones_dia/lunes > retorna todas las peliculas estrenadas en el dia `lunes`
    
    
*  /score_titulo/{titulo_de_la_filmacion}:
   https://labs-mlops.onrender.com/score_titulo/titulo_de_la_pelicula > Donde `titulo_de_la_pelicula` es el titulo de la pelicula que deseamos consultar.
  
   
   Ejemplo de acceso directo:
   https://labs-mlops.onrender.com/score_titulo/toy%20story > retorna el score/popularidad de la pelicula`Toy Story`


*  /votos_titulo/{titulo_de_la_filmacion}:
   https://labs-mlops.onrender.com/votos_titulo/titulo_de_la_pelicula > Donde `titulo_de_la_pelicula` es el titulo de la pelicula que deseamos consultar.
   
    
   Ejemplo de acceso directo:
   https://labs-mlops.onrender.com/votos_titulo/the%20godfather > retorna la cantidad de votos que posee la pelicula `The Godfather`


*  /get_actor/{nombre_actor}:
   https://labs-mlops.onrender.com/get_actor/nombre_del_actor > Donde `nombre_del_actor` es el nombre del actor que deseamos consultar.
   
   Ejemplo:
   https://labs-mlops.onrender.com/get_actor/robin%20williams > retorna cantidad de peliculas, retorno total y retorno promedio de `Robin Williams`

*  /get_director/{nombre_director}:
   https://labs-mlops.onrender.com/get_director/nombre_del_director > Donde `nombre_del_director` es el nombre del director que deseamos consultar.
   
   Ejemplo:
   https://labs-mlops.onrender.com/get_director/james%20cameron > retorna la informacion general de `James Cameron`

*  /recomendacion/{titulo}:
   https://labs-mlops.onrender.com/recomendacion/titulo_de_la_pelicula > Donde `nombre_del_director` es el nombre del director que deseamos consultar.
   
   Ejemplo:
   https://labs-mlops.onrender.com/recomendacion/toy%20story > retorna una lista con las 5 peliculas similares para el titulo `Toy Story`

# Video

Link del Video:

# Estructura del Repositorio

* `Directorios`
* `DataSets`: Contiene los datasets utilizados durante todo el proyecto e incluye los archivos: credits. csv, credits_final.csv, dataframe_final.csv, movies_dataset.csv
* `FastApi`: Contiene los archivos necesarios para el deploy de nuestros endpoits de manera local.
* `Notebooks`: Contiene todos los archivos procesados y utilizados durante nuestro proyecto.
  * EDA.ipynb > Aqui se encuentra todo el proceso EDA
  * ETL.ipynb > Aqui se encuentra todo el proceso de ETL
  * Funciones_API.ipynb > Aqui se encuentran todas las funciones necesarias para nuestros endpoints
  * Sistema_Recomendaciones.ipynb > Aqui se encuentra el sistema de recomendaciones.
* `PKL`: Contiene los archivos necesarios para nuestro sistema de recomendaciones.
  * lista_peliculas.pkl > Contiene el set de peliculas utilizado para el sistema de recomendaciones
  * similaridad.pkl > Contiene el vector de similaridad de cada pelicula con respecto a otro para ser utilizado por el sistema de recomendaciones

* `Archivos`
* `.gitignore`: Archivo relacionado con git
* ` README.md`: Archivo con toda la informacion del proyecto
* `main.py`: Archivo para poder inicializar nuestro deploy de forma remota, en este caso contiene todos los endpoints para realizar las consultas.
* `requirements.txt`: Archivo el cual contiene las versiones usadas durante el proceso para poder levantar el deploy.

# Requerimientos del Proyecto:
Los requerimientos del proyecto solicitados por Henry se pueden encontrar en el siguiente link: https://github.com/HX-PRomero/PI_ML_OPS/blob/main/Readme.md
