#include <Wire.h>
#include <LiquidCrystal.h>

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
    Serial.begin(9600);
    Serial.println("Cardio");
    Wire.begin();
    
    lcd.begin(16, 2);
}
void loop() {
    Wire.requestFrom(0xA0 >> 1, 1);    // request 1 bytes from slave device
    while(Wire.available()) {          // slave may send less than requested
        unsigned char c = Wire.read();   // receive heart rate value (a byte)
        Serial.print(c, DEC);         // print heart rate value
        // Rq : DEC est un paramètre optionel qui indique que 'c' doit être exprimé en base 10

        lcd.setCursor(0, 0);
        lcd.print(c);
        lcd.print(" bpm");
    }
    Serial.print(F(" "));
    Serial.println(millis());
    delay(500);
    lcd.setCursor(0,1);
    lcd.print("Temps:");
    lcd.print(millis()/1000.0,1);
    lcd.print("s");
}
