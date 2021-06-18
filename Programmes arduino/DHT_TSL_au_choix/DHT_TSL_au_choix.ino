#include <LiquidCrystal.h>

#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
#include <Wire.h>
#include <Digital_Light_TSL2561.h>

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

int etat_dht = -1;
int etat_tsl = -1;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  pinMode(A0, INPUT); //Nécessaire ?

  /* DHT */
  lcd.print("Activer DHT ?");
  lcd.setCursor(0,1);
  lcd.print("Non:<- Oui:->");
  
  while(etat_dht == -1){
    if(analogRead(A0) >= 0 && analogRead(A0) < 50) { //Right
      etat_dht = 1;
    }
    if(analogRead(A0) >= 380 && analogRead(A0) < 555) { //Left
      etat_dht = 0;
    }
  }
  lcd.clear();
  if(etat_dht == 0){
    lcd.print("DHT off");
  }
  if(etat_dht == 1){
    lcd.print("DHT on");
  }
  delay(2000);

  /* TSL */
  lcd.clear();
  lcd.print("Activer TSL ?");
  lcd.setCursor(0,1);
  lcd.print("Non:<- Oui:->");
  while(etat_tsl == -1){
    if(analogRead(A0) >= 0 && analogRead(A0) < 50) { //Right
      etat_tsl = 1;
    }
    if(analogRead(A0) >= 380 && analogRead(A0) < 555) { //Left
      etat_tsl = 0;
    }
  }
  lcd.clear();
  if(etat_tsl == 0){
    lcd.print("TSL off");
  }
  if(etat_tsl == 1){
    lcd.print("TSL on");
  }
  delay(2000);

  /* Setup */
  if(etat_dht == 1){
    dht.begin();
  }
  if(etat_tsl == 1){
    Wire.begin();
    TSL2561.init();
  }

  Serial.print("Etat DHT:");
  Serial.println(etat_dht);
  Serial.print("Etat TSL:");
  Serial.println(etat_tsl);
  
}

void loop() {
 
  if(etat_tsl == 1){

    Serial.print("TSL :  ");
    Serial.print(TSL2561.readVisibleLux());
    Serial.print(F(" "));
    Serial.print(TSL2561.readIRLuminosity()); //Valeur en infra-rouge, non convertie en Lux
    Serial.print(F(" "));
    Serial.print(TSL2561.readFSpecLuminosity()); //Valeur large-spectre, non convertie en Lux
    Serial.print(F(" "));
    //Serial.println(millis());
  }

  if(etat_dht == 1){
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

    Serial.print("DHT:  ");
  
    Serial.print(h);
    Serial.print(F(" "));
    Serial.print(t);
    Serial.print(F(" "));
    Serial.print(hic);
    Serial.print(F(" "));
    //Serial.println(millis());
    }

  Serial.print("Temps:");
  Serial.println(millis());
  lcd.clear();
  lcd.print(millis());
  delay(1000);
}
