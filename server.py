from opcua import Server
from random import randint
import datetime
import time
import Control.config as config
import thermostat

def start_server():
    server = Server()

    server.set_endpoint(config.URL)

    name = "OPCUA_SIMULATION_SERVER"
    #addspace = server.register_namespace(name)
    id = 'ns=2;s="V1"'

    node =  server.get_objects_node()

    Param = node.add_object(id, "Parameters")

    Temp = Param.add_variable('ns=2;s="V1_Te"', "Temperature", 0)
    Time = Param.add_variable('ns=2;s="V1_Ti"', "Time", 0)
    State = Param.add_variable('ns=2;s="V1_St"', "State", 0)
    temp_max = Param.add_variable('ns=2;s="V1_Tmax"', "Temperature max", 0)
    temp_min = Param.add_variable('ns=2;s="V1_Tmin"', "Temperature min", 0)

    Temp.set_writable()
    Time.set_writable()
    State.set_writable()
    temp_max.set_writable()
    temp_min.set_writable()

    server.start()
    print("Server started at {}".format(config.URL))

    while True:
        Temperature = config.local_temp
        TIME = datetime.datetime.now()
        STATE = config.local_state
        config.local_temp_max = temp_max.get_value()
        config.local_temp_min = temp_min.get_value()
        print("Server: " + str(Temperature), str(TIME), str(STATE))

        Temp.set_value(Temperature)
        Time.set_value(TIME)
        State.set_value(STATE)

        time.sleep(2)