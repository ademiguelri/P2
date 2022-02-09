from opcua import Server
from random import randint
import datetime
import time
import Control.config as config
import thermostat

def start_server(stateMachine, count):
    server = Server()

    server.set_endpoint(config.URL)

    name = "OPCUA_SIMULATION_SERVER"
    #addspace = server.register_namespace(name)
    id = 'ns=2;s="V1"'

    node =  server.get_objects_node()

    param = node.add_object(id, "Parameters")

    therm_id = param.add_variable('ns=2;s="V1_Id"', "Id", 0)
    temp = param.add_variable('ns=2;s="V1_Te"', "Temperature", 0)
    timeValue = param.add_variable('ns=2;s="V1_Ti"', "Time", 0)
    state = param.add_variable('ns=2;s="V1_St"', "State", 0)
    temp_max = param.add_variable('ns=2;s="V1_Tmax"', "Temperature max", 0)
    temp_min = param.add_variable('ns=2;s="V1_Tmin"', "Temperature min", 0)

    # therm_id.set_writable()
    # temp.set_writable()
    # time.set_writable()
    # state.set_writable()
    temp_max.set_writable()
    temp_min.set_writable()

    server.start()
    print("Server started at {}".format(config.URL))

    while True:
        for i in range(count):
            ID = stateMachine[i].id
            TEMP = stateMachine[i].temp
            TIME = datetime.datetime.now()
            STATE = stateMachine[i].state
            TEMP_MAX = stateMachine[i].temp_max
            TEMP_MIN = stateMachine[i].temp_min
            print("Server: "+str(ID), str(TEMP), str(TIME), str(STATE))

            therm_id.set_value(ID)
            temp.set_value(TEMP)
            timeValue.set_value(TIME)
            state.set_value(STATE)

        time.sleep(config.server_refresh)