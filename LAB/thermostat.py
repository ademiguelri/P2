from warnings import catch_warnings
import control.stateMachine as stateMachine
import server
import random
import time
from threading import Thread
import control.config as config

class target_comp:
    def __init__(self):
        self.actual_target = 20
        self.new_target = 20

def main():

#    Get value to crate thermostat objects
    thermostat_list = []
    thermo_target = []

    for i in range(config.THERM_NUM):
#       Create the thermostat
        thermostat = stateMachine.thermostat(i+1)
        #power on the thermostat
        thermostat.power = 1
        thermostat_list.append(thermostat)
        comp = target_comp()
        thermo_target.append(comp)
        

    print("---{} Thermostats created---".format(config.THERM_NUM))

#   Start OPC UA server and client 
    server_thread = Thread(target=server.start_server, args=[thermostat_list, config.THERM_NUM])
    server_thread.start()
    time.sleep(5)
#   Switch on the thermostat
    while True:
        
        if config.th_power_off == -1:
            #Switch the thermostats
            for j in range(config.THERM_NUM):

                if thermostat_list[j].power == 1:
                    #If the machine start working again from off state
                    if thermostat_list[j].state == 'off':
                        if thermostat_list[j].temp < thermo_target[j].actual_target:
                            thermostat_list[j].status = 'warming'
                        else:
                            thermostat_list[j].status = 'cooling'
                        thermostat_list[j].set_state('power_on')

                    #Initialize the thermostat 
                    thermo_target[j].new_target = config.target_server[j]
                    if thermostat_list[j].state == 'start':
                        print("STATE 1 start")
                        thermostat_list[j].initialize()

                    elif thermo_target[j].actual_target != thermo_target[j].new_target:
                        thermostat_list[j].target_changing()
                        if thermo_target[j].new_target < thermostat_list[j].temp:
                            thermostat_list[j].start_cooling()
                        elif thermo_target[j].new_target > thermostat_list[j].temp:
                            thermostat_list[j].start_warming()
                        thermo_target[j].actual_target = thermo_target[j].new_target

                    elif thermostat_list[j].state == 'warming':
                        print("STATE 2 warming")
                        if thermostat_list[j].temp > thermo_target[j].actual_target+1:
                            thermostat_list[j].start_cooling()
                        else:
                            thermostat_list[j].temp += random.random()
                    elif thermostat_list[j].state == 'cooling':
                        print("STATE 3 cooling")
                        if thermostat_list[j].temp < thermo_target[j].actual_target-1:
                            thermostat_list[j].start_warming()
                        else:
                            thermostat_list[j].temp -= random.random()
                    elif thermostat_list[j].state == 'off':
                        print("STATE 4 of")
                else:
                    if thermostat_list[j].state != 'off':
                        thermostat_list[j].power_off()
                    if thermostat_list[j].temp > config.env_temp:
                        thermostat_list[j].temp -= random.random()
            time.sleep(config.thermostat_refresh)
        
        else:
            print('POWER OFF THERMOSTAT {}'.format(config.th_power_off))
            thermostat_list[config.th_power_off-1].power = 0
            config.th_power_off = -1

if __name__ == "__main__":
   main()

