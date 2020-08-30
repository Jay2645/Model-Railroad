import jmri

# Define the shutdown task
class ShutdownMQTT(jmri.implementation.AbstractShutDownTask):
  def run(self):
    publish("trains/status", "offline", 0, True)
    
shutdown.register(ShutdownMQTT("MQTT Shutdown"))

 