# importing libaries
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import os

# getting user pass from env variables
username = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASS')

# connect to mysql server
connection=pymysql.connect(
    host='localhost',
    user=username,
    password=password,
    local_infile=True,
    )
cursor=connection.cursor()
cursor.execute('SET GLOBAL local_infile = TRUE;')

# read csv into dataframe
df=pd.read_csv('data.csv')

# create table command using datafram headers
cmd='create table data01 ('
for c in df.columns:
    cmd+=c+' char(25), '
cmd=cmd[:-2]+');'

# create database
try:
    cursor.execute('create database data01;')
except:
    pass
cursor.execute('use data01;')

# drop the table and create it again
try:
    cursor.execute('drop table data01;')
except:
    pass
cursor.execute(cmd)

# import data in the database table
cursor.execute("LOAD DATA local INFILE 'data.csv' INTO TABLE data01 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")

# retrieve data from databse table and make a plot
data=pd.read_sql('select * from data01;',connection)
plt.figure(figsize=(12,8))
data.car_make.value_counts().plot(kind='bar')
plt.tight_layout()
plt.savefig('carmake-barchart.jpg')