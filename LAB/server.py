from opcua import Server
from random import randint
import datetime
import time
import Control.config as config
import thermostat

CONNECTION_FASE  = 0
therm_list = []

def start_server(stateMachine, count):
    server = Server()

    server.set_endpoint(config.URL)

    node =  server.get_objects_node()

    id = 'ns=2;s="V"'
    param = node.add_object(id, "Parameters")

    for k in range(count):
        therm = param.add_folder(id+'{}'.format(k+1), "therm_{}".format(k+1))
        therm_list.append(therm)

    var_list = []
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm_id = therm_list[j].add_variable('ns=2;s="V{}_Id"'.format(j+1), "Id", stateMachine[j].id)
        therm_variables.temp = therm_list[j].add_variable('ns=2;s="V{}_Te"'.format(j+1), "Temperature", stateMachine[j].temp)
        therm_variables.time_value = therm_list[j].add_variable('ns=2;s="V{}_Ti"'.format(j+1), "Time", datetime.datetime.now())
        therm_variables.state = therm_list[j].add_variable('ns=2;s="V{}_St"'.format(j+1), "State", stateMachine[j].state)
        therm_variables.temp_max = therm_list[j].add_variable('ns=2;s="V{}_Tmax"'.format(j+1), "Temperature max", stateMachine[j].temp_max)
        therm_variables.temp_min = therm_list[j].add_variable('ns=2;s="V{}_Tmin"'.format(j+1), "Temperature min", stateMachine[j].temp_min)
        var_list.append(therm_variables)

    # for j in range(count):
    # therm_id_1 = therm_list[0].add_variable('ns=2;s="V1_Id"', "Id", 0)
    # temp_1 = therm_list[0].add_variable('ns=2;s="V1_Te"', "Temperature", 0)
    # time_value_1 = therm_list[0].add_variable('ns=2;s="V1_Ti"', "Time", 0)
    # state_1 = therm_list[0].add_variable('ns=2;s="V1_St"', "State", 0)
    # temp_max_1 = therm_list[0].add_variable('ns=2;s="V1_Tmax"', "Temperature max", 0)
    # temp_min_1 = therm_list[0].add_variable('ns=2;s="V1_Tmin"', "Temperature min", 0)
    
    # therm_id_2 = therm_list[1].add_variable('ns=2;s="V2_Id"', "Id", 0)
    # temp_2 = therm_list[1].add_variable('ns=2;s="V2_Te"', "Temperature", 0)
    # time_value_2 = therm_list[1].add_variable('ns=2;s="V2_Ti"', "Time", 0)
    # state_2 = therm_list[1].add_variable('ns=2;s="V2_St"', "State", 0)
    # temp_max_2 = therm_list[1].add_variable('ns=2;s="V2_Tmax"', "Temperature max", 0)
    # temp_min_2 = therm_list[1].add_variable('ns=2;s="V2_Tmin"', "Temperature min", 0)

    # therm_id_3 = therm_list[2].add_variable('ns=2;s="V3_Id"', "Id", 0)
    # temp_3 = therm_list[2].add_variable('ns=2;s="V3_Te"', "Temperature", 0)
    # time_value_3 = therm_list[2].add_variable('ns=2;s="V3_Ti"', "Time", 0)
    # state_3 = therm_list[2].add_variable('ns=2;s="V3_St"', "State", 0)
    # temp_max_3 = therm_list[2].add_variable('ns=2;s="V3_Tmax"', "Temperature max", 0)
    # temp_min_3 = therm_list[2].add_variable('ns=2;s="V3_Tmin"', "Temperature min", 0)

    # myobject = objects.add_object(idx, "NewObject")
    # myvar = myobject.add_variable(idx, "MyVariable", [16, 56])
    # myprop = myobject.add_property(idx, "myprop", 9.9)
    # myfolder = myobject.add_folder(idx, "myfolder")
    # myvar2 = myfolder.add_variable(idx, "MyVariable2", 33)

    #therm_id.set_writable()
    #temp.set_writable()
    #timeValue.set_writable()
    #state.set_writable()
    #temp_max.set_writable()
    #temp_min.set_writable()

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
            var_list[i].time_value.set_value(TIME)
            var_list[i].state.set_value(STATE)
            var_list[i].temp_max.set_value(TEMP_MAX)
            var_list[i].temp_min.set_value(TEMP_MIN)



            
            print("Server: "+str(ID), str(TEMP), str(TIME), str(STATE))

        time.sleep(config.server_refresh)


class therm_var:

    def __init__(self):
        self.therm_id = 0
        self.temp = 0
        self.time_value = 0
        self.state = 0
        self.temp_max = 0
        self.temp_min = 0