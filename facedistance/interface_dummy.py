import threading

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
        self.start = self.run

    def run(self):
        print("interface_mqtt dummy started")


    def send(self, event_name, data):
        """
        send data to event_name
        with mqtt event_name is the topic
        @param event_name
        @param data: can be dict or str
        """
        print(event_name, data)
