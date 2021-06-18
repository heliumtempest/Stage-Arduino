#include <Wire.h>

int seuil = 80; //Seuil de fréquence cardiaque qui détermine quelle diode allumer
int DIODE_BAS = 8; //Diode allumée lorsque la valeur est inférieure au seuil
int DIODE_HAUT = 9; //Diode allumée lorsque la valeur est supérieur au seuil

void setup() {
    Serial.begin(9600);
    pinMode(DIODE_BAS,OUTPUT);
    pinMode(DIODE_HAUT,OUTPUT);
	// Les deux diodes sont d'abord éteintes
    digitalWrite(DIODE_BAS, LOW);
    digitalWrite(DIODE_HAUT, LOW);
    Serial.println("Cardio");
    Wire.begin();
}
void loop() {
    Wire.requestFrom(0xA0 >> 1, 1);    // request 1 bytes from slave device
    while(Wire.available()) {          // slave may send less than requested
        unsigned char c = Wire.read();   // receive heart rate value (a byte)
        Serial.print(c, DEC);         // print heart rate value
        if(c <= seuil) {
          digitalWrite(DIODE_BAS, HIGH);
          digitalWrite(DIODE_HAUT, LOW);
        }
        else {
          digitalWrite(DIODE_BAS, LOW);
          digitalWrite(DIODE_HAUT, HIGH);
        }
        
    }
    Serial.print(F(" "));
    Serial.println(millis());
    delay(500);
}
