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

last_temp = 0
last_state = ''
last_target = ''


with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()
    cursor.execute(drop_table)
    cursor.execute(query_create_table)
    conn.commit()
    cursor.execute(query_create_hypertable)
    conn.commit()
    cursor.close()

def insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val):
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(id_val)+"', current_timestamp,"+str(last_temp)+",'"+str(last_state)+"',"+str(last_target)+")")
    conn.commit()
    cursor.close()

class time_handler(object):
    def datachange_notification(self, node, val, data):
        insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val)

class temp_handler(object):
    def datachange_notification(self, node, val, data):
        global last_temp
        last_temp = val

class state_handler(object):
    def datachange_notification(self, node, val, data):
        global last_state
        last_state = val

class target_handler(object):
    def datachange_notification(self, node, val, data):
        global last_target
        last_target = val

client = Client(config.URL)
try:
    client.connect()
    print("Client connected")
except:
    print('Error connecting to server')
else:
    time_value = client.get_node('ns=2;s="V1_Ti"')
    id = client.get_node('ns=2;s="V1_Id"')
    temp = client.get_node('ns=2;s="V1_Te"')
    state = client.get_node('ns=2;s="V1_St"')
    temp_max = client.get_node('ns=2;s="V1_Tmax"')
    temp_min = client.get_node('ns=2;s="V1_Tmin"')
    target = client.get_node('ns=2;s="V1_Tar"')
    id_val = id.get_value()
    last_temp = temp.get_value()
    last_state = state.get_value()
    last_target = target.get_value ()
    temp_max_val = temp_max.get_value()
    temp_min_val = temp_min.get_value()

    handler_time = time_handler()
    sub_time = client.create_subscription(500, handler_time)
    handle_time = sub_time.subscribe_data_change(time_value)

    handler_temp = temp_handler()
    sub_temp = client.create_subscription(500, handler_temp)
    handle_temp = sub_temp.subscribe_data_change(temp)

    handler_state = state_handler()
    sub_state = client.create_subscription(500, handler_state)
    handle_state = sub_state.subscribe_data_change(state)

    handler_target = state_handler()
    sub_target = client.create_subscription(500, handler_target)
    handle_target = sub_target.subscribe_data_change(target)
    
    # sub.unsubscribe(handle)
    # print('Client disconnected')
    # client.disconnect





