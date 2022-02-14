import app.docker.config as client_config
import lab.control.config as therm_config


def main():
    while True:

        print('Interact with the Thermostat [press 1, 2 or 3]: ')
        th = input()

        if int(th) == 1:
            print('Change target temperature[press t]')
            print('Power off thermostat [press p]')
            pr = input()

            if pr == 't':
                client_config.th_selection = int(th)
                print('Target value: ')
                tar = input()
                client_config.target = tar
            elif pr == 'p':
                therm_config.th_power_off = th
                print(therm_config.th_power_off)

        elif int(th) == 2:
            print('Change target temperature[press t]')
            print('Power off thermostat [press p]')
            pr = input()

            if pr == 't':
                client_config.th_selection = int(th)
                print('Target value: ')
                tar = input()
                client_config.target = tar

            elif pr == 'p':
                therm_config.th_power_off = th

        elif int(th) == 3:
            print('Change target temperature[press t]')
            print('Power off thermostat [press p]')
            pr = input()

            if pr == 't':
                client_config.th_selection = int(th)
                print('Target value: ')
                tar = input()
                client_config.target = tar
            elif pr == 'p':
                therm_config.th_power_off = th

        else:
            print('Wrong input value')

if __name__ == "__main__":
   main()