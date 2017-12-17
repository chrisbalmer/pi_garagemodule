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
    client = mqtt.Client(settings['name'])
    client.tls_set(settings['ca'])
    client.username_pw_set(username=settings['username'],
                           password=settings['password']) 
    client.connect(settings['host'], settings['port'])
    client.subscribe('homeassistant/cover/door1/set')
    client.subscribe('homeassistant/cover/door1/state')
    client.subscribe('homeassistant/switch/relay1/set')
    client.on_connect = on_connect
    client.on_message = on_message
    publish(client)
    monitor(client)

def on_message(client, userdata, message):
    """Checks received messages to see if we need to do anything with our
    devices
    """
    if message.topic == 'homeassistant/cover/door1/set':
        doors[0].trigger()
    elif message.topic == 'homeassistant/switch/relay1/set':
        value = str(message.payload.decode("utf-8"))
        relays[0].state = value
        sleep(0.1)
        client.publish('homeassistant/switch/relay1/state', relays[0].state)

def on_connect(client, userdata, rc):
    """Registers our devices when a connection to the MQTT host is made and
    sends over initial state.
    """
    client.publish('homeassistant/cover/door1/config',
                   '{"name": "door1", "command_topic": "homeassistant/cover/door1/set", "state_topic": "homeassistant/cover/door1/state"}',
                   retain=True)
    client.publish('homeassistant/switch/relay1/config',
                   '{"name": "relay1", "command_topic": "homeassistant/switch/relay1/set", "state_topic": "homeassistant/switch/relay1/state"}',
                   retain=True)
    client.publish('homeassistant/switch/relay1/state', relays[0].state)
    publish(client)

def publish(client):
    """Publishes state of devices.
    """
    for door in doors:
        client.publish('homeassistant/cover/door1/state', door.state)

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
