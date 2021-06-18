Le programme est en mesure de faire les relevés pour les capteurs suivants:
- DHT22 (capteur de température, humidité et indice de chaleur)
- TSL2560 (capteur de luminosité)
- MPL3115 (baromètre, thermomètre, altimètre)
- Micro
- Cardio

Le programme peut fonctionner en l'absence de ces capteurs. Le programme arduino est en mesure de savoir si un capteur
est présent ou non, en cas d'absence, les valeurs qui auraient été relevées par ce capteur sont remplacées par le caractère '/'
dans la ligne envoyée au port serial.

Les capteurs peuvent être ajouté et retiré librement lors de l'execution du programme sans générer de problèmes ou d'incohérence
dans les mesures relevées (à l'exception du Cardio qui interrompt l'éxecution du programme s'il est ajouté durant l'execution)

Dans le cas du micro, pour déterminer sa présence ou son absence, on lit avec 'analogRead' le niveau de la broche qui doit normalement
être reliée au micro, et une autre broche analogique non utilisée (la 'broche témoin') si les 2 valeurs sont suffisament proches 
(valeurs égales plus ou moins un certain seuil qu'il est possible de définir), alors on considère qu'il n'y a pas de micro, sinon
on considère qu'il est bien présent. À noté que la présence du shield impacte la différence des mesures observées entre 2 broches
inutilisées, l'écart étant plus important entre ces deux mesures avec la présence du shield.

Le programme python peut gérer ces absences de données et remplir les tables et le fichier csv avec les données disponibles en
ignorant les traitements qui concernent les valeurs absentes (qui correspondent au caractère '/').