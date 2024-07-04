# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:56:52 2024

@author: deTRAZEGNIES
"""

import serial
import time
#import pytic
#import winsound
import subprocess
import yaml
import datetime
import initialisation


def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))

def prechauffage(tps):
    print(f"Préchauffage pendant {tps} sec.")
    return

def nébulisation(mode):
    print(f"Nébulisation avec mode : {mode}")
    return

def melange(mode, pulse):
    print(f"Mélange avec mode : {mode}")
    if pulse:
        print("Avec pulse")
    return

def incubation(tps):
    print(f"Incubation pendant {tps} sec.")
    return



def nebulisation(instruction,ser,position_N,position_N1,position_N2,vitesse_deplacement):
    if instruction["étalonnage"] == False:
        print("ETALONNAGE A FAIRE AVANT DE RUN")
        #return 1
    prechauffage(instruction["Temps_préchauffage"])
    
    # Choix nébulisation
    if instruction["Nébulisation"] == "Sans_nébu":
        pass
    elif instruction["Nébulisation"] == 'Nebu_Fixe':
        status = yaml.safe_load(ticcmd('-s', '--full'))
        x = status['Current position']
        print('position_N',position_N)
        ticcmd("--max-speed",vitesse_deplacement)
        initialisation.move(ser,position_N)
        i = 0
        while x != position_N:
            status = yaml.safe_load(ticcmd('-s', '--full'))
            x = status['Current position']
            i += 1
            if i == 1000:
                break
        initialisation.allumer_relais2(ser)
        t0 = time.time()
        while (time.time() - t0) < 5.1:
            continue
        initialisation.eteindre_relais2(ser)
    elif instruction["Nébulisation"] == 'Mobile Vitesse_ nébu  1':
        vitesse_nebu_1 = '700000'   # A CHANGER !!!!!!
        ticcmd("--max-speed",vitesse_deplacement)
        x = 0
        initialisation.move(ser,position_N1)
        while x != position_N1:
            status = yaml.safe_load(ticcmd('-s', '--full'))
            x = status['Current position']
        t0 = time.time()
        initialisation.allumer_relais2(ser)
        ticcmd("--max-speed",vitesse_nebu_1)
        while (time.time() - t0) < 5.1:
            initialisation.move(ser,position_N2)
            while x != position_N2:
                status = yaml.safe_load(ticcmd('-s', '--full'))
                x = status['Current position']
            initialisation.move(ser,position_N1)
            while x != position_N1:
                status = yaml.safe_load(ticcmd('-s', '--full'))
                x = status['Current position']
        initialisation.eteindre_relais2(ser)
    elif instruction["Nébulisation"] == 'Mobile Vitesse_nebu 2':    
        vitesse_nebu_2 = '1000000'
        ticcmd("--max-speed",vitesse_deplacement)
        x = 0
        initialisation.move(ser,position_N1)
        while x != position_N1:
             status = yaml.safe_load(ticcmd('-s', '--full'))
             x = status['Current position']
        x = 0
        t0 = time.time()
        initialisation.allumer_relais2(ser)
        ticcmd("--max-speed",vitesse_nebu_2)
        while (time.time() - t0)< 5.1:
            initialisation.move(ser,position_N2)
            while x != position_N2:
                status = yaml.safe_load(ticcmd('-s', '--full'))
                x = status['Current position']
            initialisation.move(ser,position_N1)
            while x != position_N1:
                status = yaml.safe_load(ticcmd('-s', '--full'))
                x = status['Current position']
        initialisation.eteindre_relais2(ser)
    print('nébulisation terminée')
    return 1

# Choix mélange
def Mélange(instruction,ser,position_Nm,position_Nm1,position_Nm2,position_veille,vitesse_deplacement):
    print(instruction["Mélange"])
    if instruction["Mélange"] == "Sans":
        pass
    
    elif instruction["Mélange"] == 'Fixe':
        status = yaml.safe_load(ticcmd('-s', '--full'))
        x = status['Current position']
        ticcmd("--max-speed",vitesse_deplacement)
        initialisation.move(ser,position_Nm)
        print('position_Nm',position_Nm)
        x = 0
        i = 0
        while x != position_Nm:
            i += 1
            status = yaml.safe_load(ticcmd('-s', '--full'))
            x = status['Current position']
            if i == 1000:
                break
        temps_incubation = float(instruction["temps_incubation"])*60
        t1 = time.time()
        try:
            pulse = bool(instruction["pulse"])
        except:
            pulse = False
        if pulse == True:
            while (time.time() - t1) <  temps_incubation:
                t2 =time.time()
                initialisation.allumer_relais1(ser)
                while (time.time() - t2) < 60.1:
                    continue
                initialisation.eteindre_relais1(ser)
                t0 = time.time()
                while (time.time() - t0) < 5.1:
                   continue
        elif pulse == False:
           initialisation.allumer_relais1(ser)
           while (time.time() - t1) <  temps_incubation:
               continue
           initialisation.eteindre_relais1(ser)
            
    elif instruction["Mélange"] == 'Mobile Vitesse 1':
         ticcmd("--max-speed",vitesse_deplacement)
         vitesse_mel_1 = '200000'
         x = 0
         i = 0 
         initialisation.move(ser,position_Nm1)
         while x != position_Nm1:
             status = yaml.safe_load(ticcmd('-s', '--full'))
             x = status['Current position']
             i += 1
             if i == 1000:
                 break
         ticcmd("--max-speed",vitesse_mel_1)
         initialisation.allumer_relais1(ser)
         ticcmd("--max-speed",'200000')
         initialisation.move(ser,position_Nm2)
         while x != position_Nm2:
             status = yaml.safe_load(ticcmd('-s', '--full'))
             x = status['Current position']
         initialisation.move(ser,position_Nm1)
         while x != position_Nm1:
             status = yaml.safe_load(ticcmd('-s', '--full'))
             x = status['Current position']
             initialisation.eteindre_relais1(ser)
    elif instruction["Mélange"] == 'Mobile Vitesse 2':    
         ticcmd("--max-speed",vitesse_deplacement)
         vitesse_mel_2 = '300000'
         x = 0
         i = 0
         initialisation.move(ser,position_Nm1)
         while x != position_Nm1:
              status = yaml.safe_load(ticcmd('-s', '--full'))
              x = status['Current position']
              i += 1
              if i == 1000:
                  break
         ticcmd("--max-speed",vitesse_mel_2)
         t0 = time.time()
         while (time.time() - t0) < 5.1:
              initialisation.allumer_relais1(ser)
              initialisation.move(ser,position_Nm2)
              while x != position_Nm2:
                  status = yaml.safe_load(ticcmd('-s', '--full'))
                  x = status['Current position']
              initialisation.move(ser,position_Nm1)
              while x != position_Nm1:
                  status = yaml.safe_load(ticcmd('-s', '--full'))
                  x = status['Current position']
                  initialisation.eteindre_relais1(ser)
    
    ticcmd("--max-speed",vitesse_deplacement)              
    initialisation.move(ser,position_veille)
    print('position_veille',position_veille)
    print('terminé')