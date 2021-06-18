int sensorPin = A5; //Broche utilisée
int sensorValue = 0;
int val;

void setup()
{
  Serial.begin(9600);
  Serial.println("Micro");
  pinMode(sensorPin, INPUT);
}

void loop()
{
  sensorValue = analogRead(sensorPin);
  Serial.print(sensorValue, DEC);
  Serial.print(" ");
  Serial.println(millis());
  delay(200); //Valeur arbitraire
}
