# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 20:56:01 2020

@author: Tashan Tika
"""

# CREATE TABLE IF NOT EXISTS app_user (
#   username varchar(45) NOT NULL,
#   password varchar(450) NOT NULL,
#   enabled integer NOT NULL DEFAULT '1',
#   PRIMARY KEY (username)
# )

# pip install psycopg2

# source: https://www.postgresqltutorial.com/postgresql-python/connect/
import psycopg2
from sqlalchemy import create_engine
# conn = psycopg2.connect(
#     host="localhost",
#     database="Housing_Rational",
#     

# cur = conn.cursor()
# # xecute a statement
# print('PostgreSQL database version:')
# cur.execute('SELECT version()')

# # display the PostgreSQL database server version
# db_version = cur.fetchone()
# print(db_version)
   
# 	# close the communication with the PostgreSQL
# cur.close()


engine = create_engine('postgresql+psycopg2://postgres:@localhost:5432/Housing_Rational')
# /username:password@host:port/database

import pandas as pd
import config_p24
sta_df = pd.read_excel(config_p24.coordinates)
#df = sta_df.iloc[:,3:]
sta_df.to_sql('coordinates', engine, if_exists='append', index=False)
myQuery = "SELECT * FROM coordinates"
df_read = pd.read_sql_query(myQuery, engine)



