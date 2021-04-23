import Capteurs.CapteurInterface as ci
from Capteurs.DHT22 import DHT22
from Capteurs.TSL2561 import TSL2561

#TODO faire de la doc, nettoyer les commentaire
class Capteur(ci.CapteurInterface):

    def __init__(self):
        # Instanciation des classes pour les modules individuels
        self.dht22 = DHT22.Capteur()
        self.tsl2561 = TSL2561.Capteur()
        self.bdd = None
        self.affichage_console = "Humidité : {h}, Température : {t}, Indice : {i}, Lux : {l}, Luminosité IR : {ir}, " \
                                 "Luminosité Plein Spectre : {ps}, T0+{tec} ms"
        # Pas sûr que la bdd non vide soit attribuée aux sous-objets une fois donné à la classe
        # i.e. je sais pas si les bdd vont toutes avoir la même référence
        # Edit : non, ça doit être une copie de l'objet et pas la même référence qui est passée
        # self.dht22.bdd = self.bdd
        # self.tsl2561.bdd = self.bdd

    # Ligne reçue : humidité, temperature, indice, lux, lumIR, lumFS, tec
    def afficher_console(self, ligne):
        champs = ligne.split(" ")
        #print("Méthode de la classe héritée ; ", ligne)
        affichage = self.affichage_console.format(h=champs[0], t=champs[1], i=champs[2], l=champs[3], ir=champs[4],
                                                  ps=champs[5], tec=champs[6])
        print(affichage)

    def inserer_bdd(self, ligne):
        # TODO expliquer le principe
        # En gros, on s'embête pas, on réutilise les méthodes pour les capteurs individuels.
        # Pour ça faut un peu reformater la ligne reçue pour les capteurs ensembles pour recréer celle qu'on
        # aurait si chaque capteur était seul, afin de pouvoir utiliser les méthodes (puisque c'est pour ce contexte
        # qu'elles ont été créées).
        # TODO c'est pas super opti : on parse, on reforme des str qui seront reparsées
        champs = ligne.split(" ")
        champs_dht22 = champs[0:3]  # Les 3 1ères mesures + temps ecoulé (la borne sup n'est PAS incluse)
        champs_dht22.append(champs[6]) # Rq : j'ai pas trouvé comment le faire en une seule ligne
        champs_tsl2561 = champs[3:7] #(la borne sup n'est PAS incluse)
        ligne_dht22 = ' '.join(champs_dht22)
        ligne_tsl2561 = ' '.join(champs_tsl2561)
        self.dht22.inserer_bdd(ligne_dht22)
        self.tsl2561.inserer_bdd(ligne_tsl2561)


    def ecrire_csv(self, ligne):
        # TODO mettre les csv dans le même dossier ?
        # TODO un seul CSV  avec les 2 mesures ?
        champs = ligne.split(" ")
        champs_dht22 = champs[0:3]  # Les 3 1ères mesures + temps ecoulé (la borne sup n'est PAS incluse)
        champs_dht22.append(champs[6])  # Rq : j'ai pas trouvé comment le faire en une seule ligne
        champs_tsl2561 = champs[3:7]  # (la borne sup n'est PAS incluse)
        ligne_dht22 = ' '.join(champs_dht22)
        ligne_tsl2561 = ' '.join(champs_tsl2561)
        self.dht22.ecrire_csv(ligne_dht22)
        self.tsl2561.ecrire_csv(ligne_tsl2561)

    def creer_table(self):
        # La connexion avec la base de données n'a pas encore été transmise aux objets dht22 et tsl2561
        # Ce n'est pas possible de le faire à l'initialisation car la BDD n'est pas connue
        # TODO sauf si on peut passer la bdd en paramètre
        # Mais lorsque cette fonction doit-être executée, la connexion a été assignée, on peut alors la transmettre
        # TODO c'est quand même du bricolage... je dis ça je dis rien
        # -> on peut aller cherhcher les scripts nous même et les executer avec la co plutôt que de passer par les sous-objets
        self.dht22.bdd = self.bdd
        self.tsl2561.bdd = self.bdd
        self.dht22.creer_table()
        self.tsl2561.creer_table()
        # Remarque : pas de table spécifique pour les mesures conjointes de capteurs
