#include "arduino_secrets.h"

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Function prototypes
bool doesPinHaveData(uint8_t readPin);

// Pins to read
static const uint8_t PINS_TO_CHECK[] =  { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

// Ethernet and MQTT related objects
static byte MAC_ADDRESS[] = { 0xA8, 0x61, 0x0A, 0xAE, 0x7D, 0xB1 };
static const IPAddress IP_ADDRESS(192, 168, 86, 44);
static const char* MQTT_TOPIC = "trains/helix";

static const char* MQTT_ID = "helix";
static const char* MQTT_USERNAME = "mqtt";
static const char* MQTT_PASSWORD = SECRET_MQTT_PASSWORD;
 
static const char* SERVER_ADDRESS = "192.168.86.223";
 
EthernetClient ethClient;
PubSubClient mqttClient(ethClient);

bool activePins[] = { false, false, false, false, false, false, false, false, false, false };
static_assert(sizeof(PINS_TO_CHECK) == sizeof(activePins), "Pin size mismatch");
bool hasChanged = false;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  for(int i = 0; i < sizeof(PINS_TO_CHECK); i++)
  {
    pinMode(PINS_TO_CHECK[i], INPUT);
  }
  
  // Start the ethernet connection
  if (Ethernet.begin(MAC_ADDRESS) == 0)
  {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware)
    {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) 
      {
        delay(1); // do nothing, no point running without Ethernet hardware
      }
    }
    if (Ethernet.linkStatus() == LinkOFF) 
    {
      Serial.println("Ethernet cable is not connected.");
    }
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(MAC_ADDRESS, IP_ADDRESS);
  } 
  else 
  {
    Serial.print("DHCP assigned IP ");
    Serial.println(Ethernet.localIP());
  }

  // Ethernet takes some time to boot!
  delay(4000);                          
 
  Serial.println("Connecting...");
  
  // Set the MQTT server to the server stated above
  mqttClient.setServer(SERVER_ADDRESS, 1883);   
  // Attempt to connect
  if (mqttClient.connect(MQTT_ID, MQTT_USERNAME, MQTT_PASSWORD)) 
  {
    Serial.println("Connection has been established");

    // Upload the current status when we connect for the first time
    hasChanged = true;
  } 
  else 
  {
    Serial.println("Server connection failed!");
  }
}

bool doesPinHaveData(uint8_t readPin)
{
  const int readValue = digitalRead(readPin);
  Serial.print("Pin #");
  Serial.print(readPin);
  Serial.print(" has value of ");
  Serial.println(readValue);

  return readValue < 1;
}

void loop()
{
  mqttClient.loop();

  for (int i = 0; i < sizeof(PINS_TO_CHECK); i++)
  {
    const bool hasData = doesPinHaveData(PINS_TO_CHECK[i]);
    hasChanged |= hasData != activePins[i];
    activePins[i] = hasData;
  }

  if (hasChanged)
  {
    // Change detected, tell the server    
    String payloadString = "{";
    for (int i = 0; i < sizeof(PINS_TO_CHECK); i++)
    {
      payloadString += "\"block_" + String(PINS_TO_CHECK[i]) + "\":";
      payloadString += activePins[i] ? "\"ON\"" : "\"OFF\"";
      if (i < sizeof(PINS_TO_CHECK) - 1)
      {
        payloadString += ",";
      }
    }
    payloadString += "}";

    
    Serial.println("Detection changed, payload: " + payloadString);

    mqttClient.publish(MQTT_TOPIC, payloadString.c_str(), true);
    
    hasChanged = false;
  }

  delay(100);
}