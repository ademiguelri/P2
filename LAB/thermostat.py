from itertools import cycle
from warnings import catch_warnings
import control.stateMachine as stateMachine
import server
import random
import time
import json
from threading import Thread
import control.config as config

class target_comp:
    def __init__(self):
        self.actual_target = 20
        self.new_target = 20

def start_thermostat(count):

#    Get value to crate thermostat objects
    thermostat_list = []
    thermo_target = []
    cycle = []
    next_cycle = 0.01

#   Create the thermostat
    thermostat_list = create_thermostats(count, thermostat_list)

    for i in range(int(count)):
        comp = target_comp()
        thermo_target.append(comp)
        cycle.append(0)

    print("---{} Thermostats created---".format(int(count)))

#   Start OPC UA server
    server_thread = Thread(target=server.start_server, args=[thermostat_list, int(count)])
    server_thread.start()

#   Switch on the thermostat
    while True:
        #Switch the thermostats
        for j in range(int(count)):
            #Check JSON file
            
            power = read_json(j+1)
            #power == 1 -> on / power == 0 -> off
            if power == 1:
                #If the machine start working again from off state
                if thermostat_list[j].state == 'off':
                    if thermostat_list[j].temp < thermo_target[j].actual_target:
                        thermostat_list[j].target_state = 'warming'
                        temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])
                    else:
                        thermostat_list[j].target_state = 'cooling'
                        temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])
                    thermostat_list[j].power_on()

                #Initialize the thermostat 
                thermo_target[j].new_target = config.target_server[j]
                if thermostat_list[j].state == 'start':
                    print("STATE 1 on")
                    thermostat_list[j].initialize()
                    temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])

                #Target temperature change
                elif thermo_target[j].actual_target != thermo_target[j].new_target:
                    thermostat_list[j].target_changing()
                    if thermo_target[j].new_target < thermostat_list[j].temp:
                        thermostat_list[j].start_cooling()
                    elif thermo_target[j].new_target > thermostat_list[j].temp:
                        thermostat_list[j].start_warming()
                    thermo_target[j].actual_target = thermo_target[j].new_target
                    temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])

                elif thermostat_list[j].state == 'warming':
                    print("STATE 2 warming")
                    if thermostat_list[j].temp > thermo_target[j].actual_target:
                        thermostat_list[j].start_cooling()
                        temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])
                    else:
                        thermostat_list[j].temp += caclulate_temp_change(cycle[j])
                        if thermostat_list[j].temp < thermo_target[j].actual_target-(thermostat_list[j].target_dist/2):
                            cycle[j] += next_cycle
                        else:
                            cycle[j] -= next_cycle
                elif thermostat_list[j].state == 'cooling':
                    print("STATE 3 cooling")
                    if thermostat_list[j].temp < thermo_target[j].actual_target:
                        thermostat_list[j].start_warming()
                        temperature_change_init(thermostat_list[j], thermo_target[j].actual_target, cycle[j])
                    else:
                        thermostat_list[j].temp -= caclulate_temp_change(cycle[j])
                        if thermostat_list[j].temp > thermo_target[j].actual_target+(thermostat_list[j].target_dist/2):
                            cycle[j] += next_cycle
                        else:
                            cycle[j] -= next_cycle
            else:
                print("STATE 4 off")
                if thermostat_list[j].state != 'off':
                    thermostat_list[j].power_off()
                    temperature_change_init(thermostat_list[j], config.env_temp, cycle[j])
                if thermostat_list[j].temp > config.env_temp:
                    thermostat_list[j].temp -= caclulate_temp_change(cycle[j])
                    if thermostat_list[j].temp < config.env_temp+(thermostat_list[j].target_dist/2):
                        cycle[j] += next_cycle
                    else:
                        cycle[j] -= next_cycle
                else:
                    thermostat_list[j].temp += caclulate_temp_change(cycle[j])
                    if thermostat_list[j].temp > config.env_temp-(thermostat_list[j].target_dist/2):
                        cycle[j] += next_cycle
                    else:
                        cycle[j] -= next_cycle
                        
        time.sleep(config.thermostat_refresh)

def create_thermostats(count, thermostat_list):
    for i in range(int(count)):
#       Create the thermostat
        thermostat = stateMachine.thermostat(i+1)
        #power on the thermostat
        th_file = open("lab/control/th{}.json".format(i+1), "r")
        json_object = json.load(th_file)
        print(json_object)
        th_file.close()

        json_object["power"] = 1
        th_file = open("lab/control/th{}.json".format(i+1), "w")
        json.dump(json_object, th_file)
        th_file.close()

        thermostat_list.append(thermostat)
    return thermostat_list

def read_json(num):
    th_file = open("lab/control/th{}.json".format(num), "r")
    json_object = json.load(th_file)
    th_file.close()
    return json_object["power"]

def temperature_change_init(thermostat, target, cycle):
    thermostat.target_dist = abs(thermostat.temp - target)
    cycle = 0

def caclulate_temp_change(cycle):
    if cycle < 0:
        cycle = 0
    return (cycle**2.0)+0.01
