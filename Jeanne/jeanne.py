#les imports
import os
#from schedular import schedular
import speech_recognition as sr
import pyttsx3 as ttx
import random as rd
import wikipedia
import webbrowser
import pyautogui
import locale
import time
from variableGlobal import VariableGlobalON
from youtubesearchpython import VideosSearch

#Récupération de la date et de l'heure locale.
locale.setlocale(locale.LC_TIME, '')

#La classe principale de l'assistant vocal
class Jeanne:
    # initialisation des paramètres utile au programme
    def __init__(self):
        self.ecouteur = sr.Recognizer()
        self.voixGenerateur = ttx.init()
        self.jeanne = self.voixGenerateur.getProperty('voices')

        self.voixGenerateur.setProperty('jeanne', 'french')

        self.lancer_assistant()

    ###
    # Gestion Audio
    ###
    # création de la fonction qui va faire parler notre programme
    def parler(self, text):
        self.voixGenerateur.say(text)
        self.voixGenerateur.runAndWait()

    # fonction qui indique que l'assistant nous écoute attentivement
    def ecouter(self):
        #on initialise une variable qui sera utilisé dans beaucoup des fonctions suivantes car c'est elle qui prendra en ce que nous allons dire à l'assistant
        commande = ''
        try:
            with sr.Microphone() as source:
                voix = self.ecouteur.listen(source, phrase_time_limit=6)
                commande = self.ecouteur.recognize_google(voix, language='fr-FR')
                commande = commande.lower()
        except:
            pass
        # Confirmation ou non de la bonne saisie
        print(commande)
        return commande

    ###
    # Requête
    ###
    #Ici on crée une fonction pour éteindre Jeanne vocalement
    def eteindreJeanne(self, commande, ecouteON):
        if 'au revoir' in commande:

            if self.confirmation():
                self.parler('Allez mourir je vous pris !')
                ecouteON.Global_OFF()
                return True
            else:
                return True
        else:
            return False
    #fonctionnalité qui nous fais répété quand l'assistant ne comprends pas notre requète
    def bakaJeanne(self, commande):
        if commande != '':
            Test = rd.choice([0, 1, 2, 3])
            texte = ''
            if Test == 1:
                texte = "Utilisateur. Je n'ai pas compris. Rèpète !"
            elif Test == 2:
                texte = "Erreur ! Utilisateur incompréhensible."
            elif Test == 3:
                texte = "Moi pas comprendre."
            else:
                texte = 'Echec de la liaison satélite !'
            self.parler(texte)
        else:
            return None
    #Ici une simple confirmation est demandé pour ne pas qu'il y ait d'erreur de compréhension de la part de l'utilisateur
    def confirmation(self):
        self.parler('Veuilliez confirmer vos dires.')
        commande = self.ecouter()

        if 'oui' in commande:  # or 'affirmatif' or 'ok'
            return True
        else:
            self.parler("Annulation Confirmer")
            return False

    ###
    #  Gestion requête
    ###
    #La fonctionnalité de requète de l'assistant vocal
    def requeteJeanne(self, commande, ecouteON):
        if 'secours' in commande:
            # Jeanne salutation
            self.parler("Jeanne à votre secours, j'écoute ...")
            requete = self.ecouter()
            self.parler(requete)
            # return None#True
        elif self.eteindreJeanne(commande, ecouteON):
            print("Extinction en cours ...")
            # return None#True
        else:
            self.bakaJeanne(commande)
            # print('[ !OK! ]')
            # return None#True

    # Le tuto qui permettra de mieux comprendre comment utiliser l'assistant vocal et ses différentes fonctionnalités

    def getTuto(self,commande):
        #text="Bonjour, je suis Jeanne votre nouvelle radio intelligente, je peux vous être utile dans plusieurs domaines. Je peux vous donner le jour ou l'heure actuelle, je peux également vous renseigner sur la météo, j'ai été créée avec plusiuers information intégrée ce qui peux me faire ressembler à un dictionnaire, je peux également vous mettre votre musique préférée quand vous le voulez, enregistrer une émission de radio vous donner l'actualité du jour ou encore configurer une alarme à l'horaire souhaité."
        #enregistrer="Afin d'enregistrer l'émission de votre choix, il vous suffit de me dire le nom de celle-ci ainsi que le jour et son heure de de diffusion, cela me permettra de savoir précisément à qu'elle moment je dois commencer et terminer l'enregistrement. Vous n'aurez plus qu'à me dire de vous diffuser ce dernier plus tard." ##pour lancer la rediffusion il faudra savoir comment ça se passe
        #alarme="Je peux planifier une alarme pour vous réveiller, vous aider à cuisiner, vous rappeller de prendre vos médicaments ou encore vous pour ne pas oublier l'anniversaire d'un membre de votre famille." ##pour lancer l'alarme, il faudra savoir comment ça se passe
        #actualité="Suite aux évènement qu'il a put se produire un jour donné, je peux vous transmettre les infos les concernant le lendemain même grâce au réseau d'information de la radio."
        #date="Vous ne vous souvenez plus du jour du mois ou de l'année, pas d'inquiétude, je peux vous les donné à n'importe quel moment, il vous suffit de me le demander."
        #musique="Je peux vous lancer vos musiques favorites ou de nouvelles musique via la bande-son de la radio, je peux donc garder en mémoire certaines qui vous plaisent pour vous les diffusé quand vous le souhaitez."
        #information="Je connais la majeur partie des mots que l'on peut trouver dans un dictionnaire, ce qui me permet de vous donner l'information que vous rechercher et de vous l'expliquer tant que vous ne l'avez pas comprit."
        #if('met' in commande and 'tuto' in commande):
            #self.parler(text)
        #elif ("comment" in commande and "enregistrer" in commande):
            #self.parler(enregistrer)
        #elif ("comment" in commande and "alarme" in commande):
            #self.parler(alarme)
        #elif ("comment" in commande and "actualité" in commande):
            #self.parler(actualité)
        #elif ("comment" in commande and "date" in commande):
            #self.parler(date)
        #elif ("comment" in commande and "musique" in commande):
            #self.parler(musique)
        #elif ("comment" in commande and "information" in commande):
            #self.parler(information)
        self.parler("Si vous voulez entendre le tuto il faut décommenter le code correspondant, cela a eté fait ainsi car le tuto est assez long")

    ### Fonction Radio
    def lancer_radio(self):
        return print("Radio lancer")

    #Un Wiki qui permet de savoir ce que l'on veut quand on le veut


    def lancer_wiki(self):
        wikipedia.set_lang("fr")
        self.parler("Quel mot vous voulez chercher ?")
        wiki = self.ecouter()
        try:
            self.parler(wikipedia.summary(f'{wiki}', sentences=1))
        except wikipedia.exceptions.PageError:
            self.parler("Pas de mot reconnu.")
        except wikipedia.exceptions.DisambiguationError as error:
            self.parler("Trop de mot possible")
            return error.options[:5]

    #Fonctionnalité qui permet de lancer youtube en lui indiquant précisément la vidéo souhaité
    def lancer_youtube(self):
        self.parler("Quel video vous voulez regardez ?")
        nomytb = self.ecouter()
        print(nomytb)
        videosSearch = VideosSearch(nomytb, limit=1)
        link = videosSearch.result()['result'][0]['link']
        webbrowser.open(link)

    #Une autre pour quitter Youtube
    def quitter_youtube(self):
        os.system("taskkill /im chrome.exe /f")
        # ATTENTION A CHANGER SUR LINUX !

    #et une pour mettre en pause

    def pause_youtube(self):
        pyautogui.press("space")

    #on fait dire l'heure à l'assistant
    def heures(self):
        t = time.localtime()
        self.parler("il est " + time.strftime('%H:%M'))

    #on fait dire le jour à l'assistant
    def jours(self):
        t = time.localtime()
        self.parler("Nous sommes le " + time.strftime('%A %d/%m/%Y'))

    #On récupère un audio d'une radio dans le but de l'enregistrer et le retransmettre
    def meteo(self):
        sound = "meteo.wav"
        r = sr.Recognizer()
        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source)
            print("En conversion..")
            audio = r.listen(source)
        try:
            texteconvert = r.recognize_google(audio, language='fr-FR')
            print(texteconvert)
        except Exception as e:
            print(e)

    ###
    #  Fonction Maître
    ###
    #La fonction principale qui regroupe toutes les requète sous forme d'un ou de plusieur mots de l'utilisateur et qui va rediriger le programme en fonction de ces dernières.
    def lancer_assistant(self):
        ecouteON = VariableGlobalON()
        # print(ecouteON.getGlobalON())

        while ecouteON.getGlobalON():
            commande = ''
            commande = self.ecouter()

            if 'jeanne' in commande:
                print('Requête en cours')
                self.requeteJeanne(commande, ecouteON)
            elif 'tutoriel' in commande:
                self.getTuto(commande)
            elif 'radio' in commande:
                self.lancer_radio()
            elif 'wikipédia' in commande:
                self.lancer_wiki()
            elif ('mets' and 'youtube') in commande:
                try:
                    self.quitter_youtube()
                    self.lancer_youtube()
                except:
                    self.lancer_youtube()
            elif ('quel' and 'météo') in commande:
                self.meteo()
            elif ('quitter' and 'youtube') in commande:
                self.quitter_youtube()
            elif ('pause' and 'youtube') in commande:
                self.pause_youtube()
            elif ('quel' and 'heure') in commande:
                self.heures()
            elif ('quel' and 'jour') in commande:
                self.jours()



            ## Pour forcer l'arrêt de jeanne si besoin
            if 'stop' in commande:
                ecouteON.Global_OFF()

#if __name__ == '__main__':

Jeanne()