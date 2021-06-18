#include "DHT.h"
#include "rgb_lcd.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

DHT dht(DHTPIN, DHTTYPE);

rgb_lcd lcd;
const int colorR = 255;
const int colorG = 0;
const int colorB = 0;

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22"));

  dht.begin();
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2); //16 caractères par ligne, 2 lignes
  lcd.setRGB(colorR, colorG, colorB);
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

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

  Serial.print(h);
  Serial.print(F(" "));
  Serial.print(t);
  Serial.print(F(" "));
  Serial.print(hic);
  Serial.print(F(" "));
  Serial.println(millis());

  lcd.setCursor(0, 0);
  lcd.print(t);
  lcd.print("C ");
  lcd.print("H:");
  lcd.print(h);
  lcd.print("%");
  lcd.setCursor(0, 1);
  lcd.print("Ind:");
  lcd.print(hic);
  lcd.print(" ");
  lcd.print(millis()/1000);
  lcd.print("s");
  
}
