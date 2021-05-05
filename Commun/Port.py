try:
    import serial.tools.list_ports
    import serial.serialutil  # Pour l'exception relative au port débranché
except ModuleNotFoundError:
    # Installation du module 'pyserial' s'il n'est pas présent
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial"])

import time
import importlib


# TODO le code est pas très "propre"
# TODO faire des try/except un peu partout => c'est +/- fait
# TODO faire des raise est peut-être pas le plus pertinent
class Port:

    def __init__(self):
        self.baud = 9600  # TODO donner la possibilité de modifier la valeur
        self.port = None
        self.textBoxQT = None  # TODO à voir comment on gère les fenêtres

    def selectionner_port(self):
        # Rq : aucune connexion avec le port n'est établie dans cette fonction
        # Lister les ports détectés
        liste_ports = serial.tools.list_ports.comports(include_links=False)
        nombre_ports = len(liste_ports)
        if(nombre_ports == 0):
            print("Aucun port n'a été trouvé")
            exit()
        elif(nombre_ports == 1):
            # Assignation du port par le seul port trouvé
            self.port = liste_ports[0]
            print("Un port trouvé : ", self.port.name)
        else:  # Plusieurs ports disponibles
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
        """Lit en continu les informations reçues par le port en série"""

        if self.port is None:
            # TODO il y a déjà un exit si ce cas de figure se présente dans selectionner_port
            print("Aucun port accessible")
            print("Fermeture de l'appli")
            exit()

        # Connexion au port (qui a été assigné avec la fonction selectionner_port())
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
        # TODO les trucs pout QT, à voir comment organiser le tout
        if self.textBoxQT is not None:
            self.textBoxQT.setText("Nom du programme arduino :" + id_programme)
        # Importation du module python correspondant à partir du nom de programme
        # Attention à bien vérifier l'exactitude des noms
        module = "Capteurs." + id_programme + "." + id_programme  # Nom du répertoire correspondant
        cpt = None  # Déclaration de la variable avant son assignation
        try:
            cl_cpt = importlib.import_module(module)  # Importation du module à partir du nom de répértoire
        except ModuleNotFoundError:
            print("Aucun module python correspondant au nom du programme a été trouvé")
            # Le arduino doit dans son programme indiquer le nom du porgramme (dans le 'setup')
            # Ce nom est utilisé pour récupérer le module python qui lui est associé
            # Causes d'erreur possible : nom du programme non retourné par le arduino, mauvais emplacement du module,
            # nom incorrect,...
            raise
            exit()
        try:
            cpt = cl_cpt.Capteur()
        except TypeError:
            print("Échec de l'instanciation de l'objet représentant le capteur")
            print("Cause possible : toutes les méthodes virtuelles ne sont pas implémentées")
            raise  # Affiche le message d'erreur associé, qui indique quelle méthode n'est pas implémentée
            exit()
        except AttributeError:  # Capteur() n'est pas reconnu
            print("La classe Capteur() n'est pas défini dans le module python")
            raise
            # Le nom de la classe associée au capteur doit impérativement s'appeler 'Capteur'

        # TODO l'exception est pas déjà gérée sur 'creer_table()' ?
        # TODO l'exception survient avant non ?
        # Edit : oui, mais c'est possible de déclarer la méthode,
        # mais avec des arguments non conformes à son utilisation ici
        # TODO les erreurs doivent-elles être bloquantes ?
        try:
            cpt.creer_table()
        except TypeError:
            print("Échec de la procédure creer_table() avec erreur de type TypeError)")
            print("Cause possible : la méthode est peut-être mal déclarée. Vérifier les arguments de la méthode")
            # La fonction ne prend aucun paramètre
            #raise
            #exit()
        except FileNotFoundError:
            print("La procédure utilise un script qui est introuvable")
            # Le script n'est pas à l'emplacement spécifié.
            # Remarque : la racine du chemin absolu (chemin par rapport à l'espace de travail) est dans le répértoire
            # où se situe le 'main'
        except:
            print("Echec de la procédure creer_table()")
            print("Cause possible : l'implémentation de la fonction génère une erreur")
            raise
            # C'est à dire tout type d'erreur que peut renvoyer Python lors d'une execution invalide
            # Difficile de donner plus d'indication. Débugger la fonction (afficher des variables, executer des
            # morceaux de code, ...)

        # Lecture en continu du reste des données
        try:
            while True:  # Boucle infinie, elle est interrompue seulement en cas d'erreur (p.ex. port débranché)
                ligne = arduino.readline().decode("utf-8")
                ligne = ligne[:-2]  # Retrait du '\n' de fin de ligne
                if ligne != "":
                    # Opérations liées au capteur
                    #TODO on pourrait un peu uniformiser les noms genre : ecrire_console ; ecrire_bdd ; ecrire_csv
                    try:
                        cpt.afficher_console(ligne)
                        cpt.inserer_bdd(ligne)
                        cpt.ecrire_csv(ligne)
                    except TypeError:
                        # Les arguments ne correspondent pas entre l'utilisation faite dans le bloc et leur définition
                        # dans le module
                        # Les procédures ne doivent avoir que la ligne reçue par le capteur en argument
                        print("Au moins une procédure est déclarée avec de mauvais argument")
                        raise
                    except:
                        print("Échec de l'execution d'au moins l'une des procédures")
                        raise

                    if self.textBoxQT is not None:
                        self.ecrire_textbox(ligne)

        except serial.serialutil.SerialException:
            print("Lecture interrompue")
            raise
            exit()

    # TODO C'est une fonction pour QT, à voir si elle nous est utile
    def ports_dispo(self):
        """Retourne la liste des noms de ports disponibles."""
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
        """Assigne l'attribut 'port' à l'objet à partir du nom su port."""
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
