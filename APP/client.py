from opcua import Client, ua
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

lap = 1
id = 'ns=2;s=V'
therm_id = ''
temp = ''
state = ''
target = ''


def start_client():
    therm_list = []
    handler_list = []
    handle_list = []
    global therm_id
    global temp
    global state
    global target

    client = Client(config.URL)
    try:
        client.set_user(config.username)
        client.set_password(config.password)
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
    

        root = client.get_root_node()
        
        # print("Root node is: {:s} ".format(str(root)))

        def browse_recursive(node):
            for childId in node.get_children():
                ch = client.get_node(childId)
                # print(ch.get_node_class())
                if ch.get_node_class() == ua.NodeClass.Object:
                    browse_recursive(ch)
                elif ch.get_node_class() == ua.NodeClass.Variable:
                    try:
                        # print("{bn} has value {val}".format(
                        #     bn=ch.get_browse_name(),
                        #     val=str(ch.get_value()))
                        # )
                        bn=str(ch.get_browse_name())
                        val=str(ch.get_value())
                        if bn.find(':Id)') != -1:
                            if therm_id != '':
                                insert_value(therm_id, temp, state, target)
                        if bn.find(':Id)') != -1 or bn.find('Temperature') != -1 or bn.find('State') != -1 or bn.find('Target') != -1:
                            # print(str(bn)+': '+str(val))
                            clasify_variables(bn, val)
                    except ua.uaerrors._auto.BadWaitingForInitialData:
                        pass

        while True:
            browse_recursive(root)
            insert_value(therm_id, temp, state, target)
            time.sleep(lap)


def insert_value(id, temp, state, target):
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state, target) VALUES ('"+str(id)+"', current_timestamp,"+str(temp)+",'"+str(state)+"',"+str(target)+")")
    conn.commit()
    cursor.close()

def clasify_variables(bn, val):
    global therm_id
    global temp
    global state
    global target
    if bn.find(':Id)') != -1:
        therm_id = val
    elif bn.find('Temperature)') != -1:
        temp = val
    elif bn.find('State') != -1:
        state = val
    elif bn.find('Target') != -1:
        target = val