int sensorPin = A5; // select the input pin for the potentiometervoid
void setup () 
{
  Serial.begin (9600);
}

void loop () 
{
  int sensorValue = analogRead (sensorPin);
  delay (500);
  Serial.println (sensorValue, DEC);
}
