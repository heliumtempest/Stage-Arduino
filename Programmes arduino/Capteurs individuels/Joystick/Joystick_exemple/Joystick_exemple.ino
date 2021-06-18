/*
  Thumb Joystick demo v1.0
  by:https://www.seeedstudio.com
  connect the module to A0&A1 for using;
*/
 
void setup()
{
    Serial.begin(9600);
}
 
void loop()
{
    //Si le joystick est branché sur le port A0 du shield
    int sensorValue1 = analogRead(A0);
    int sensorValue2 = analogRead(A1);

    //Si le joystick est branché sur le portA3 du shield
    //int sensorValue1 = analogRead(A3);
    //int sensorValue2 = analogRead(A4);
 
    Serial.print("The X and Y coordinate is:");
    Serial.print(sensorValue1, DEC);
    Serial.print(",");
    Serial.println(sensorValue2, DEC);
    Serial.println(" ");
    delay(200);
}
