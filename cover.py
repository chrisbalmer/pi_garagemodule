'Module for managing a cover.'
from time import sleep
import automationhat

DOOR_CLOSED = 0
DOOR_OPEN = 1


class Cover(object):
    'Class for controlling a cover.'

    def __init__(self, name, state_pin, trigger_delay=0.500):
        self.state_pin = state_pin
        self.trigger_delay = trigger_delay
        self.name = name


    def trigger(self):
        'Triggers the door relay to open or close it.'
        automationhat.relay.on()
        sleep(self.trigger_delay)
        automationhat.relay.off()


    @property
    def state(self):
        'Return the current state of the door.'
        if automationhat.input[self.state_pin - 1].read() == 1:
            return "closed"
        else:
            return "open"


    @state.setter
    def state(self, value):
        raise AttributeError('can\'t set attribute')


    def open(self):
        'If the door is closed, trigger opening it.'
        if self.state == DOOR_CLOSED:
            self.trigger()


    def close(self):
        'If the door is open, trigger closing it.'
        if self.state == DOOR_OPEN:
            self.trigger()