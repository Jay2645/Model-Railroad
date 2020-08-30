
import paho.mqtt as mq
import paho.mqtt.client as mqtt
import thread
import time
import sys
import logging

BROKER_ADDRESS = "192.168.86.223"
BROKER_PORT    = 1883
BROKER_TIMEOUT = 120

class JMRIMQTTManager:
    def __init__(self):
        print("Connecting to " + BROKER_ADDRESS + " port: " + str(BROKER_PORT) + ". Timeout: " + str(BROKER_TIMEOUT))

        self.__client = mqtt.Client("JMRI", True, None, protocol=mqtt.MQTTv31)

        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.__client.enable_logger(logging)

        self.__subscription_list = {}

        # we only publish if connected
        self.__client_connected = False

        self.__running = True

        self.__print_paho_version()
  
        # Create threads
        try:
            thread.start_new_thread(self.__start_mqtt_thread, ("MQTT Thread", ))
        except:
            print("Error: unable to start thread")

        count = 0

        while not self.__client_connected and count < BROKER_TIMEOUT:
            time.sleep(1)
            count += 1
        
        if count >= BROKER_TIMEOUT:
            print("Timeout")

    def __print_paho_version(self):
        print("We are running paho-mqtt, version: " + str(mq.__version__))

    # Everything down from here is to create a separate thread for the MQTT
    # subscription to run in...else, you freeze JMRI up and need to kill it
    # to gain control again.
    def __start_mqtt_thread(self, thread_name):
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message

        self.__client.connect(BROKER_ADDRESS, BROKER_PORT, BROKER_TIMEOUT)
        self.__client_connected = True

        self.__client.loop_start()

        count = 0

        # show thread is alive every minute:
        while (self.__running):
            time.sleep(60)  
            count += 1
            print("%s %6d: %s" % (thread_name, count, time.ctime(time.time())))
        
        self.__client.loop_stop()
        print("MQTT Thread stopped")

    # Message when connection is made
    def __on_connect(self, client, user_data, flags, rc):
        print("Connected with result code " + str(rc))

        self.__running = self.__running and rc == 0

        if not self.__running:
            return

        print("MQTT broker flags: " + str(flags))

    # The callback for when a PUBLISH message is received from the Broker.
    def __on_message(self, client, user_data, msg):
        if not self.__running:
            print("Not running")
            return

        payload = str(msg.payload)
        topic = msg.topic
        for delegate in self.__subscription_list[topic]:
            delegate(topic, payload)

    def disconnect(self):
        print ("Disconnecting")
        self.__running = False

    def add_subscription(self, subscription, delegate=None):
        if delegate is not None:
            if subscription not in self.__subscription_list:
                self.__subscription_list[subscription] = []
            self.__subscription_list[subscription].append(delegate)

        self.__client.subscribe(subscription)
        print("Subscribing to " + subscription)

    def publish(self, topic, payload, qos=0, retain=False):
        print("Publishing " + str(payload) + " to " + str(topic))
        self.__client.publish(str(topic), str(payload), qos, retain)
