import re

ROSTER_PATH = "trains/roster"
DISCOVERY_SENSOR_PATH = "discovery/sensor"

manager = JMRIMQTTManager()

def publish(topic, payload, qos=0, retain=False):
    manager.publish(topic, payload, qos, retain)

def subscribe(topic, delegate):
    manager.add_subscription(topic, delegate)

def sanitize_id(id):
    id_string = str(id)
    return re.sub('\W+','_', id_string).lower()

def get_roster_attributes_path(id):
    clean_id = sanitize_id(id)
    return ROSTER_PATH + "/" + clean_id + "/attributes"

def get_roster_state_path(id):
    clean_id = sanitize_id(id)
    return ROSTER_PATH + "/" + clean_id + "/state"

def get_discovery_sensor_path(id):
    clean_id = sanitize_id(id)
    return DISCOVERY_SENSOR_PATH + "/" + clean_id + "/config"

publish("trains/status", "online", 0, True)