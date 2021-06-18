/*
  Demonstrates how to connect the W600 module to a wifi access point and send some data to AdafruitIO via httpPost. 

  created 12 Oct, 2019
  by Finn Lattimore

  This example code is in the public domain.
 */
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

const char *TARGET_IP   = "145.14.145.48"; //"https://stageiutarduino.000webhostapp.com"; // This is the IP address for AdafruitIO           
uint16_t TARGET_PORT = 80;
uint16_t LOCAL_PORT  = 1234;


int connect_to_AP(int retries){
  bool ssid_set = false;
  bool psswd_set = false;
  bool joined = false;
  int attempt = 0;
  debug.println(F("setting ssid ..."));
  while (!ssid_set && attempt < retries){
      ssid_set = wifi.wifiStaSetTargetApSsid(F("Xperia XZ_8f51")); //TODO put in access point name here
      delay(150);
  } if (!ssid_set){
    debug.println(F("failed to set ssid"));
    return 0;
  }
  
  attempt = 0;
  debug.println(F("setting password"));
  while (!psswd_set && attempt < retries){
    psswd_set = wifi.wifiStaSetTargetApPswd(F("xk5psx9h")); //TODO put in access point password here
    delay(150);
  } if (!psswd_set){
    debug.println(F("failed to set password"));
    return 0;
  }

  attempt = 0;
  while (!joined && attempt < retries){
      joined = wifi.sendAT(F("AT+WJOIN")); //join network
      delay(1500);
  } if (!joined){
      debug.println(F("failed to join network"));
      return 0;
  }

  debug.println(F("connected to AP"));
  return 1;
}


char value[] = "value=44.6\n\n"; // the data to post
int socket = -1;
void setup()
{
    //debug.begin(115200);
    debug.begin(9600); //fonctionne bien mieux
    wifi.begin(WifiSerial,9600);

    configure_wifi(5);
    connect_to_AP(5);
    //socket = create_socket(5);

    /*
    wifi.httpPost(
      socket,
      F("POST /test/script.php HTTP/1.1\n"),
      F("Host: stageiutarduino.000webhostapp.com\n"),
      F("User-Agent: arduino\n"),
      F("Content-Type: application/x-www-form-urlencoded\n"),
      F("Accept: *\/*\n"),
      value //"value=44.6\n\n"
    ); 
    */
    
    
       
}

void loop()
{
  /*String tmp = "value=" + String(millis()) + "\r\n";
  char * valeurs = &tmp[0]; //malloc(sizeof(char) * tmp.length() + 1);*/
  char valeurs[]="value='coucou'\n\n";
  //char value[] = "value=44.6\n\n";

  /*
  Serial.println("************");
  Serial.println(valeurs);
  Serial.println("--------------");
  */

  //socket = create_socket(5);

    //configure_wifi(5);
    //connect_to_AP(5);
    //socket = create_socket(5);

  
     wifi.httpPost(
      socket,
      F("POST /test/script.php HTTP/1.0\n"),
      F("Host: stageiutarduino.000webhostapp.com\n"),
      F("User-Agent: arduino\r\n"),
      F("Content-Type: application/x-www-form-urlencoded\n"),
      F("Connection: keep-alive\r\n"),
      //F("Accept: */*\n"), //Attention à l'échapement
      valeurs //"value='coucou'\n\n"
    ); 

    char donnees[] = "coucou";
    //post_data(socket, donnees);
    // Remplacer \r\n et \n
    //Il semble que rien n'est écrit dans le 'POST' (vient peut-être de l'implémentation de la méthode...)
 

    delay(15000);
}

int create_socket(int retries){
  int socket = -1;
  for (int attempt = 0; attempt < retries; attempt ++){
    debug.print(F("Creating socket to remote server, attempt:"));debug.println(attempt+1);
    socket = wifi.wifiCreateSocketSTA(TCP,Client,TARGET_IP,TARGET_PORT,LOCAL_PORT);
    if (socket >= 0) {
      debug.print(F("connected to remote server. Socket="));debug.println(socket);
      delay(400);
      return socket;
    }
    delay(1000);
  }
  debug.println(F("failed to connect to remote server"));
  return socket;
}

void configure_wifi(int retries){
  for (int attempt = 0; attempt < retries; attempt ++) {
    debug.print(F("Configuring wifi, attempt:")); debug.println(attempt + 1);
    wifi.sendAT(F("AT+Z")); //wifi_reset
    delay(1500);
    if (wifi.wifiSetMode(STA)){
      debug.println(F("wifi configured"));
      delay(100);
      return;
    }
  }
  debug.println(F("wifi configuration failed"));
}
