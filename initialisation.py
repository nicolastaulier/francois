# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 10:06:03 2024

@author: deTRAZEGNIES
"""

import serial
import time
#import pytic
import winsound
import subprocess
import yaml

import datetime



# Définition des fonctions de contrôle des relais
# Énvoi l'adresse exadécimal

def allumer_relais1(ser):  # Mélangeur
    ser.write(b'\x6C')
    return 1


def allumer_relais2(ser):  # Nébulisation
    ser.write(b'\x6B')
    return 1


def allumer_relais3(ser):  # Chauffage lame
    ser.write(b'\x6A')
    return 1


def allumer_relais4(ser):  # Contact coté moteur
    ser.write(b'\x69')
    return 1


def allumer_relais5(ser):  # Contact coté support lame
    ser.write(b'\x68')
    return 1


def eteindre_relais1(ser):
    ser.write(b'\x76')
    return 1


def eteindre_relais2(ser):
    ser.write(b'\x75')
    return 1


def eteindre_relais3(ser):
    ser.write(b'\x74')
    return 1


def eteindre_relais4(ser):
    ser.write(b'\x73')
    return


def eteindre_relais5(ser):
    ser.write(b'\x72')
    return 1


def soundend(sound):
    flags = winsound.SND_FILENAME
    winsound.PlaySound(sound, flags)


def attendre5():
    time.sleep(2)
    return 1


def attendre10():
    time.sleep(2)
    return 1

def move(ser):
    move(ser,100)
    return
###############################################################################
# LECTURE DES CONTACTS


def fin_de_course1(ser):  # Cote moteur
    code = b'\x69'
    ser.write(code)
    code = b'\x11'
    ser.write(code)
    res = ser.read(size=2)  # Lecture de l'état (res) xff ou x00
    if res == b'\x00':
        print("Fin de course 1 activée")
        code = b'\x73'
        ser.write(code)
    return 1


def fin_de_course2(ser):  # coté support lame
    code = b'\x68'
    ser.write(code)
    code = b'\x12'
    ser.write(code)
    res = ser.read(size=2)
    if res == b'\x00':
        print("Fin de course 2 activée")
        code = b'\x72'
        ser.write(code)
    return 1


def move(ser, value):  # Cote moteur
    ticcmd('--exit-safe-start', '--position', str(value))
   


###############################################################################
# COMMANDE MOTEUR

# Uses ticcmd to send and receive data from the Tic over USB.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB"
# in order to set the target position over USB.


def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))



def etalonnage(ser):

   now = datetime.datetime.now()
   code = b'\x11'
   ser.write(code) 
   x11 = ser.read(size=2)
      
   code = b'\x73'
   ser.write(code)
   
   ticcmd("--max-speed",'190000')
   
   position = 10000
   move(ser,position)
   x11 = b'\xFF'
   code = b'\x11'
   i = 0
   ser.write(code) 
   x11 = ser.read(size=2)
  
   if x11 == b'\x00':
       ticcmd('--halt-and-set-position','0')
   elif x11 == b'\xff':
       while x11 != b'\x00':
           ser.write(code) 
           x11 = ser.read(size=2)
           print(x11)
           i+=1 
           if i == 500:
               break
       else:
           ticcmd('--halt-and-set-position','0')
   position = -10000
   move(ser,position)
   x12 = b'\xFF'
   code = b'\x12'
   i = 0
   while x12 != b'\x00':
       ser.write(code) 
       x12 = ser.read(size=2)
       print(x12)
       i+=1 
       if i == 500:
           break
   else:
       ticcmd('--halt-and-hold')  
       status = yaml.safe_load(ticcmd('-s', '--full'))
       position_x12 = status['Current position'] 
       print(position_x12)        
  
   
   ticcmd("--status")
   ser.close()
   

def findposition(ser):
   ticcmd('--energize')
   code = b'\x11'
   ser.write(code) 
   x11 = ser.read(size=2)
      
   code = b'\x73'
   ser.write(code)
   ticcmd("--max-speed",'190000')
   """
   position = -10000
   move(ser,position)
   x12 = b'\xFF'
   code = b'\x12'
   i = 0
   while x12 != b'\x00':
       ser.write(code) 
       x12 = ser.read(size=2)
       print(x12)
       i+=1 
       if i == 500:
           break
   else:
       ticcmd('--halt-and-hold')  
       status = yaml.safe_load(ticcmd('-s', '--full'))
       position_x12 = status['Current position'] 
       print(position_x12)   
   """    
   position = 10000
   move(ser,position)
   x11 = b'\xFF'
   code = b'\x11'
   i = 0
   ser.write(code) 
   x11 = ser.read(size=2)
   if x11 == b'\x00':
       ticcmd('--halt-and-hold')
   elif x11 == b'\xff':
       while x11 != b'\x00':
           ser.write(code) 
           x11 = ser.read(size=2)
           print(x11)
           i+=1 
           if i == 500:
               break
       else:
           ticcmd('--halt-and-hold')
           status = yaml.safe_load(ticcmd('-s', '--full'))
           position_x11 = status['Current position'] 
        
   #ticcmd("--status")
   