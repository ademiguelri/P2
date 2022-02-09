import random
from transitions import Machine

class thermostat(object):

    STATESLIST = ['start', 'warming', 'cooling', 'off']

    def __init__(self):
        self.machine = Machine(model=self, states=thermostat.STATESLIST, initial ='start')
        self.temp = 20
        self.LOOP = True

        self.machine.add_transition(trigger='initialize', source='start', dest='warming')
        self.machine.add_transition(trigger='temp_max', source='warming', dest='cooling')
        self.machine.add_transition(trigger='temp_min', source='cooling', dest='warming')
        self.machine.add_transition(trigger='power_off', source='*', dest='OFF')


