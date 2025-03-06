# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:27:24 2020
Sourced and based on: https://www.postgresqltutorial.com/postgresql-python/
Database setup Insert, connect and select
@author: Dominik
"""

from datetime import datetime
import psycopg2

def database_conn():
    username="postgres"
    password =""
    host=""
    database ="postgres"
    
    global connection
    global cursor
    try:
        
        connection=psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    database=database)
       
        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

        
def database_select(serial_number):
    try:
        postgreSQL_select_Query = "select * from serial_num where serial = %s"
        cursor.execute(postgreSQL_select_Query, (serial_number,))
        
        serial_num = cursor.fetchall() 
        
        print("Print each row and it's columns values")
        for row in serial_num:
            print("\n")
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print("\n")
            
            #Return originality,value,timestamp
            return(row[2])
        
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

def database_insert(serial_number,real_note,value):
    dt = datetime.now()
    try:
        insert_query = '''INSERT INTO serial_num (ORIGINAL, VALUE, TIME, SERIAL) VALUES (%s,%s,%s,%s)'''
        record_insert = (real_note , value , dt, serial_number)
        
        cursor.execute(insert_query,record_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into table")
        database_select()
    except (Exception, psycopg2.Error) as error :
        if(connection):
            connection.rollback()
            print("Failed to insert record into table", error)
            database_select(serial_number)
            
def connection_close():
     if (connection):
         try:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")
         except:
            print("Connection already closed?")
