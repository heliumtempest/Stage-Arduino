#include "w600.h"
#if defined(HAVE_HWSERIAL1) 
  #define WifiSerial Serial1
#elif defined(ARDUINO_SEEED_ZERO) 
  //the different board of samd have different serialx
  #define WifiSerial Serial2   //serial number of seeeduino_zero (compatible with Wio Lite W600)
#elif defined(SEEED_XIAO_M0) 
    #define WifiSerial Serial1   
#else
  SoftwareSerial WifiSerial(2,3);
#endif

#define SERIAL Serial
#define debug  SERIAL

AtWifi wifi;

void setup() {
  Serial.begin(9600);
  debug.begin(9600);
  wifi.begin(WifiSerial,9600);

  
  wifi.sendAT(F("AT+Z"));
  wifi.sendAT(F("AT+WPRT=0"));
  wifi.sendAT(F("AT+SSID=Xperia XZ_8f51"));
  wifi.sendAT(F("AT+KEY=1,0,xk5psx9h"));
  wifi.sendAT(F("AT+NIP=0"));
  bool rejoint = wifi.sendAT(F("AT+WJOIN")); //retourne un bool
  while(!rejoint){
    delay(1500);
    Serial.println("Connexione en cours...");
    rejoint = wifi.sendAT(F("AT+WJOIN"));
  }
  wifi.sendAT(F("AT+SKCT=0,0,145.14.145.48,80,1234"));

/*
  wifi.sendAT(F("AT+SKSND=1,194\n"));
  wifi.sendAT(F("POST /test/script.php HTTP/1.1\n"));
  wifi.sendAT(F("Host: stageiutarduino.000webhostapp.com\n"));
  wifi.sendAT(F("User-Agent: arduino\n"));
  wifi.sendAT(F("Content-Type: application/x-www-form-urlencoded\n"));
  wifi.sendAT(F("Connection: keep-alive\n"));
  wifi.sendAT(F("Content-Length: 6\n\n"));
  //wifi.sendAT(F(""));
  wifi.sendAT(F("coucou\n\n"));
  */

  //wifi.wifiSocketPrepareSend(1, 194); //socket, taille en byte de toute la requête POST (entête + contenu)
  //wifi.ATWrite(F("AT+SKSND=1,194,\n"));
  wifi.sendAT(F("AT+SKSND=1,194,\n"));
  wifi.ATWrite(F("POST /test/script.php HTTP/1.1\n"));
  wifi.ATWrite(F("Host: stageiutarduino.000webhostapp.com\n"));
  wifi.ATWrite(F("User-Agent: arduino\n"));
  wifi.ATWrite(F("Content-Type: application/x-www-form-urlencoded\n"));
  wifi.ATWrite(F("Connection: keep-alive\n"));
  wifi.ATWrite(F("Content-Length: 6\n\n"));
  //wifi.sendAT(F(""));
  wifi.sendAT(F("coucou\n\n"));

}

void loop() {
  // put your main code here, to run repeatedly:

}
