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
#include "rgb_lcd.h"

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

void setup() {
    Wire.begin();
    Serial.begin(9600);
    TSL2561.init();
    Serial.println("TSL2561");

    lcd.begin(16, 2); //16 caractères par ligne, 2 lignes
    lcd.setRGB(colorR, colorG, colorB);
}

void loop() {
    //TODO optimiser la lecture
    //Serial.print("The Light value is: ");
    Serial.print(TSL2561.readVisibleLux());
    Serial.print(F(" "));
    Serial.print(TSL2561.readIRLuminosity()); //Valeur en infra-rouge, non convertie en Lux
    Serial.print(F(" "));
    Serial.print(TSL2561.readFSpecLuminosity()); //Valeur large-spectre, non convertie en Lux
    Serial.print(F(" "));
    Serial.println(millis());

    //Affichage sur le LCD
    lcd.setCursor(0, 0);
    lcd.print("Lux:");
    lcd.print(TSL2561.readVisibleLux());
    lcd.print(" IR:");
    lcd.print(TSL2561.readFSpecLuminosity());
    lcd.setCursor(0, 1);
    lcd.print("PS:");
    lcd.print(TSL2561.readFSpecLuminosity());
    lcd.print(" ");
    lcd.print(millis()/1000);
    lcd.print("s");
    
    delay(1000);
}