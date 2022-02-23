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

def start_client(count):
    therm_list = []
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

    # while True:
    #     insert_value(therm_list[k].get_value())
    #     print("Client: "+str(therm_list[k].id), str(therm_list[k].temp), str(therm_list[k].state), str(therm_list[k].target))    
    #     time.sleep(config.client_refresh)

def insert_value(term):

    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(term.id)+"', current_timestamp,"+str(term.temp)+",'"+str(term.state)+"',"+str(term.target)+")")
    conn.commit()
    cursor.close()

class therm_handler(object):
    def datachange_notification(self, node, val, data):
        insert_value(val.get_value())
