from opcua import Client
import time
import docker.config as config
from warnings import catch_warnings;
import psycopg2
import random
import json

CONNECTION = "postgres://"+config.username+":"+config.password+"@"+config.host+":"+config.port+"/"+config.dbName
query_create_table = "CREATE TABLE therm (id VARCHAR (10), datetime TIMESTAMP, temp FLOAT, state VARCHAR (10), target INTEGER);"
query_create_hypertable = "SELECT create_hypertable('therm', 'datetime');"
drop_table = "DROP TABLE therm;"

with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()
    cursor.execute(drop_table)
    cursor.execute(query_create_table)
    conn.commit()
    cursor.execute(query_create_hypertable)
    conn.commit()


class temp_handler(object):
    def datachange_notification(self, node, val, data):
        insert_value(id.get_value, val, state.get_value, target.get_value)


client = Client(config.URL)
try:
    client.connect()
    print("Client connected")
except:
    print('Error connecting to server')
else:
    id = client.get_node('ns=2;s="V1_Id"')
    temp = client.get_node('ns=2;s="V1_Te"')
    timeValue = client.get_node('ns=2;s="V1_Ti"')
    state = client.get_node('ns=2;s="V1_St"')
    temp_max = client.get_node('ns=2;s="V1_Tmax"')
    temp_min = client.get_node('ns=2;s="V1_Tmin"')
    target = client.get_node('ns=2;s="V1_Tar"')

    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(id.get_value)+"', current_timestamp,"+str(temp.get_value)+",'"+str(state.get_value)+"',"+str(target.get_value)+")")
    conn.commit()

    handler = temp_handler()
    sub = client.create_subscription(500, handler)
    handle = sub.subscribe_data_change(temp)

    
    # sub.unsubscribe(handle)
    # print('Client disconnected')
    # client.disconnect


def insert_value(id, temp, state, target):
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (datetime, temp, state) VALUES ('"+str(id)+"', current_timestamp,"+str(temp)+",'"+str(state)+"',"+str(target)+")")
    conn.commit()


