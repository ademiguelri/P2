from tracemalloc import start
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

lap = 15
therm1_val = 0
therm2_val = 0
therm3_val = 0


def start_client(count):
    therm_list = []
    global therm1_val
    global therm2_val
    global therm3_val

    client = Client(config.URL)
    try:
        client.connect()
        print("Client connected")
    except:
        print('Error connecting to server')
    else:
        with psycopg2.connect(CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute(drop_table)
            cursor.execute(query_create_table)
            conn.commit()
            cursor.execute(query_create_hypertable)
            conn.commit()
            cursor.close()
    
        
        therm1 = client.get_node('ns=2;s=V1_Therm')
        therm2 = client.get_node('ns=2;s=V2_Therm')
        therm3 = client.get_node('ns=2;s=V3_Therm')

        handler_1 = therm_handler()
        sub_1 = client.create_subscription(500, handler_1)
        handle_1 = sub_1.subscribe_data_change(therm1)

        handler_2 = therm_handler()
        sub_2 = client.create_subscription(500, handler_2)
        handle_2 = sub_2.subscribe_data_change(therm2)

        handler_3 = therm_handler()
        sub_3 = client.create_subscription(500, handler_3)
        handle_3 = sub_3.subscribe_data_change(therm3)

        while True:
           insert_value(therm1_val)
           insert_value(therm2_val)
           insert_value(therm3_val)
           time.sleep(lap)

def insert_value(term):
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(term[0])+"', current_timestamp,"+str(term[1])+",'"+str(term[2])+"',"+str(term[5])+")")
    conn.commit()
    cursor.close()
    if term[0] == 'TH1':
        therm1_val = term
    elif term[0] == 'TH2':
        therm2_val = term
    elif term[0] == 'TH3':
        therm3_val = term

class therm_handler(object):
    def datachange_notification(self, node, val, data):
        insert_value(val)
        global flag
        flag = True
