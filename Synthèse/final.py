#import le reste des doc
from pyautogui import keyDown
from assistant.jeanne import Jeanne
import radio
import stockage

import sys
import threading
from pynput import keyboard

keys_press = []

# Application Lancé par la radio au démarage ????
def lancer_assistant(commande):
    if commande == True:
        try:
            th_assistant = threading.Thread(target=Jeanne)
            th_assistant.start()
            print('lancer_assistant: [OK]')
        except:
            print('lancer_assistant: [echec]')
def lancer_radio(commande):
    if commande == True:
        try:
            th_assistant = threading.Thread(False)
            th_assistant.start()
            print('lancer_radio: [OK]')
        except:
            print('lancer_radio: [echec]')

def already_Press(k):
    global keys_press
    if k in keys_press:
        keys_press.remove(k)
        return True
    else:
        keys_press.append(k)
        return False

def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
   
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys
    if k == 'a':  # keys of interest
        if already_Press(k):
            lancer_assistant(False)
            print('Assistant stop: ' + k)
        else:
            print('Assistant start: ' + k)
            lancer_assistant(True)
       
    if k == 'r':  # keys of interest
        #th_radio = threading.Thread()
        #qth_radio.start()
        print('Radio start: ' + k)


#th_radio = threading.Thread()
#th_assistant = threading.Thread()




if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys
