import java
import java.beans
import jmri
import jmri.jmrit.roster

throttle_manager = jmri.InstanceManager.getDefault(jmri.ThrottleManager)
roster_list = jmri.jmrit.roster.Roster.getDefault().matchingList(None, None, None, None, None, None, None)

class LocoListener(java.beans.PropertyChangeListener):
    def __init__(self):
        self.roster_entry = None
        self.is_forward = False
        self.speed = 0.0

    def propertyChange(self, event):
        if str(event.propertyName) == "SpeedSetting":
            self.speed = round(float(event.newValue), 2)
        elif str(event.propertyName) == "IsForward":
            self.is_forward = bool(event.newValue)
        
        self.publish_loco()

    def get_topic(self):
        return get_roster_state_path(self.roster_entry.getId())

    def publish_loco(self):
        publish(self.get_topic(), self.get_payload(), 0, True)

    def get_payload(self):
        if self.is_forward or self.speed == 0.0:
            return self.speed
        else:
            return -1.0 * self.speed

for entry in roster_list.toArray():
    dcc_address = entry.getDccLocoAddress()
    
    listener = LocoListener()
    listener.roster_entry = entry

    throttle_manager.attachListener(dcc_address, listener)
    listener.publish_loco()

    print("Attached to " + str(entry.getId()))
