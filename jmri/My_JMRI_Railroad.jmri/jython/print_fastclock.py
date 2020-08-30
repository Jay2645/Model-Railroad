import java
import java.beans
import jmri

FAST_CLOCK_PATH = "trains/utilities/fast_clock"

timebase = jmri.InstanceManager.getDefault(jmri.Timebase)

publish(FAST_CLOCK_PATH, str(timebase.getTime()), 0, True)

class TimeListener(java.beans.PropertyChangeListener):
    def propertyChange(self, event):
        publish(FAST_CLOCK_PATH, str(timebase.getTime()), 0, True)

timebase.addMinuteChangeListener(TimeListener())
