void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(7, INPUT);
  pinMode(6, OUTPUT);
}

void writePin(uint8_t readPin, uint8_t writePin)
{
  int readValue = digitalRead(readPin);
  Serial.println(readValue);

  if (readValue < 1)
  {
    digitalWrite(writePin, HIGH);
  }
  else
  {
    digitalWrite(writePin, LOW);
  }
}

void loop()
{
  writePin(7, 6);
  delay(100);
}
