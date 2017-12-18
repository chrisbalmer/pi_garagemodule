'Module for the device class.'
from abc import ABCMeta, abstractmethod
from time import sleep
import json
import paho.mqtt.client as mqtt

class Device(object):
    'Parent class to manage devices.'
    __metaclass__ = ABCMeta

    DEFAULT_TOPICS = {
        'availability': 'homeassistant/cover/{name}/availability',
        'state': 'homeassistant/cover/{name}/state',
        'command': 'homeassistant/cover/{name}/set',
        'config': 'homeassistant/cover/{name}/config'
    }

    ONLINE = 'online'
    OFFLINE = 'offline'


    def __init__(self, name, client_settings, device_settings):
        self.name = name
        self._client_settings = client_settings
        self._device_settings = device_settings
        self._configure_topics()

        self._client = None
        self.client_setup()


    def _configure_topics(self):
        for topic in self.DEFAULT_TOPICS:
            if topic not in self._device_settings:
                self._device_settings[topic] = \
                    self.DEFAULT_TOPICS[topic].format(name=self.name)

    def client_setup(self):
        client_name = self._client_settings['name'] + \
            '_' + self._device_settings['name']
        self._client = mqtt.Client(client_name)
        self._client.tls_set(self._client_settings['ca'])
        self._client.username_pw_set(username=self._client_settings['username'],
                                     password=self._client_settings['password'])
        self._client.will_set(self._client_settings['availability_topic'],
                              self.OFFLINE,
                              qos=1,
                              retain=True)
        self._client.connect(self._client_settings['host'],
                             self._client_settings['port'])
        self._client.subscribe(self._device_settings['command_topic'])
        self._client.subscribe('homeassistant/switch/relay1/set')
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        """Checks received messages to see if we need to do anything with our
        devices
        """
        if message.topic == self._device_settings['command_topic']:
            self.process_command(str(message.payload.decode("utf-8")))

        # elif message.topic == 'homeassistant/switch/relay1/set':
        #     value = str(message.payload.decode("utf-8"))
        #     relays[0].state = value
        #     sleep(0.1)
        #     client.publish('homeassistant/switch/relay1/state', relays[0].state)

    def on_connect(self, client, userdata, rc):
        """Registers our device when a connection to the MQTT host is made and
        sends over initial state.
        """
        topic = self._device_settings['config_topic']
        config = json.dumps(self._device_settings)
        client.publish(topic, config, retain=True)

        topic = self._device_settings['availability_topic']
        client.publish(topic, 'online', qos=1, retain=True)
        self.publish()

    def loop(self):
        """Monitors for changes in device state and runs the MQTT loop to check for
        messages.
        """
        last_state = None
        while True:
            state = self.state
            update = False
            if last_state != state:
                last_state = state
                update = True
            
            if update:
                self.publish()
            self._client.loop()
            sleep(0.25)

    @property
    @abstractmethod
    def state(self):
        pass
    
    @state.setter
    @abstractmethod
    def state(self, value):
        pass

    @abstractmethod
    def process_command(self, command):
        pass

    @abstractmethod
    def publish(self):
        pass
