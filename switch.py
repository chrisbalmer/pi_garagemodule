'Module for managing a simple switch.'
import automationhat

class Switch(object):
    'Class for controlling a simple switch.'

    _options = [
        "ON",
        "OFF",
        "on",
        "off",
        1,
        0
    ]

    def __init__(self, name, switch_pin):
        self.switch_pin = switch_pin
        self.name = name

    @property
    def state(self):
        'Return the current state of the door.'
        if automationhat.output[self.switch_pin - 1].read() == 1:
            return "ON"
        else:
            return "OFF"

    @state.setter
    def state(self, value):
        if value not in self._options:
            print(value)
            return

        if value.upper() == "ON":
            value = 1
        elif value.upper() == "OFF":
            value = 0
        automationhat.output[self.switch_pin - 1].write(value)
