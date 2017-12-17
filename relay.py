'Module for managing a simple relay.'
import automationhat

class Relay(object):
    'Class for controlling a simple relay.'

    _options = [
        "ON",
        "OFF",
        "on",
        "off",
        1,
        0
    ]

    def __init__(self, name, relay_pin):
        self.relay_pin = relay_pin
        self.name = name

    @property
    def state(self):
        'Return the current state of the door.'
        if automationhat.output[self.relay_pin - 1].read() == 1:
            return "ON"
        else:
            return "OFF"

    @state.setter
    def state(self, value):
        if value not in self._options:
            raise AttributeError('can\'t set attribute')

        if value.upper() == "ON":
            value = 1
        elif value.upper() == "OFF":
            value = 0
        automationhat.output[self.relay_pin - 1].write(value)
