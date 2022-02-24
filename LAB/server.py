from http import server
from opcua import Server,ua 
import datetime
import time
import control.config as config
import thermostat
from security.opc_server_security import OPC_SERVER_SECURITY

# opc_server = OPC_SERVER_SECURITY()
obj_list = []
var_list = []
value_list = []
id = 'ns=2;s=V'
power_value = True
server_ip = '0.0.0.0'

def start_server(stateMachine, count):
    server = Server()
    server.set_endpoint(config.URL)

########################################

    # uri = "http://examples.freeopcua.github.io"
    # idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    # objects = server.get_objects_node()
    # types = server.get_node(ua.ObjectIds.BaseObjectType)
    
    # object_type_to_derive_from = server.get_root_node().get_child(["0:Types", 
    #                                                                "0:ObjectTypes", 
    #                                                                "0:BaseObjectType"])
    # mycustomobj_type = types.add_object_type(idx, "MyThermostat")
    # var = mycustomobj_type.add_variable(0, "target", 15.0) # demonstrates instantiate
    # var.set_modelling_rule(True) #if false it would not be instantiated
    # var2 = mycustomobj_type.add_variable(1, "temp", 15.0) # demonstrates instantiate
    # var2.set_modelling_rule(True) #if false it would not be instantiated
    # var3 = mycustomobj_type.add_variable(1, "state", "off") # demonstrates instantiate
    # var3.set_modelling_rule(True) #if false it would not be instantiated
    # myobjA = objects.add_object(idx, "ThermA", mycustomobj_type.nodeid)
    # myobjB = objects.add_object(idx, "ThermB", mycustomobj_type.nodeid)
    # myobjC = objects.add_object(idx, "ThermC", mycustomobj_type.nodeid)

    # myobjC.target = 11

########################################

    node =  server.get_objects_node()
    custom_obj_type = node.add_object_type(id, "Thermostats")

    therm_id = custom_obj_type.add_variable(0, "Id", '')
    therm_id.set_modelling_rule(True)
    temp = custom_obj_type.add_variable(1, "Temperature", 0.0)
    temp.set_modelling_rule(True)
    state = custom_obj_type.add_variable(2, "State", '')
    state.set_modelling_rule(True)
    temp_max = custom_obj_type.add_variable(3, "Temperature_max", 0.0)
    temp_max.set_modelling_rule(True)
    temp_min = custom_obj_type.add_variable(4, "Temperature_min", 0.0)
    temp_min.set_modelling_rule(True)
    target = custom_obj_type.add_variable(5, "Target", 0)
    target.set_modelling_rule(True)
    target.set_writable()
    target = custom_obj_type.add_variable(6, "Power", 0)
    target.set_modelling_rule(True)
    target.set_writable()

    for l in range(count):
        myobj = node.add_object(id+'{}'.format(str(l+1)), "Therm{}".format(l+1), custom_obj_type.nodeid)
        obj_list.append(myobj)

    var_list = add_variables(count, stateMachine, obj_list)

    server.start()
    print("Server started at {}".format(config.URL))
    
    # opc_server.init_opc_server_security(server_ip)
    # opc_server.set_server_credentials('admin', 'admin123')


    global power_value
    TARGET = stateMachine[0].target
    POWER = stateMachine[0].power
    for n in range(int(count)):
        var_list[n].target.set_value(TARGET)
        var_list[n].power.set_value(POWER)

    while True:
        # auth = opc_server.client_authentication()
        # while auth:
        for i in range(count):
            ID = stateMachine[i].id
            TEMP = stateMachine[i].temp
            STATE = stateMachine[i].state
            TEMP_MAX = stateMachine[i].temp_max
            TEMP_MIN = stateMachine[i].temp_min
            TARGET = var_list[i].target.get_value() 
            stateMachine[i].target = TARGET
            POWER = var_list[i].power.get_value() 
            stateMachine[i].power = POWER

            print("Server: "+str(ID), str(TEMP), str(STATE), str(TARGET))

            var_list[i].therm_id.set_value(ID)
            var_list[i].temp.set_value(TEMP)
            var_list[i].state.set_value(STATE)
            var_list[i].temp_max.set_value(TEMP_MAX)
            var_list[i].temp_min.set_value(TEMP_MIN)

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
        self.power = 0

def add_variables(count, stateMachine, obj_list):
    list = []
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm_id = obj_list[j].get_child(["0:Id"])
        therm_variables.temp = obj_list[j].get_child(["1:Temperature"])
        therm_variables.state = obj_list[j].get_child(["2:State"])
        therm_variables.temp_max = obj_list[j].get_child(["3:Temperature_max"])
        therm_variables.temp_min = obj_list[j].get_child(["4:Temperature_min"])
        therm_variables.target = obj_list[j].get_child(["5:Target"])
        therm_variables.power = obj_list[j].get_child(["6:Power"])
        list.append(therm_variables)   
    return list