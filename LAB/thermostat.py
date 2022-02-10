from warnings import catch_warnings
import Control.stateMachine as stateMachine
import server
import random
import time
from threading import Thread
import Control.config as config


def main():

#    Get value to crate thermostat objects
    thermostat_list = []

    for i in range(config.THERM_NUM):
#       Create the thermostat
        thermostat = stateMachine.thermostat(i+1)
        thermostat_list.append(thermostat)

        

    print("---{} Thermostats created---".format(config.THERM_NUM))

#   Start OPC UA server and client 
    server_thread = Thread(target=server.start_server, args=[thermostat_list, config.THERM_NUM])
    server_thread.start()
    time.sleep(5)
#   Switch on the thermostat
    while True:
        for j in range(config.THERM_NUM):
            if thermostat_list[j].state == 'start':
                print("STATE 1 start")
                thermostat_list[j].initialize()
            elif thermostat_list[j].state == 'warming':
                print("STATE 2 warming")
                if thermostat_list[j].temp > config.start_temp_max:
                    thermostat_list[j].start_cooling()
                else:
                    thermostat_list[j].temp += random.random()
            elif thermostat_list[j].state == 'cooling':
                print("STATE 3 cooling")
                if thermostat_list[j].temp < config.start_temp_min:
                    thermostat_list[j].start_warming()
                else:
                    thermostat_list[j].temp -= random.random()
            elif thermostat_list[j].state == 'off':
                print("STATE 4 of")

        time.sleep(config.thermostat_refresh)

if __name__ == "__main__":
   main()