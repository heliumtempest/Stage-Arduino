#include <SoftwareSerial.h>
#define RxD 2
#define TxD 3

//Site hebergé : https://stageiutarduino.000webhostapp.com/
//IP du site : 145.14.145.48
/*
 * AT+WPRT=0
 * AT+SSID=Xperia XZ_8f51
 * AT+KEY=1,0,xk5psx9h
 * AT+NIP=0
 * AT+PMTF //Après cette commande, on peut directement faire 'AT+WJOIN' sans les étapes précédantes pour se connecter de nouveau
 * AT+WJOIN
 * AT+SKCT=0,0,145.14.145.48,80,1234
 */
 /*
  * AT+LKSTT //Donne l'IP de la connexion reseau (et autres info)
  * AT+PING=https://stageiutarduino.000webhostapp.com,1000,0,1 //Il dit juste 'OK'
  */

#define DEBUG_ENABLED 1

SoftwareSerial BLE(RxD, TxD);

void setup() {
  Serial.begin(9600);
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  setupBleConnection();

  attente_ok("AT+WPRT=0");
  attente_ok("AT+SSID=Xperia XZ_8f51");
  attente_ok("AT+KEY=1,0,xk5psx9h");
  attente_ok("AT+NIP=0");
  attente_ok("AT+WJOIN"); //Avait fait une erreur une fois, mais OK lorsque commande relancée
  attente_ok("AT+SKCT=0,0,145.14.145.48,80,1234"); //Création d'un socket

  attente_ok("AT+SKSND=1,194");
  BLE.println("POST /test/script.php HTTP/1.1");
  BLE.println("Host: stageiutarduino.000webhostapp.com");
  BLE.println("User-Agent: arduino");
  BLE.println("Content-Type: application/x-www-form-urlencoded");
  BLE.println("Connection: keep-alive");
  BLE.println("Content-Length: 6");
  BLE.println(""); //Ligne vide entre 'content length' et le 'contenu'
  BLE.println("coucou\n\n");
  
  

}

void loop() {
  char recvChar;
  //BLE.write("AT+"); //Err -1 (trop tôt et la co n'a pas eu le temps de s'établir lorqu'on demande AT+ ??)
  //Erreur -1 : invalid command format (pourtant la ligne marche bien quand on la tape sur le moniteur)
  while(1) {
    if(BLE.available()) { //Check if there's any data sent from the remote BLE
      recvChar = BLE.read();
      Serial.print(recvChar);
    }
    if(Serial.available()) { //Check if there's any data sent from the local serial terminal, you can add the other application here
      recvChar = Serial.read();
      BLE.print(recvChar);
    }
  }

}

void attente_ok(String commande){
  BLE.println(commande);
  bool ok=false;
  String reponse = "";
  while(!ok){
    if(BLE.available() > 0){
      char recvChar = BLE.read();
      if(recvChar == '+' || recvChar == 'O' || recvChar == 'K' ||recvChar == 'E' || recvChar == 'R'){
        reponse += recvChar; 
      }
    }
    if(reponse == "+OK" ||reponse == "+ERR"){
      ok = true;
      Serial.print(commande);
      Serial.print(" -> ");
      Serial.println(reponse);
    }
  }
}

void setupBleConnection(){
  BLE.begin(9600); //Set BLE BaudRate to default baud rate 9600
}
