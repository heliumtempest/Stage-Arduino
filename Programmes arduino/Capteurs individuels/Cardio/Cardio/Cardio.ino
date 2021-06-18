#include <Wire.h>
void setup() {
    Serial.begin(9600);
    Serial.println("Cardio");
    Wire.begin();
}
void loop() {
    Wire.requestFrom(0xA0 >> 1, 1);    // request 1 bytes from slave device
    while(Wire.available()) {          // slave may send less than requested
        unsigned char c = Wire.read();   // receive heart rate value (a byte)
        Serial.print(c, DEC);         // print heart rate value
        // Rq : DEC est un paramètre optionel qui indique que 'c' doit être exprimé en base 10
        
    }
    Serial.print(F(" "));
    Serial.println(millis());
    delay(500);
}
