#include <LiquidCrystal.h>

const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(9600);
  Serial.println(F("TestHELLO"));

  lcd.begin(16, 2);

  lcd.setCursor(0,0);
  lcd.print("Hello world");
}

void loop() {
  // put your main code here, to run repeatedly:
  lcd.setCursor(0, 1);
  lcd.print(millis()/1000);

}
