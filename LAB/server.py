from opcua import Server
import datetime
import time
import control.config as config
import thermostat

therm_list = []
var_list = []
id = 'ns=2;s=V'

def start_server(stateMachine, count):
    server = Server()
    server.set_endpoint(config.URL)
    node =  server.get_objects_node()
    param = node.add_object(id, "Thermostat")

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
            TARGET = stateMachine[i].target

            var_list[i].therm.set_value(stateMachine[i])

            print("Server: "+str(ID), str(TEMP), str(STATE), str(TARGET))

        time.sleep(config.server_refresh)
    

class therm_var:
    def __init__(self):
        self.therm = 0
        

def add_variables(count, stateMachine):
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm = therm_list[j].add_variable('ns=2;s=V{}_Therm'.format(j+1), "Therm", 0)
        therm_variables.therm.set_writable()

        var_list.append(therm_variables)   
    return var_list