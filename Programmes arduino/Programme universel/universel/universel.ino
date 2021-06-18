/* Bloc DHT */
#include "DHT.h"
#define DHTPIN 2 //Broche utilisée par le DHT
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
/* Utilisé par TSL, MPL et le Cardio*/
#include <Wire.h>
/* Bloc TSL */
#include <Digital_Light_TSL2561.h>
/* Bloc MPL */
#include <Adafruit_MPL3115A2.h>
Adafruit_MPL3115A2 baro = Adafruit_MPL3115A2();
/* Bloc Micro */
int microPin = A1; //Broche utilisée par le micro
int temoinPin = A0;  //Broche inutilisée
//Sert de référence à la détéction du micro (il y a toujours une tension sur une broche, même si le capteur n'est pas branché, il la broche où est sensée être branché le micro à la même
//tension qu'un broche sur laquelle il n'y a rien, on considère alors que le micro n'est pas branché. Veiller à regler le potentiomètre pour que les valeurs temoin soient éloignées des valeurs mesurables
// par le micro
int valeurMicro = 0;
int seuil_micro = 30; //Seuil pour lequel on considère qu'il y a un micro ou non en fonction de l'écart entre la valeur témoin et la broche où est censée être branché le micro
// Sa valeur est un peu arbitraire. Régler le potentiomètre de manière à ce que les valeurs mesurées par le micro soient relativement éloigné de la valeur 'témoin'
// Rq : la présence d'un shield rend la différence entre 2 valeurs 'temoin' plus importantes (plutôt déconseillé dans le cas du micro)

void setup() {
  /* Bloc pour tout programme arduino */
  Serial.begin(9600);
  Serial.println("Universel"); //Nom du programme arduino, qui sera reconnu par le programme python
  /* Utilisé par TSL et Cardio*/
  Wire.begin();
  /* Bloc DHT */
  dht.begin();
  /* Bloc TSL */
  TSL2561.init();
  /* Bloc Micro */
  pinMode(microPin, INPUT);
  pinMode(temoinPin, INPUT);
}

void loop() {
  /* Bloc DHT */
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if(isnan(h) || isnan(t)) {
    Serial.print(F("/ / /")); //Les valeurs indéfinies (c'est à dire qui ne peuvent être lues du fait de l'absence de capteur sont remplacée par des '/')
  }
  else{
      float hic = dht.computeHeatIndex(t, h, false);
      Serial.print(h);
      Serial.print(F(" "));
      Serial.print(t);
      Serial.print(F(" "));
      Serial.print(hic);
  }
  Serial.print(F(" "));

  /* Bloc TSL */
  byte error;
  Wire.beginTransmission(0x29);
  error = Wire.endTransmission();
  if(error == 0){
    //Le TSL est bien détecté
    TSL2561.init(); //Avec cette ligne, on peut le rajouter "à la volée" le cacpteur sur le montage
	//Lecture et envoi des données
    Serial.print(TSL2561.readVisibleLux());
    Serial.print(F(" "));
    Serial.print(TSL2561.readIRLuminosity()); //Valeur en infra-rouge, non convertie en Lux
    Serial.print(F(" "));
    Serial.print(TSL2561.readFSpecLuminosity());
  }
  else{
    //Le TSL n'est pas détecté
    Serial.print(F("/ / /"));
  }
  Serial.print(F(" "));

  /* Bloc MPL */
  if (! baro.begin()) {
    //Capteur MPL non détecté
    Serial.print(F("/ / / "));
  }
  else{
    //Capteur MPL détecté
    float pascals = baro.getPressure();
    Serial.print(pascals);
    Serial.print(F(" "));
  
    float altm = baro.getAltitude();
    Serial.print(altm); //Altitude en mètres (par rapport au niveau de la mer)
    Serial.print(F(" "));
  
    float tempC = baro.getTemperature();
    Serial.print(tempC); //Température en °C
    Serial.print(F(" "));
  }

  /* Bloc Cardio */
  //C'est le seul capteur qui bloque le programme lorsqu'il est branché en cours d'execution
  bool lecture_ok = false;
  Wire.requestFrom(0xA0 >> 1, 1);
  while(Wire.available()) {
      unsigned char c = Wire.read();
      Serial.print(c, DEC);
      lecture_ok = true;
     // Rq : DEC est un paramètre optionel qui indique que 'c' doit être exprimé en base 10
      
  }
  if(!lecture_ok){
    Serial.print(F("/"));
  }
  Serial.print(F(" "));

  /* Bloc Micro */
  valeurMicro = analogRead(microPin);
  int temoinValue = analogRead(temoinPin);

  //Vérifie la présence ou non du capteur
  if(valeurMicro > temoinValue + seuil_micro || valeurMicro < temoinValue - seuil_micro){ //La valeur de la broche associée au micro n'a pas un écart de +/- 5 avec la valeur temoin -> il y a un micro
    Serial.print(valeurMicro);
  }
  else{
	//La valeur de la broche du micro et de la broche temoin sont proches, le micro est considéré absent
    Serial.print(F("/"));
  }
  Serial.print(F(" "));
  

  /* Commun à tous les capteurs */
  Serial.println(millis());
  delay(1000); //Arbitraire

}
