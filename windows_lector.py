#!/usr/bin/env python
# coding: utf-8

# In[1]:


import serial
import re
from datetime import datetime
import time
from tqdm import tqdm
import psycopg2 as psy


# In[2]:


def fluo_read():
    # Establish the connection on a specific port
    s = serial.Serial('COM3',57600)
    data = []
    now = str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    data.append(now)

    for i in range (2):
        data.append(s.readline())

    data = [str(dato, 'utf-8') for dato in data]
    data = [re.split("\r", dato) for dato in data]
    data = data[-1][-1]
    data = re.split(", ", data)
    data = data[:3]
    print(data)
    return data


# In[ ]:


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



# In[ ]:
