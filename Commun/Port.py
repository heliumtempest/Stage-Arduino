import serial.tools.list_ports
# Je crois qu'il faut installer 'pyserial' avant
import time
import importlib

# TODO le code est pas très "propre"
# TODO faire des try/except un peu partout
class Port:
    baud = 9600  # A specifier si besoin
    port = None
    bdd = None #TODO voir comment faire ça plus efficacement
    textBoxQT = None

    def selectionner_port(self):
        liste_ports = serial.tools.list_ports.comports(include_links=False)
        nombre_ports = len(liste_ports)
        if(nombre_ports == 0):
            print("Aucun port n'a été trouvé")
            exit()
        elif(nombre_ports == 1):
            # Assignation du port par le seul port trouvé
            self.port = liste_ports[0]
            print("Un port trouvé : ", self.port.name)
        else: # Plus de 1 port
            print("Port disponibles :")
            num_port = 0
            for port in liste_ports:
                print("Port n°", num_port, ":", port.name)
            # Demande à l'utilisateur de choisir un port
            choix_port = input("Choix du numéro de port à sélectionner : ")
            self.port = liste_ports[int(choix_port)]

    def lire_port(self):
        #port = self.selectionner_port()
        #print("Connexion au port : ", self.port)

        if self.port is None:
            print("Fermeture de l'appli")
            exit()

        arduino = serial.Serial(self.port.device, baudrate=self.baud)
        print('Connexion au port ' + arduino.name + ' à une vitesse en baud de ' + str(self.baud))

        # Réinitialisation
        arduino.setDTR(False)
        time.sleep(0.1)
        arduino.setDTR(True)

        # Vidage du Buffer
        arduino.flushInput()

        #Lecture de la 1ère ligne reçue
        ligne_1 = arduino.readline().decode("utf-8")
        id_programme = ligne_1[:-2]  # Retrait du '\n' de fin de ligne
        # Identification du programme arduino
        print("Nom du programme arduino :", id_programme)
        # Importation du module python correspondant
        # Attention à bien vérifier l'exactitude des noms
        module = "Capteurs." + id_programme + "." + id_programme  # Nom du répertoire correspondant
        cl_cpt = importlib.import_module(module)  # Importation du module à partir du nom de répértoire
        cpt = cl_cpt.Capteur()  # Instanciation d'un objet pour le capteur
        # TODO je ne sais pas si une telle erreur est réalisable

        # TODO je vais essayer de prendre la bdd sans passer par le port
        if(self.bdd != None):
            cpt.bdd = self.bdd
        else:
            print("Erreur : connexion vers la base de données invalide")
            exit()

        # Création de la table (si elle n'existe pas déjà)
        # Le script SQL doit comporter l'instruction 'CREATE TABLE IF NOT EXISTS'
        # TODO l'exception est pas déjà gérée sur 'creer_table()' ?
        try:
            cpt.creer_table()
        except:
            print("Échec de la procédure creer_table()")
            #raise
            exit()

        # Lecture en continu du reste des données
        try:
            while True:
                ligne = arduino.readline().decode("utf-8")
                ligne = ligne[:-2]  # Retrait du '\n' de fin de ligne
                if ligne != "":
                    # Opérations liées au capteur
                    cpt.afficher_console(ligne)
                    cpt.inserer_bdd(ligne)
                    cpt.ecrire_csv(ligne)

        except:
            print("Lecture interrompue")
            raise
            exit()

    # TODO C'est une fonction pour QT, à voir si elle nous est utile
    def ports_dispo(self):
        """Retourne la liste des noms de ports disponibles"""
        # Recherche les ports disponibles
        liste_ports = serial.tools.list_ports.comports(include_links=False)
        liste_noms = []
        for port in liste_ports:
            liste_noms.append(str(port.name))
        if len(liste_ports) < 1:
            liste_noms.append("Aucun port détecté")
        return liste_noms

    # TODO idem, juste pour QT
    def assigner_port(self, nom_port):
        """Assigne l'attribur 'port' à l'objet à partir du nom su port"""
        if(nom_port == "Aucun port détecté"):
            exit() #TODO c'est un peu radical
        else:
            liste_ports = serial.tools.list_ports.comports(include_links=False)
            for port in liste_ports: #TODO il y a peut-être moyen de mieux coder ça
                if port.name == nom_port:
                    self.port = port




# Exception lorsque le port est débranché :
# raise SerialException("ClearCommError failed ({!r})".format(ctypes.WinError()))
# serial.serialutil.SerialException: ClearCommError failed (PermissionError(13, 'Le périphérique ne reconnaît pas la commande.', None, 22))

# Zone pour test
# test = Port()
# test.selectionner_port()
# test.lire_port()