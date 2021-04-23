import serial.tools.list_ports
import serial.serialutil # Pour l'exception relative au port débranché
# Je crois qu'il faut installer 'pyserial' avant
import time
import importlib

# TODO le code est pas très "propre"
# TODO faire des try/except un peu partout
class Port:

    def __init__(self):
        self.baud = 9600
        self.port = None
        self.bdd = None  # TODO voir comment faire ça plus efficacement
        self.textBoxQT = None  # TODO à voir comment on gère les fenêtres

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
        else:  # Plus de 1 port
            print("Port disponibles :")
            num_port = 0
            for port in liste_ports:
                print("Port n°", num_port, ":", port.name)
            # Demande à l'utilisateur de choisir un port
            choix_port = input("Choix du numéro de port à sélectionner : ")
            try:
                self.port = liste_ports[int(choix_port)]
            except IndexError:
                # Erreur causée par un "index out of range",
                # c-à-d le numéro entré est plus grand que l'indice max de la liste
                print("Ce port n'existe pas")
            except ValueError:
                # Erreur causée par l'impossibilité de convertir le texte entré par l'utilisateur en un nombre entier
                print("Veuillez saisir un numéro valide")

    def lire_port(self):
        #port = self.selectionner_port()
        #print("Connexion au port : ", self.port)

        if self.port is None:
            # TODO il y a déjà un exit si ce cas de figure se présente dans selectionner_port
            print("Aucun port accessible")
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
        if self.textBoxQT is not None:
            self.textBoxQT.setText("Nom du programme arduino :" + id_programme)
        # Importation du module python correspondant
        # Attention à bien vérifier l'exactitude des noms
        module = "Capteurs." + id_programme + "." + id_programme  # Nom du répertoire correspondant
        cpt = None  # Déclaration de la variable avant son assignation
        try:
            cl_cpt = importlib.import_module(module)  # Importation du module à partir du nom de répértoire
            #cpt = cl_cpt.Capteur()  # Instanciation d'un objet pour le capteur
        except:
            print("Programme non reconnu")
            raise
            exit()
        try:
            cpt = cl_cpt.Capteur()
        except:
            print("Echec de l'instanciation de l'objet représentant le capteur")
            print("Cause possible : toutes les méthodes virtuelles ne sont pas implémentées")
            raise  # Affiche le message d'erreur associé, qui indique quelle méthode n'est pas implémentée
            exit()

        # TODO je ne sais pas si une telle erreur est réalisable
        # TODO je vais essayer de prendre la bdd sans la transmettre du main vers le port
        #Edit : ça risque d'être inutilement complexe
        if(self.bdd != None):
            cpt.bdd = self.bdd
        else:
            print("Erreur : connexion vers la base de données invalide")
            exit()

        # Création de la table (si elle n'existe pas déjà)
        # Le script SQL doit comporter l'instruction 'CREATE TABLE IF NOT EXISTS'
        # TODO l'exception est pas déjà gérée sur 'creer_table()' ?
        # Edit : oui, mais c'est possible de déclarer la méthode, mais avec des arguments non conformes à son utilisation ici
        try:
            cpt.creer_table()
        except TypeError:
            print("Échec de la procédure creer_table() avec erreur de type TypeError)")
            print("Cause possible : la méthode est peut-être mal déclarée. Vérifier les arguments de la méthode")
            #raise
            #exit() # TODO après tout, on peut continuer sans table ??
        except:
            print("Echec de la procédure creer_table()")
            print("Cause possible : l'implémentation de la fonction génère une erreur")
            # C'est à dire tout type d'erreur que peut renvoyer Python lors d'une execution invalide
            # Difficile de donner plus d'indication. Débugger la fonction (afficher des variables, executer des
            # morceaux de code, ...)

        # Lecture en continu du reste des données
        try:
            while True:
                ligne = arduino.readline().decode("utf-8")
                ligne = ligne[:-2]  # Retrait du '\n' de fin de ligne
                if ligne != "":
                    # Opérations liées au capteur
                    #TODO on pourrait un peu uniformiser les noms genrt=e : ecrire_console ; ecrire_bdd ; ecrire_csv
                    cpt.afficher_console(ligne)
                    cpt.inserer_bdd(ligne)
                    cpt.ecrire_csv(ligne)
                    if self.textBoxQT is not None:
                        self.ecrire_textbox(ligne)

        except serial.serialutil.SerialException:
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

    # TODO idem
    def ecrire_textbox(self, ligne):
        # TODO ne s'écrit qu'à la fin de l'execution du programme (ce qui ne sert pas à grand chose)
        texte = self.textBoxQT.toPlainText()
        self.textBoxQT.setPlainText(texte + ligne)
        print("Ecriture dans la box")
        #return


# Exception lorsque le port est débranché :
# raise SerialException("ClearCommError failed ({!r})".format(ctypes.WinError()))
# serial.serialutil.SerialException: ClearCommError failed (PermissionError(13, 'Le périphérique ne reconnaît pas la commande.', None, 22))

# Zone pour test
# test = Port()
# test.selectionner_port()
# test.lire_port()