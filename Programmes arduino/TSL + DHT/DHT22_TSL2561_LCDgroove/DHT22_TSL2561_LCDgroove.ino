#include "DHT.h"
#include <Wire.h>
#include "Digital_Light_TSL2561.h"
#include "rgb_lcd.h"

#define DHTPIN 2
#define DHTTYPE DHT22

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

DHT dht(DHTPIN, DHTTYPE);

int mode = 3;

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22_TSL2561"));

  dht.begin();
  Wire.begin();
  lcd.begin(16, 2);
  TSL2561.init();
  pinMode(A0, INPUT);
}

void loop() {
  
  delay(1000); 

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Echec de lecture provenant du capteur DHT!"));
    return;
  }
  float hic = dht.computeHeatIndex(t, h, false);
  
   //1ère ligne : DHT avec température et humidité (indice de chaleur non affiché)
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print(t, 1);
   lcd.print("C H:");
   lcd.print(h, 1);
   lcd.print("%");
   //2ème ligne
   lcd.setCursor(0, 1);
   lcd.print("L:");
   lcd.print(TSL2561.readVisibleLux());
   lcd.print(" I:");
   lcd.print(TSL2561.readIRLuminosity());
   lcd.print(" P:");
   lcd.print(TSL2561.readFSpecLuminosity());   
   
 

}
