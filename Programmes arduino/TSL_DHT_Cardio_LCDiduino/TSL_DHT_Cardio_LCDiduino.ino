#include "DHT.h"
#include <Wire.h>
#include <Digital_Light_TSL2561.h>
#include <LiquidCrystal.h>

#define DHTPIN 2
#define DHTTYPE DHT22

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
DHT dht(DHTPIN, DHTTYPE);

int mode = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println(F("TSL_DHT_Cardio"));

  dht.begin();
  Wire.begin();
  lcd.begin(16, 2);
  TSL2561.init();
  pinMode(A0, INPUT);
}

void loop() {
   int bouton = analogRead(A0);
   if(bouton >= 555 && bouton < 790){ //SELECT
    mode = 0;
   }
   if(bouton >= 380 && bouton < 555){ //LEFT
    mode = 1;
   }
   if(bouton < 50){ //RIGHT
    mode = 2;
  }
   
  //Cardio
  unsigned char bpm;
  Wire.requestFrom(0xA0 >> 1, 1);    // request 1 bytes from slave device
  while(Wire.available()) {          // slave may send less than requested
      bpm = Wire.read();   // receive heart rate value (a byte)
      //Serial.print(bpm, DEC);         // print heart rate value      
  }
  //DHT
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Echec de lecture provenant du capteur DHT!"));
    return;
  }
  float hic = dht.computeHeatIndex(t, h, false);
  //TSL
  int lux = TSL2561.readVisibleLux();
  int ir = TSL2561.readIRLuminosity();
  int ps = TSL2561.readFSpecLuminosity();


  Serial.print(bpm);
  Serial.print(F(" "));
  Serial.print(h);
  Serial.print(F(" "));
  Serial.print(t);
  Serial.print(F(" "));
  Serial.print(hic);
  Serial.print(F(" "));
  Serial.print(lux);
  Serial.print(F(" "));
  Serial.print(ir);
  Serial.print(F(" "));
  Serial.print(ps);
  Serial.print(F(" "));
  Serial.println(millis());


  if(mode == 0){
    //Synthèse : bpm, T° et lux
    lcd.clear();
    lcd.print(bpm);
    lcd.print("bpm ");
    lcd.print(millis()/1000);
    lcd.print("s");
    lcd.setCursor(0,1);
    lcd.print(lux);
    lcd.print(" lux ");
    lcd.print(t);
    lcd.print("C");
  }
  if(mode == 1){
    //DHT seulement
    lcd.clear();
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
  if(mode == 2){
    //TSL seulement
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

  delay(1000);
}
