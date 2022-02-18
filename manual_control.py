import app.docker.config as client_config
import lab.control.config as therm_config
import json


def main():
    while True:

        print('Thermostat ID: ')
        th = input()

        print('Change target temperature[press t]')
        print('Power on/off thermostat [press p]')
        pr = input()

        if pr == 't':
            client_config.th_selection = int(th)
            print('Target value: ')
            tar = input()

            th_file = open("app/docker/th{}.json".format(int(th)), "r")
            json_object = json.load(th_file)
            th_file.close()
            
            json_object["target"] = int(tar)
            json_object["flag"] = 1
            th_file = open("app/docker/th{}.json".format(int(th)), "w")
            json.dump(json_object, th_file)
            th_file.close()

        elif pr == 'p':
            th_file = open("lab/control/th{}.json".format(int(th)), "r")
            json_object = json.load(th_file)
            th_file.close()
            
            if json_object["power"] == 0:
                json_object["power"] = 1
            elif json_object["power"] == 1:
                json_object["power"] = 0

            th_file = open("lab/control/th{}.json".format(int(th)), "w")
            json.dump(json_object, th_file)
            th_file.close()

        else:
            print('Wrong input value')

if __name__ == "__main__":
   main()