"""

@author: muhamizz
@date: October 2017

python2 ok
python3 ok

-*- coding: utf-8 -*-

"""
import logging
welcomebt_log = logging.getLogger("mqttlog")

import threading
import paho.mqtt.client as mqtt
import traceback
import json
import time
import subprocess

class Connection(object):
    """
    Connection using mqtt
    io:
        self.emit: (event, data) send data to topic {event}
        self.send: (event, data) same as self.emit
        self.set_event: subscribe to event topic and set callback_function on message
        self.start: start the threading main loop
        #event constants
    """
    

    def __init__(
            self,
            user="a",
            password="a",
            server="127.0.0.1",
            port=1883,
            on_message=None
        ):
        #~ super(Connection,self).__init__()
        self.user = user
        self.password = password
        self.server = server
        self.port = port
        
        mqtt_protocol = mqtt.MQTTv31
        
        self.client = mqtt.Client(protocol=mqtt_protocol)
        
        self.client.username_pw_set(user, password)
        
        if on_message is not None:
            self.client.on_message = on_message
        else:
            self.client.on_message = self.on_message
        
        self.client.on_connect = self.on_connect
        self.publish = self.client.publish
        
        self.emit = self.send
        
        self.event_callbacks = {} 
        """
        dict method as callback for each event_name
        format {
            event_name:callback_function
        }
        """
        
        
        self.start = self.run




    def on_connect(self, client, userdata, flags, rc):
        print("interface_mqtt connected")
        welcomebt_log.info("interface_mqtt connected")
        
        for topic in self.event_callbacks:
            self.client.subscribe(topic, 1)#(topic,qos)


    def on_disconnect(self, client, userdata, rc):
        print("mqtt {} disconnected, reconnecting".format(self.server))
        welcomebt_log.info("mqtt {} disconnected, reconnecting".format(self.server))
        client.reconnect()




    def set_event(self, event_name, callback_function):
        """
        subscribe to topic event_name and do 
        callback_function(message) on message received for this topic
        
        @param callback_function is method with param (data):
            data is in dict or str
        """
        self.event_callbacks[event_name] = callback_function
        self.client.subscribe(event_name, 1)




    def on_message(self, client, userdata, msg):
        event = msg.topic
        try:
            utf8data = msg.payload.decode("utf-8")
            data = json.loads(utf8data)
        except ValueError:
            data = utf8data
        
        try:
            self.event_callbacks[event](data)
        except KeyError:
            print("event {} action not set".format(event))




    def run(self):
        print("interface_mqtt started")
        while True:
            try:
                self.client.connect(self.server, self.port)
                break
            except:
                print("retry")
                time.sleep(1)
                  
        self.client.loop_start()




    def send(self, event_name, data):
        """
        send data to event_name
        with mqtt event_name is the topic
        @param event_name
        @param data: can be dict or str
        """
        if type(data)==dict:
            data = json.dumps(data)
        self.publish(event_name, qos=1, payload=data, retain=False)
        
