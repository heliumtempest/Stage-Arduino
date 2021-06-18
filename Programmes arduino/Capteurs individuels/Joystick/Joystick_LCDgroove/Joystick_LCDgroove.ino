/*
  Thumb Joystick demo v1.0
  by:https://www.seeedstudio.com
  connect the module to A0&A1 for using;
*/
#include "rgb_lcd.h"

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

void setup()
{
    Serial.begin(9600);
    Serial.print("Joystick");

    lcd.begin(16, 2); //16 caractères par ligne, 2 lignes
    lcd.setRGB(colorR, colorG, colorB);
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

    lcd.setCursor(0,0)
    lcd.print("X:");
    lcd.print(sensorValue1);
    lcd.print(" Y:");
    lcd.print(sensorValue2);
    lcd.setCursor(0,1);
    lcd.print(millis()/1000.0, 1);

    delay(200);
}
