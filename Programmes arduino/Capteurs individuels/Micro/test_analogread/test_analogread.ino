// Comme le micro est sensé lire sur le port A0, je voulais voir si, sans le micro, c'est la même chose
//pour les 2 broches, afin de voir si le micro est bien présent ou non

void setup() {
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);

  Serial.begin(9600);

}

void loop() {
  Serial.print("A0:");
  Serial.print(analogRead(A0));
  Serial.print("\t");
  Serial.print("A1:");
  Serial.println(analogRead(A1));
  delay(200);
}

// Vardict : les valeurs ne sont pas toujours égales, mais dans la majorité des cas, on a 1 d'écart
//Je pense qu'avec +/- 5, on peut affirmer que les deux broches sont indentiques et qu'il n'y a pas de micro
//ATTENTION : faut pas que le potentiomètre rattaché aux micro soit dans la plage de valeur (400 après réinitialisation,
// redescend vers les 350 par la suite)
