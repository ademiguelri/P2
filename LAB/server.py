from opcua import Server,ua 
import datetime
import time
import control.config as config
import thermostat

therm_list = []
var_list = []
value_list = []
id = 'ns=2;s=V'
power_value = True

def start_server(stateMachine, count):
    server = Server()
    server.set_endpoint(config.URL)

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()
    types = server.get_node(ua.ObjectIds.BaseObjectType)
    
    object_type_to_derive_from = server.get_root_node().get_child(["0:Types", 
                                                                   "0:ObjectTypes", 
                                                                   "0:BaseObjectType"])
    mycustomobj_type = types.add_object_type(idx, "MyThermostat")
    var = mycustomobj_type.add_variable(0, "target", 15.0) # demonstrates instantiate
    var.set_modelling_rule(True) #if false it would not be instantiated
    var2 = mycustomobj_type.add_variable(1, "temp", 15.0) # demonstrates instantiate
    var2.set_modelling_rule(True) #if false it would not be instantiated
    var3 = mycustomobj_type.add_variable(1, "state", "off") # demonstrates instantiate
    var3.set_modelling_rule(True) #if false it would not be instantiated
    myobjA = objects.add_object(idx, "ThermA", mycustomobj_type.nodeid)
    myobjB = objects.add_object(idx, "ThermB", mycustomobj_type.nodeid)
    myobjC = objects.add_object(idx, "ThermC", mycustomobj_type.nodeid)

    myobjC.target = 11




    node =  server.get_objects_node()
    param = node.add_object(id, "Thermostat")
    global power_value

    for k in range(count):
        therm = param.add_folder(id+'{}'.format(k+1), "therm_{}".format(k+1))
        therm_list.append(therm)

        value_list.append(extract_required_values(stateMachine[k]))

    

    var_list = add_variables(count, value_list)

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
            VALUE_LIST = var_list[i].therm.get_value()
            stateMachine[i].target = int(VALUE_LIST[5])

            if VALUE_LIST[6] == 'False':
                stateMachine[i].power = 0
                power_value = False
            elif VALUE_LIST[6] == 'True':
                stateMachine[i].power = 1
                power_value = True

            THERM = extract_required_values(stateMachine[i])
            var_list[i].therm.set_value(THERM)

            print("Server: "+str(ID), str(TEMP), str(STATE), str(VALUE_LIST[5]))

        time.sleep(config.server_refresh)
    

class therm_var:
    def __init__(self):
        self.therm = 0

def add_variables(count, values):
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm = therm_list[j].add_variable('ns=2;s=V{}_Therm'.format(j+1), 'Therm{}'.format(j+1), values[j])
        therm_variables.therm.set_writable()
        var_list.append(therm_variables)   
    return var_list

def extract_required_values(stateMachine):
    values = []
    global power_value 
    values.append(str(stateMachine.id))
    values.append(str(stateMachine.temp))
    values.append(str(stateMachine.state))
    values.append(str(stateMachine.temp_max))
    values.append(str(stateMachine.temp_min))
    values.append(str(stateMachine.target))
    values.append(str(power_value))
    return values