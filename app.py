from concurrent.futures import process
from decouple import config
from bs4 import BeautifulSoup
import requests
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import logging 
from datetime import datetime
import os
from settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

file_handler = logging.FileHandler('main.log') 
file_handler.setFormatter(formatter) 

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter) 

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


hoy = '{:%d-%m-%Y}'.format(datetime.today())
mes = meses[(int(datetime.today().month))-1] #Lista 'meses' importada desde settings.
anio = hoy[-4:]
main_dir = str(os.getcwd())

names = list(category.keys())
URLs = list(category.values())


# Descarga los datos fuente y los almacena de forma local.'
def get_csv(name, URL):

    data_prueba = requests.get(URL)
    soup = BeautifulSoup(data_prueba.content, 'html.parser')
    tags = soup.find_all('a', class_='btn btn-green btn-block')
    exc = False
    try:
        for tag in tags:
            
            link = tag.get('href')
            if name in link:
                exc = True
                csv_data = requests.get(link).content
                # print(type(csv_data))
                if os.path.exists(f'{main_dir}/{name}s/{anio}-{mes}') == True:
                    os.chdir(f'{main_dir}/{name}s/{anio}-{mes}')
                else:
                    os.makedirs(f'{main_dir}/{name}s/{anio}-{mes}')
                    logger.info(f'Directorio {name}s/{anio}-{mes} creado exitosamente')
                    os.chdir(f'{main_dir}/{name}s/{anio}-{mes}')
                with open(f'{name}s-{hoy}.csv', 'wb') as file:
                    file.write(csv_data)
                    logger.info(f'archivo {name}s-{hoy}.csv adquirido' )
                os.chdir(main_dir)
        if exc == False:
            raise ValueError(f'No se encontraron datos disponibles. Revisar enlace de {name}s en .env')            
    except Exception as e:
        logger.error(e)

# Se procesan los datos de los .csv y se les da formato para devolver las DataFrames.

def process_data():
    '''''''''
      Retorna:
      dataf1, dataf2, dataf3
    '''
    
    get_csv(names[0], URLs[0])
    get_csv(names[1], URLs[1])
    get_csv(names[2], URLs[2])


    museos_dataf = pd.read_csv(f'{names[0]}s/{anio}-{mes}/{names[0]}s-{hoy}.csv', engine='python')
    museos_dataf.drop(columns = museos_drop , axis =1, inplace=True)
    museos_dataf.reindex(columns = nombres_columnas)
    museos = museos_dataf.rename(columns = museos_newname, inplace = False)
     
    
    
    cine_dataf = pd.read_csv(f'{names[1]}s/{anio}-{mes}/{names[1]}s-{hoy}.csv', engine='python')
    cine_to_drop = cine_dataf.drop(columns = cine_drop, axis = 1 ,inplace=False)
    cine_to_drop.reindex(columns = nombres_columnas)
    cine = cine_to_drop.rename(columns = cine_newname ,inplace = False)
 
    
    
    biblioteca_dataf=pd.read_csv(f'{names[2]}s/{anio}-{mes}/{names[2]}s-{hoy}.csv', engine='python')
    biblioteca_dataf.drop(columns = biblioteca_drop, axis = 1,inplace=True)
    biblioteca_dataf.reindex(columns = nombres_columnas)
    biblioteca = biblioteca_dataf.rename(columns = biblioteca_newname ,inplace = False)
    
    dataf = pd.concat([museos, cine, biblioteca], ignore_index=True)
    dataf1 = dataf.drop(columns = 'fuente')
    a = pd.DataFrame(dataf.groupby('categoría').count().sum())
    b = pd.DataFrame(dataf.groupby('fuente').count().sum())
    c = pd.DataFrame(dataf.groupby(['provincia','categoría']).count().sum())
    dataf2 = pd.concat([a, b, c], axis=1, keys=['registros totales por categoría', 'registros totales por fuente', 'registros por categoría y provincia'])
    tabla_cine = cine_dataf[['Provincia','Pantallas','Butacas','espacio_INCAA']]
    dataf3 = tabla_cine.groupby(['Provincia']).count()

    return (dataf1, dataf2, dataf3)


try:
  dataf1, dataf2, dataf3 = process_data()
  logger.info('Datos Procesados')

except Exception as e:
  logger.error(e)


# Conexion a Base de Datos

def get_database():
    '''''''''
    Retorna:
        engine
    '''
    try:
        engine = get_engine(DBsettings['pguser'],
                      DBsettings['pgpasswd'],
                      DBsettings['pghost'],
                      DBsettings['pgport'],
                      DBsettings['pgdb'])
        logger.info('Conectado a la base de datos PostgreSQL!')
    except IOError:
        logger.exception('Error al tratar de conectarse a la base de datos!')
        return None, 'fail'
    return engine

def get_engine(user, passwd, host, port, db):
    '''''''''
    Obtiene el Engine de la base de datos PostgreSQL.
    Retorna:
        engine de la base de datos
    '''
    url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=user, passwd=passwd, host=host, port=port, db=db)

    engine = create_engine(url)
    return engine

def get_session():
    '''''''''
    Return an SQLAlchemy session
    Input:
        engine: an SQLAlchemy engine
    '''
    engine = get_database()
    session = sessionmaker(bind=engine)()

    return engine, session

bd, session = get_session()
Base = declarative_base()


# Actualización de la base de Datos. 

def delete_table(session, tabla):
  sql = 'DROP TABLE %s' %tabla
  crsr = session.bind.raw_connection().cursor()
  crsr.execute(sql)
  session.commit()

def db_update():
    '''
    Actualiza la información de las tablas en la base de datos. 
    '''
    try:
        timemark = [f'{hoy}']*len(dataf1)
        dataf1['fecha'] = timemark
        dataf1.to_sql('tabla_1', bd, if_exists = 'replace')
        timemark = [f'{hoy}']*len(dataf2)
        dataf2['fecha'] = timemark
        dataf2.to_sql('tabla_2', bd, if_exists = 'replace')
        timemark = [f'{hoy}']*len(dataf3)
        dataf3['fecha'] = timemark
        dataf3.to_sql('tabla_3', bd, if_exists = 'replace')
        logger.info('La base de datos ha sido actualizada')
    except Exception as e:
        logger.error(e)

db_update()
if __name__ == '__main__':
  Base.metadata.drop_all(bd)
  Base.metadata.create_all(bd) 

