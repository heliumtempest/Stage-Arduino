/*
  Thumb Joystick demo v1.0
  by:https://www.seeedstudio.com
  connect the module to A0&A1 for using;
*/
 
void setup()
{
    Serial.begin(9600);
    Serial.println("Joystick");
}
 
void loop()
{
    int sensorValue1 = analogRead(A0);
    int sensorValue2 = analogRead(A1);

 /*
    Serial.print("The X and Y coordinate is:");
    Serial.print(sensorValue1, DEC);
    Serial.print(",");
    Serial.println(sensorValue2, DEC);
    Serial.println(" ");
    delay(200);
*/
    Serial.print(sensorValue1); //coordonnée X
    Serial.print(" ");
    Serial.print(sensorValue2); //Coordonnée Y
    Serial.print(" ");
    Serial.println(millis());

    delay(200);
}
