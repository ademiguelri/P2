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

node_id = 'ns=2;s=V1_Id'
node_temp = 'ns=2;s=V1_Te'
node_state = 'ns=2;s=V1_St'
node_temp_max = 'ns=2;s=V1_Tmax' 
node_temp_min = 'ns=2;s=V1_Tmin'
node_target = 'ns=2;s=V1_Tar'

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

class temp_handler(object):
    def datachange_notification(self, node, val, data):
        global last_temp
        last_temp = val
        insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val)

class state_handler(object):
    def datachange_notification(self, node, val, data):
        global last_state
        last_state = val
        insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val)

class target_handler(object):
    def datachange_notification(self, node, val, data):
        global last_target
        last_target = val
        insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val)

client = Client(config.URL)
try:
    client.connect()
    print("Client connected")
except:
    print('Error connecting to server')
else:
    id = client.get_node(node_id)
    temp = client.get_node(node_temp)
    state = client.get_node(node_state)
    temp_max = client.get_node(node_temp_max)
    temp_min = client.get_node(node_temp_min)
    target = client.get_node(node_target)
    id_val = id.get_value()
    last_temp = temp.get_value()
    last_state = state.get_value()
    last_target = target.get_value ()
    temp_max_val = temp_max.get_value()
    temp_min_val = temp_min.get_value()

    handler_temp = temp_handler()
    sub_temp = client.create_subscription(500, handler_temp)
    handle_temp = sub_temp.subscribe_data_change(temp)

    handler_state = state_handler()
    sub_state = client.create_subscription(500, handler_state)
    handle_state = sub_state.subscribe_data_change(state)

    handler_target = target_handler()
    sub_target = client.create_subscription(500, handler_target)
    handle_target = sub_target.subscribe_data_change(target)
    
    while True:
        insert_value(last_temp,last_state,last_target,id_val,temp_max_val,temp_min_val)
        time.sleep(15)
    # sub.unsubscribe(handle)
    # print('Client disconnected')
    # client.disconnect





