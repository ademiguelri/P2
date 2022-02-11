from opcua import Client
import time
import docker.config as config
from warnings import catch_warnings;
import psycopg2

CONNECTION = "postgres://"+config.username+":"+config.password+"@"+config.host+":"+config.port+"/"+config.dbName
query_create_table = "CREATE TABLE therm (id VARCHAR (10), datetime TIMESTAMP, temp FLOAT, state VARCHAR (10));"
query_create_hypertable = "SELECT create_hypertable('therm', 'datetime');"
drop_table = "DROP TABLE therm;"

THERM_COP = 0

def start_client():
    client = Client(config.URL)
    client.connect()
    print("Client connected")

    with psycopg2.connect(CONNECTION) as conn:
        cursor = conn.cursor()
    try:
        cursor.execute(query_create_table)
        conn.commit()
        cursor.execute(query_create_hypertable)
        conn.commit()
    except:
        cursor.execute(drop_table)
    finally:
        conn.commit()

    while True:

        for i in range(3):
            id = client.get_node('ns=2;s="V{}_Id"'.format(i+1))
            temp = client.get_node('ns=2;s="V{}_Te"'.format(i+1))
            timeValue = client.get_node('ns=2;s="V{}_Ti"'.format(i+1))
            state = client.get_node('ns=2;s="V{}_St"'.format(i+1))
            temp_max = client.get_node('ns=2;s="V{}_Tmax"'.format(i+1))
            temp_min = client.get_node('ns=2;s="V{}_Tmin"'.format(i+1))
        
            print("Client: "+ str(id.get_value()), str(temp.get_value()), str(timeValue.get_value()), str(state.get_value()))
            #insert thermostat value to the database
            insert_value(id.get_value(), temp.get_value(), state.get_value())
            
        time.sleep(config.client_refresh)

        # cursor.close()


def insert_value(id, temp, state):

    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therm (id, datetime, temp, state) VALUES ('"+str(id)+"', current_timestamp,"+str(temp)+",'"+str(state)+"')")
    conn.commit()