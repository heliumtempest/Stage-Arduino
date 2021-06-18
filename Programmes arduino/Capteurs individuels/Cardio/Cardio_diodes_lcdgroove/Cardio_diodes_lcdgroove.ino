#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

int seuil = 80;
int DIODE_BAS = 8; //Diode allumée lorsque la valeur est inférieure au seuil
int DIODE_HAUT = 9;

void setup() {
    Serial.begin(9600);
    Serial.println("Cardio");  //Serial.println("heart rate sensor:");
    // Initailisation des diodes
    pinMode(DIODE_BAS,OUTPUT);
    pinMode(DIODE_HAUT,OUTPUT);
    digitalWrite(DIODE_BAS, LOW);
    digitalWrite(DIODE_HAUT, LOW);
    
    Wire.begin();

    // set up the LCD's number of columns and rows:
    lcd.begin(16, 2); //16 caractères par ligne, 2 lignes
    lcd.setRGB(colorR, colorG, colorB);
}
void loop() {
    Wire.requestFrom(0xA0 >> 1, 1);    // request 1 bytes from slave device
    while(Wire.available()) {          // slave may send less than requested
        unsigned char c = Wire.read();   // receive heart rate value (a byte)
        Serial.print(c, DEC);         // print heart rate value
        // Rq : DEC est un paramètre optionel qui indique que 'c' doit être exprimé en base 10

        // Éclairage des diodes
        if(c <= seuil) {
          digitalWrite(DIODE_BAS, HIGH);
          digitalWrite(DIODE_HAUT, LOW);
        }
        else {
          digitalWrite(DIODE_BAS, LOW);
          digitalWrite(DIODE_HAUT, HIGH);
        }

        //Affichage sur le LCD
        lcd.setCursor(0, 0); //1ère colonne, 1ère ligne (les indices commencent à 0)
        lcd.print(c);
        lcd.print(" bpm");                
    }
    Serial.print(F(" "));
    Serial.println(millis());
    // Affichage du temps écoulé sur le LCD
    lcd.setCursor(0,1); //1ère colonne, 2nde ligne
    lcd.print("Temps:");
    lcd.print(millis()/1000.0, 1);
    lcd.print("s");
    delay(500);
}
