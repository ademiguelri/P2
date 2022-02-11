import random
import control.config as config
from transitions import Machine

class thermostat:

    STATESLIST = ['start', 'warming', 'cooling', 'off']

    def __init__(self, id):
        self.machine = Machine(model=self, states=thermostat.STATESLIST, initial ='start')
        self.temp = config.start_temp
        self.target = config.start_target
        self.temp_max = config.start_temp_max
        self.temp_min = config.start_temp_min
        self.id = 'TH'+str(id)

        self.machine.add_transition(trigger='initialize', source='start', dest='warming')
        self.machine.add_transition(trigger='start_cooling', source='warming', dest='cooling')
        self.machine.add_transition(trigger='start_warming', source='cooling', dest='warming')
        self.machine.add_transition(trigger='power_off', source='*', dest='off')


