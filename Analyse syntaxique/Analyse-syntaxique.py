import speech_recognition as sr
import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import threading
import time

liste = ["météo", "degré", "ciel", "pluie", "soleil", "température", "brouillards", " temps ", "averse", "orageuses",
             "ensoleillée",
             "anticyclone", "anti-cyclone", "cyclone", "atmosphère", "brise", " vent ", "climat", "dépression", "nuage",
             "orage", "ouragan", "prévision", "brume", "éclair", "foudre", "givre", "grêle", "mousson", "neige",
             "pression", "saison", "sécheresse", "tempête", "tonnerre", "vague de chaleur", "vague de froid",
             "verglas"]
cptAudio = 0
sound = ""


def audioconvert(nomf):
    r = sr.Recognizer()
    print("var sound : ", nomf)
    with sr.AudioFile(nomf) as source:
        r.adjust_for_ambient_noise(source)
        print("En conversion..")
        audio = r.listen(source)
        try:
            global texteconvert
            texteconvert = r.recognize_google(audio, language='fr-FR')
            print(texteconvert)
            return texteconvert

        except Exception as e:
            print(e)


def enregistrer(numaudio):
    global sound
    fs = 44100
    seconds = 30
    sound = (str(numaudio) + ".wav")
    print("enregistrement numéro : " + sound + " en route")

    data = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    y = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
    write(sound, fs, y)


def meteoverif(n):
    global texteconvert, etatMeteo, cptAudio, bMeteo
    compteur = 0
    try:
        for i in range(len(liste)):
            if liste[i] in texteconvert:
                count = texteconvert.count(liste[i])
                print("Le compte est de:", count)
                compteur += count
                print(compteur)

        if compteur >= 3:
            cptAudio += 1
            print("LA METEO ! LA METEO ! LA METEO !")
            return True

        else:
            if n > 0 and n <= 9:
                os.remove(str(n - 1) + ".wav")
            else:
                os.remove(sound)
            cptAudio = 0
            print("pas meteo")
            return False
    except NameError as e:
        print(e)


def fusion(infiles):
    import wave
    # infiles = ["0.wav",sound]
    outfile = "FusionT.wav"

    data = []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()
    try:
        os.remove(infiles[0])  # suppression des fichies inutiles pour un gain de mémoire et renommer la fusion des deux comme étant le dernier fichier son
        os.remove(infiles[1])
        os.rename(outfile, infiles[1])

    except FileExistsError as e:
        print("this file does not exist : ", e)


def Ftest(n):
    if cptAudio > 1:
        try:
            fusion([str(n - 2) + ".wav", str(n-1) + ".wav"])

        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)


if __name__ == "__main__":

    # threads qui vont paralleliser l'enregistrement et l'analyse du précédent enregistrement
    bMeteo = False
    while True:
        n = 0
        if cptAudio == 0:
            enregistrer(n)

        for n in range(1, 10):
            # n = i
            th1 = threading.Thread(target=enregistrer, args=[n])
            th2 = threading.Thread(target=audioconvert, args=[str(str(n - 1) + ".wav")])
            th1.start()
            th2.start()
            th1.join()
            th2.join()
            bMeteo = meteoverif(n)
            Ftest(n)

        print("premier print test : ", os.listdir())
        audioconvert(str(n) + ".wav")
        bMeteo = meteoverif(n + 1)
        Ftest(n)


        try:
            fil = os.listdir()
            for file in fil:

                if file.find(".wav") != -1 and cptAudio > 0:
                    if bMeteo:
                        os.rename(file, "0.wav")
                    else:
                        try:
                            os.remove("bulletin.wav")
                        except Exception:
                            pass
                        os.rename(file, "bulletin.wav")
                elif file.find(".wav") != -1 and file.find("bulletin.wav") != -1:
                    print("dernier print test : ", os.listdir())

        except FileExistsError as e:
            print(e)

    '''
        version obsolète
        th1 = threading.Thread(target=enregistrer, args=[cptAudio])
        th1.start()
        try:
            th2 = threading.Thread(target=audioconvert, args=[sound])
            th2.start()

        except FileNotFoundError as e:
            print("indeed it's : ",e)
        except NameError as e:
            print("indeed it's : ", e)

        th1.join()
        th2.join()
        if cptAudio == 0:
            meteoverif()

        elif cptAudio == 1:
            b = meteoverif()
            if b:
                try:
                    fusion()
                except Exception as e:
                    print("pas de fichier a fusionner")

            else:
                try:
                    os.remove("Meteo.wav")
                    os.rename("0.wav", "Meteo.wav")
                except:
                    os.rename("0.wav", "Meteo.wav")
    '''
