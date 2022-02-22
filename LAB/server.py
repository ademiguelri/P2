from opcua import Server
from random import randint
import datetime
import time
import control.config as config
import thermostat

therm_list = []
var_list = []
id = 'ns=2;s="V"'

def start_server(stateMachine, count):
    server = Server()
    server.set_endpoint(config.URL)
    node =  server.get_objects_node()
    param = node.add_object(id, "Parameters")

    for k in range(count):
        therm = param.add_folder(id+'{}'.format(k+1), "therm_{}".format(k+1))
        therm_list.append(therm)

    var_list = add_variables(count, stateMachine)

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

            var_list[i].therm_id.set_value(ID)
            var_list[i].temp.set_value(TEMP)
            var_list[i].state.set_value(STATE)
            var_list[i].temp_max.set_value(TEMP_MAX)
            var_list[i].temp_min.set_value(TEMP_MIN)
            TARGET = var_list[i].target.get_value()
            config.target_server[i] = TARGET

            print("Server: "+str(ID), str(TEMP), str(STATE), str(TARGET))

        time.sleep(config.server_refresh)

class therm_var:
    def __init__(self):
        self.therm_id = 0
        self.temp = 0
        self.time_value = 0
        self.state = 0
        self.temp_max = 0
        self.temp_min = 0
        self.target = 0

def add_variables(count, stateMachine):
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm_id = therm_list[j].add_variable('ns=2;s=V{}_Id'.format(j+1), "Id", stateMachine[j].id)
        therm_variables.temp = therm_list[j].add_variable('ns=2;s=V{}_Te'.format(j+1), "Temperature", stateMachine[j].temp)
        therm_variables.state = therm_list[j].add_variable('ns=2;s=V{}_St'.format(j+1), "State", stateMachine[j].state)
        therm_variables.temp_max = therm_list[j].add_variable('ns=2;s=V{}_Tmax'.format(j+1), "Temperature max", stateMachine[j].temp_max)
        therm_variables.temp_min = therm_list[j].add_variable('ns=2;s=V{}_Tmin'.format(j+1), "Temperature min", stateMachine[j].temp_min)
        therm_variables.target = therm_list[j].add_variable('ns=2;s=V{}_Tar'.format(j+1), "Therm target", stateMachine[j].target)
        therm_variables.target.set_writable()
        therm_variables.state.set_writable()
        var_list.append(therm_variables)   
    return var_list