import mysql.connector
import streamlit as st 

#Conexión:
conn=mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    db='mydb'
)
c = conn.cursor()

#fetch
def view_all_data():
    c.execute('select * from insurance order by id;')
    data = c.fetchall()
    return data