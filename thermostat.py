import Control.stateMachine as stateMachine
import server
import client
import random
import time
from threading import Thread
import Control.config as config


def main():
#   Create the thermostat
    thermostat = stateMachine.thermostat()
    config.local_temp = thermostat.temp
    config.local_state = thermostat.machine.get_state(thermostat.state).name
    print("---Thermostat created---")
    print("Startig state: "+ thermostat.machine.get_state(thermostat.state).name)

#   Start OPC UA server and client 
    server_thread = Thread(target=server.start_server)
    server_thread.start()
    time.sleep(5)
    client_thread = Thread(target=client.start_client)
    client_thread.start()

#   Switch on the thermostat
    while thermostat.LOOP:  

        if thermostat.state == 'start':
            print("STATE 1")
            thermostat.initialize()
        elif thermostat.state == 'warming':
            print("STATE 2")
            if config.local_temp_max == 1:
                thermostat.temp_max()
            else:
                thermostat.temp += random.random()
        elif thermostat.state == 'cooling':
            print("STATE 3")
            if config.local_temp_min == 1:
                thermostat.temp_min()
            thermostat.temp -= random.random()

        config.local_temp = thermostat.temp
        config.local_state = thermostat.machine.get_state(thermostat.state).name
        time.sleep(3)

if __name__ == "__main__":
   main()