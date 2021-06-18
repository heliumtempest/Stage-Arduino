/*
    Digital_Light_Sensor.ino
    A library for TSL2561

    Copyright (c) 2012 seeed technology inc.
    Website    : www.seeed.cc
    Author     : zhangkun
    Create Time:
    Change Log :

    The MIT License (MIT)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE. 
*/

#include <Wire.h>
#include <Digital_Light_TSL2561.h>
void setup() {
    Wire.begin();
    Serial.begin(9600);
    TSL2561.init();
    Serial.println("TSL2561");
}

void loop() {
  /*
    int lux = -1;
    int ir = -1;
    int fs = -1;
    Serial.print("The Light value is: ");
    lux = TSL2561.readVisibleLux();
    Serial.print(lux);
    Serial.print(F(" "));
    //ir = TSL2561.readIRLuminosity();
    Serial.print(ir); //Valeur en infra-rouge, non convertie en Lux
    Serial.print(F(" "));
    //fs = TSL2561.readFSpecLuminosity();
    Serial.print(fs); //Valeur large-spectre, non convertie en Lux
    Serial.print(F(" "));
    Serial.println(millis());
    delay(1000);
    */

    //Bien puisque la lecture des valeurs est bloquante sans le capteur, je vais voir si je peux
    //voir si le capteur est présent ou non avant de faire les lectures
    //D'après le .h de la librairie du TSL, l'addresse est 0x29
    //https://create.arduino.cc/projecthub/abdularbi17/how-to-scan-i2c-address-in-arduino-eaadda
    byte address;
    byte error;
    Wire.beginTransmission(0x29);
    error = Wire.endTransmission();
    if(error == 0){
      Serial.println("TSL Trouvé");
    }
    else{
      Serial.println("TSL pas trouvé");
    }
    Serial.print("ms :");
    Serial.println(millis());
    delay(1000);
}
