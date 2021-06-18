#include <LiquidCrystal.h>

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//int bouton = analogRead(A0);

void setup() {
  lcd.begin(16, 2);
  pinMode(A0, INPUT); //Nécessaire ?
}

void loop() {
  lcd.clear();
  lcd.setCursor(0,0);
  int bouton = analogRead(A0);
  //Rq : aucun bouton -> bouton = 1023
  if(bouton < 50){
    lcd.print("RIGHT");
  }
  if(bouton >= 50 && bouton < 195){
    lcd.print("UP");
  }
  if(bouton >= 195 && bouton < 380){
    lcd.print("DOWN");
  }
  if(bouton >= 380 && bouton < 555){
    lcd.print("LEFT");
  }
  if(bouton >= 555 && bouton < 790){
    lcd.print("SELECT");
  }
  if(bouton >= 790){ //La fiche tecnhique indique 1000
    lcd.print("NONE");
  }

  lcd.setCursor(0,1);
  //lcd.print(millis()/1000);
  lcd.print(bouton);

  delay(500); //Attendre 0.5s (le pauvre écran sinon)
}
