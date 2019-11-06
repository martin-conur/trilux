#!/usr/bin/python

from time import sleep
import serial
import re
import pandas as pd
import matplotlib.pyplot as plt
import re
import psycopg2 as psy
import numpy as np
from datetime import date
import datetime
import csv, pyodbc

def fluo_read():
    # Establish the connection on a specific port
    s = serial.Serial('/dev/ttyUSB0',9600)
    data = []
    for i in range (2):
        data.append(s.readline())

    data = [str(dato, 'utf-8') for dato in data]
    data = [re.split("\r", dato) for dato in data]
    data = data[-1][-1]
    data = re.split(", ", data)
    data = data[:3]
    print(data)
    return data



def insert_data(chla,tby,pc):
    conn = None
    try:
        conn = psy.connect(host="salt.db.elephantsql.com",
                           user="aeaudjwo", password="5uHoUq62gU5BoS2HvJQH0ogSw_94nxCE")

        c = conn.cursor()

        fecha = str(datetime.datetime.now())[:16]

        c.execute("""INSERT INTO trilux (
                    fecha,
                    chla,
                    tby,
                    pc) VALUES (%s,%s,%s,%s)""",(fecha,float(chla),float(tby),float(pc)))
        conn.commit()
        conn.close()

    except (Exception, psy.DatabaseError) as error:
        print (error)

    finally:
        if conn is not None:
            conn.close()


while True:
  chla, tby, pc = fluo_read()
  print("Iniciando actualización al servidor: " + str(datetime.datetime.now())[:16])
  insert_data(chla, tby, pc)
  print("Actualización completada a las: " + str(datetime.datetime.now())[:16])

  sleep(600)
