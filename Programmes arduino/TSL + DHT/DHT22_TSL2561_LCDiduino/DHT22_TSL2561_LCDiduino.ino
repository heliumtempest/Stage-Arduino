#include "DHT.h"
#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#include <LiquidCrystal.h>
#define DHTPIN 2
#define DHTTYPE DHT22
const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
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
  int lu =  analogRead(A0);
  Serial.println(lu);
  if((lu>=50) && (lu<=195)){
    mode = 1; //Bouton UP
  }
  if((lu >= 195) && (lu<=380)){
    mode = 2; //Bouton DOWN
  }
  if((lu >= 555) && (lu <= 790)){
    mode = 3; //Bouton SELECT
  }
  Serial.println(mode);
  delay(1000); 

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Echec de lecture provenant du capteur DHT!"));
    return;
  }
  float hic = dht.computeHeatIndex(t, h, false);

  if(mode == 1){ //DHT seulement
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(t, 1);
    lcd.print("C");
    lcd.print(" H=");
    lcd.print(h);
    lcd.print("%");
    lcd.setCursor(0,1);
    lcd.print("Ind=");
    lcd.print(hic);
    lcd.print(" ");
    lcd.print(millis()/1000);
    lcd.print("s");
  }

  if(mode == 2){ //TSL seulement
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(TSL2561.readVisibleLux());
    lcd.print(" lux"); //Rq : 1 peu différenciable de l (lx symbole de lux)
    lcd.print("  ");
    lcd.print(millis()/1000);
    lcd.print("s");
    lcd.setCursor(0, 1);
    lcd.print("IR:");
    lcd.print(TSL2561.readIRLuminosity());
    lcd.print(" PS:"); //Plein Spectre
    lcd.print(TSL2561.readFSpecLuminosity());
  }

   if(mode == 3) { //Les 2 capteurs
     //1ère ligne : DHT avec température et humidité (indice de chaleur non affiché)
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print(t);
     lcd.print("C H:");
     lcd.print(h);
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
 

}
