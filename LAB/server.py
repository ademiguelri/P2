from opcua import Server
import datetime
import time
import control.config as config
import thermostat

therm_list = []
var_list = []
value_list = []
id = 'ns=2;s=V'
actual_power = 'True'

def start_server(stateMachine, count):
    server = Server()
    server.set_endpoint(config.URL)
    node =  server.get_objects_node()
    param = node.add_object(id, "Thermostat")
    global actual_power

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

            if actual_power != VALUE_LIST[6]:
                if VALUE_LIST[6] == 'False':
                    stateMachine[i].power_off()
                    actual_power = 'False'
                elif VALUE_LIST[6] == 'True':
                    stateMachine[i].power_on()
                    actual_power = 'True'

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
    power = True    
    values.append(str(stateMachine.id))
    values.append(str(stateMachine.temp))
    values.append(str(stateMachine.state))
    values.append(str(stateMachine.temp_max))
    values.append(str(stateMachine.temp_min))
    values.append(str(stateMachine.target))
    values.append(str(power))
    return values