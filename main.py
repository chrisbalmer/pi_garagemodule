#!/usr/bin/env python3
"""Simple module to manage some garage devices with MQTT
"""

import json
from time import sleep
import paho.mqtt.client as mqtt
from garagedoor import GarageDoor
from relay import Relay

settings = None
doors = []
relays = []

def main():
    """Sets up the devices and registers with the MQTT host.
    """
    global settings
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    doors.append(GarageDoor("door1", state_pin=1))
    relays.append(Relay("relay1", relay_pin=1))

    publish(client)
    monitor(client)

def monitor(client):
    """Monitors for changes in device state and runs the MQTT loop to check for
    messages.
    """
    count = 0
    states = {}
    while True:
        for door in doors:
            state = door.state
            update = False
            if door.name not in states or states[door.name] != state:
                states[door.name] = state
                update = True
            
            if update:
                publish(client)
        client.loop()
        sleep(0.25)

if __name__ == '__main__':
    main()
