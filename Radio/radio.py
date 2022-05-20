#!/usr/bin/python3
#Code de base obtenue sur "https://www.raspberrypi.org/forums/viewtopic.php?t=53680" par l'utilisateur: LinuxCircle et récupérer sur piddlerintheroot

#Permet d'interagir avec la carte mère et le module tea5767 pour récupérer et utiliser les informations FM
import smbus as smbus 
import subprocess
#Permet d'intergair avec le terminal
import curses
import curses.textpad
#Ajoute la notion de temps (utile pour endormir le programme)
import time

i2c = smbus.SMBus(1) 
i2c_address = 0x60

def init_radio(address):
    """Initialisation du matériel"""
    i2c.write_quick(address)
    time.sleep(0.1)


def set_freq(address, freq):
    """Definir la fréquence de la radio"""
    freq14bit = int (4 * (freq * 1000000 + 225000) / 32768) # Distribution de fréquence sur deux octets (selon la fiche technique)
    freqH = freq14bit>>8 #int (freq14bit / 256)
    freqL = freq14bit & 0xFF

    data = [0 for i in range(4)] # Descriptions des bits individuels dans un octet.
    init = freqH # freqH # 1.bajt (bit muet; Frequance H)  // Rendre muet sur le 0x80
    data[0] = freqL # 2.bajt (frequance L)
    #Le nombre hexadecimal correspond au paramètre que l'on veut modifier
    #
    data[1] = 0xB0 #0b10110000 # 3.bajt (SUD; SSL1, SSL2; HLSI, MS, MR, ML; SWP1)
    #       SUD     SSL1    SSL2    HLSI    MS      MR      ML      SWP1
    #Bit    7       6       5       4       3       2       1       0
    #7 Search up/down  6 Search stop Level   5 High/low Side Injection     4 Mono to stereo  3 Mute Right  2 Mute Right  1 Mute Left   0 Software programmable port 1
    #
    data[2] = 0x10 #0b00010000 # 4.bajt (SWP2; STBY, BL; XTAL; smut; HCC, SNC, SI)
    #       SWP2    STBY    BL      XTAL    SMUTE   HCC     SNC     SI
    #Bit    7       6       5       4       3       2       1       0
    #Descr  7 Software programmable port2  6 Standby   5 Band Limits     4 Clock frequency  3 Soft Mute  2 High Cut Control  1 Stereo Noise Cancelling   0 Search indicator
    #
    data[3] = 0x00 #0b00000000 # 5.bajt (PLLREF; DTC; 0; 0; 0; 0; 0; 0)
    #       PLLREF  DTC     0        0       0       0       0       0
    #Bit    7       6       5       4       3       2       1       0
    #Descr  7 PLLREF  6 DTC
    #
    try:
      i2c.write_i2c_block_data (address, init, data) # Restitue la nouvelle fréquence au circuit TEA5767
      print("Frequence mit sur: " + str(freq)+"/r")
    except IOError:
      subprocess.call(['i2cdetect', '-y', '1'])


def mute(address):
    """"rendre radio muette"""
    freq14bit = int(4 * (0 * 1000000 + 225000) / 32768)
    freqL = freq14bit & 0xFF
    data = [0 for i in range(4)]
    init = 0x80
    data[0] = freqL
    data[1] = 0xB0
    data[2] = 0x10
    data[3] = 0x00
    try:
        i2c.write_i2c_block_data(address, init, data)
        print("Radio muette"+"/r")
    except IOError:
        subprocess.call(['i2cdetect', '-y', '1'])


if __name__ == '__main__':
    init_radio(i2c_address)
    frequency = 102.6 # Fréquence de départ
    # Le terminal utilise une loupe infini pour fonctionner en continue
    stdscr = curses.initscr()
    curses.noecho()
    try:
        while True:
            c = stdscr.getch()
            #Modification de la fréquence avec une touche#
            if c == ord('1'): # Mets France Bleu 102.6
                frequency = 102.6
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('2'): # Mets NRJ 101.4
                frequency = 101.4
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('3'): # Mets RTL 105.0
                frequency = 105.0
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('4'): # Mets FUN RADIO 96.3
                frequency = 96.3
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('5'): # Mets TENDANCE OUEST 100.2
                frequency = 100.2
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('w'): # incremente de 1 la fréquence
                frequency += 1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('s'): # decremente de 1 la fréquence
                frequency -= 1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('e'): # incremente de 0.1 la fréquence
                frequency += 0.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('d'): # decremente de 0.1 la fréquence
                frequency -= 0.1
                set_freq(i2c_address, frequency)
                time.sleep(1)
            #Permet de couper/remettre/quitter la radio
            elif c == ord('m'): # mute
                mute(i2c_address)
                time.sleep(1)
            elif c == ord('u'): # unmute
                set_freq(i2c_address, frequency)
                time.sleep(1)
            elif c == ord('q'): # quitter le script
                mute(i2c_address)
                curses.endwin()
                break
    except KeyboardInterrupt:
        mute(i2c_address)
        curses.endwin()
