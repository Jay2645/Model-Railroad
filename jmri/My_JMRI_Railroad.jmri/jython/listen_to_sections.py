import java
import java.beans
import jmri

section_manager = jmri.InstanceManager.getDefault(jmri.SectionManager)
section_name_list = section_manager.getSystemNameList().toArray()

class SectionListener(java.beans.PropertyChangeListener):
    def __init__(self):
        self.is_occupied = False
        self.section = None

    def propertyChange(self, event):
        print(event.newValue)
        
    def get_topic(self):
        return get_roster_state_path(self.roster_entry.getId())

    def publish_loco(self):
        publish(self.get_topic(), self.get_payload(), 0, True)

    def get_payload(self):
        return self.is_occupied

for section_name in section_name_list:
    section = section_manager.getSection(section_name)
    
    listener = SectionListener()
    listener.section = section
    
    section.addPropertyChangeListener(listener)


