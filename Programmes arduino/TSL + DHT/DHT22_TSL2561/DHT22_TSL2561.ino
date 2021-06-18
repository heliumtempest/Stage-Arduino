#include "DHT.h"
#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22_TSL2561"));

  dht.begin();
  Wire.begin();
  TSL2561.init();
}

void loop() {
  delay(2000); //DHT22 : toutes les 2s
               //TSL2561 : toutes les 1s =>  on prend le max

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Echec de lecture provenant du capteur DHT!"));
    return;
  }
  
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  //Capteur DHT22
  Serial.print(h);
  Serial.print(F(" "));
  Serial.print(t);
  Serial.print(F(" "));
  Serial.print(hic);
  Serial.print(F(" "));
  //Serial.println(millis());

  //Capteur TSL2561
   Serial.print(TSL2561.readVisibleLux());
   Serial.print(F(" "));
   Serial.print(TSL2561.readIRLuminosity()); //Valeur en infra-rouge, non convertie en Lux
   Serial.print(F(" "));
   Serial.print(TSL2561.readFSpecLuminosity()); //Valeur large-spectre, non convertie en Lux
   Serial.print(F(" "));

   //Temps écoulé
   Serial.println(millis());

}
