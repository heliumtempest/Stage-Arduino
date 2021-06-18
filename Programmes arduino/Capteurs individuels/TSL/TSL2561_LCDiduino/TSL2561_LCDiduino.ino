#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#include <LiquidCrystal.h>

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
    Wire.begin();
    Serial.begin(9600);
    TSL2561.init();
    Serial.println("TSL2561");
    
    lcd.begin(16, 2);
}

void loop() {
    //Serial.print("The Light value is: ");
    Serial.print(TSL2561.readVisibleLux());
    Serial.print(F(" "));
    Serial.print(TSL2561.readIRLuminosity()); //Valeur en infra-rouge, non convertie en Lux
    Serial.print(F(" "));
    Serial.print(TSL2561.readFSpecLuminosity()); //Valeur large-spectre, non convertie en Lux
    Serial.print(F(" "));
    Serial.println(millis());
    delay(1000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(TSL2561.readVisibleLux());
    lcd.print(" lux"); //Rq : 1 peu différenciable de l (lx symbole de lux)
    lcd.setCursor(0, 1);
    lcd.print("IR:");
    lcd.print(TSL2561.readIRLuminosity());
    lcd.print(" PS:"); //Plein Spectre
    lcd.print(TSL2561.readFSpecLuminosity());
}
