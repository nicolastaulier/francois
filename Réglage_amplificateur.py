# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:53:20 2024

@author: deTRAZEGNIES
"""

import serial
import time
#import pytic
import winsound
import subprocess
import yaml
import initialisation

import datetime

def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))

def move(ser, value):  # Cote moteur
    """-*9
    code1 = b'\x69'
    ser.write(code1)
    code1 = b'\x11'
    ser.write(code1)

    code2 = b'\x68'
    ser.write(code2)
    code2 = b'\x12'
    ser.write(code2)
    """
    status = yaml.safe_load(ticcmd('-s', '--full'))
    position = status['Current position']

    new_target = value
    ticcmd('--exit-safe-start', '--position', str(new_target))

def Réglage_amplificateur(tps):
    print(f"Réglage amplificateur")
    return



def start_routine(instruction,ser):
    print(instruction["Réglage amplificateur"])
    if instruction["Réglage amplificateur"] == False:
        print("Effectuer la mesure sur les deux buses puis selectonner 'Réalisé'")
      
    #return 1

def run_reglage_cote_moteur(ser):
    ticcmd("--max-speed",'5000000')
    position = -4480
    print(position)
    move(ser,position)
    i = 0
    x = 0
    while x != position:
        i += 1
        status = yaml.safe_load(ticcmd('-s', '--full'))
        x = status['Current position']
        if i == 1000:
            break
    t2 = time.time()
    initialisation.allumer_relais1(ser)
    while (time.time() - t2) < 30.1:
         continue
    initialisation.eteindre_relais1(ser) 
    
def run_reglage_cote_lame(ser):  
    ticcmd("--max-speed",'5000000')
    position = -3860
    print(position)
    move(ser,position)
    i = 0
    x = 0
    while x != position:
        i += 1
        status = yaml.safe_load(ticcmd('-s', '--full'))
        x = status['Current position']
        if i == 1000:
            break
    t2 =time.time()
    initialisation.allumer_relais1(ser)
    while (time.time() - t2) < 30.1:
         continue
    initialisation.eteindre_relais1(ser) 
    return 0