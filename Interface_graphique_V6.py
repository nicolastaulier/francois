"""
Created on Tue Feb 20 15:03:58 2024

@author: deTRAZEGNIES
"""

from tkinter import *
from tkinter import Tk, StringVar
from tkinter.ttk import Combobox
import os
from tkinter import Tk, Button, Entry
import serial 
from Démarer_routine import nebulisation, Mélange
from Réglage_amplificateur import run_reglage_cote_lame, run_reglage_cote_moteur

import initialisation



ser = serial.Serial('COM6', 9600, timeout=1,parity=serial.PARITY_EVEN, rtscts=1)
 
def allumer_relais3():  # Chauffage lame
    ser.write(b'\x6A')
    return 
allumer_relais3()                      

print(ser.name)

# Première boite pour le titre avec arrière plan (bg) gris, instance frame se positionne dans la fenètre
global temps
instruction = {"étalonnage" : False}

fenetre=Tk()
fenetre.title("Automate IHC") 
fenetre.iconbitmap("C:/Users/utilisateur/Documents/Python Scripts/IMG_3469.ico")

fenetre.minsize(400, 500)
fenetre.maxsize(500, 700)

# Première boite pour le titre avec arrière plan (bg) gris, instance frame se positionne dans la fenètre
#expand=TRUE centre la boite
boite1=Frame(fenetre, bg="grey")
boite1.pack(expand=TRUE)



# Titre du haut bg=couleur en hexadecimal
titre = Label(boite1, text="INTERFACE SCENARIO OPTIMISATION",fg="white", bg="#7F7D9C", wraplength=500)
titre .pack(fill=X)


titre = Label(boite1, text="Réglage amplificateur")
titre .pack(fill=X) 
variable_Réglage_amplificateur = StringVar()
# def get_choice_Réglage_amplificateur(event):
    
#     instruction["Réglage_amplificateur"] = variable_Réglage_amplificateur.get()
#     print(variable_Réglage_amplificateur.get())  
# variable_Réglage_amplificateur.set('Réglage_amplificateur')
# choices = {'Côté_moteur': 'Côté_moteur', 'Côté_lame' : 'Côté_lame' , 'Réalisé' : 'Réalisé'}  
# champ = Combobox(boite1, values=list(choices.keys()), textvariable=variable_Réglage_amplificateur, state='readonly')
# champ.pack(fill=X)
# tmp = champ.bind('<<ComboboxSelected>>', get_choice_Réglage_amplificateur)



def reglage_cote_moteur_clicked():
    run_reglage_cote_moteur(ser)
    return

def reglage_cote_lame_clicked():
    run_reglage_cote_lame(ser)
    return

# Etalonnage
def Etalonnage_button_clicked():
    initialisation.etalonnage(ser)
    initialisation.findposition(ser)

    print("Etalonnage en cours patentez")
    text.set("Etalonage en cours") 
    instruction["étalonnage"] = True


# Deuxième boite avec bg gris qui contien les widgets
boite2=Frame(fenetre, bg="grey")
boite2.pack(expand=TRUE)
bouton = Button(boite2, text="Coté moteur", bg="grey", command=reglage_cote_moteur_clicked)
bouton.pack(fill=X)
titre.pack(fill=X) 


# Deuxième boite avec bg gris qui contien les widgets
boite3=Frame(fenetre, bg="grey")
boite3.pack(expand=TRUE)
bouton = Button(boite2, text="Coté lame", bg="grey", command=reglage_cote_lame_clicked)
bouton.pack(fill=X)
titre.pack(fill=X) 


# Deuxième boite avec bg gris qui contien les widgets
boite=Frame(fenetre, bg="grey")
boite.pack(expand=TRUE)
text = StringVar()
text.set("Etalonage à faire")
titre = Label(boite, textvariable=text)

initialisation.ticcmd('--energize')

# Créez un champ de texte (Entry)

bouton = Button(boite, text="Etalonnage", bg="grey", command=Etalonnage_button_clicked)
bouton.pack(fill=X)

titre.pack(fill=X) 
    


def get_choice(event):
    os.startfile(choices[event.widget.get()])
    
titre = Label(boite, text="Temps préchauffage à 36°C (secondes)")
titre .pack(fill=X) 
variable_Temps_préchauffage = StringVar()  

def get_choice_Temps_préchauffage(event):
    val_chaine = variable_Temps_préchauffage.get()
    val_entier = int(val_chaine)
    tempsP = variable_Temps_préchauffage.get()
    instruction["Temps_préchauffage"] = tempsP
    print(tempsP)
#printTemps_préchauffage
#   print('ok temps prechauffage',variable_prechauffage.get()) 
variable_Temps_préchauffage.set('Temps_préchauffage')       
choices = {'1 ': '1P', '2 ': '2P', '3 ': '3P', '4 ': '4P', '5': '5P'}
champ = Combobox(boite, values=list(choices.keys()), textvariable=variable_Temps_préchauffage, state='readonly')
champ.pack(fill=X)
tmp = champ.bind('<<ComboboxSelected>>', get_choice_Temps_préchauffage) 

    

titre = Label(boite, text="Nébulisation")
titre .pack(fill=X) 
variable_Nebulisation = StringVar()

def get_choice_Nebulisation(event):
    instruction["Nébulisation"] = variable_Nebulisation.get()
    print(variable_Nebulisation.get())  
    
variable_Nebulisation.set('Nebulisation')
choices = {'Sans_nébu': 'Sans_nébu', 'Nebu_Fixe': 'Nebu_Fixe', 'Mobile Vitesse_ nébu  1': 'Mobile_nebu 1', 'Mobile Vitesse_nebu 2': 'Mobile_NEBU 2'}  
champ = Combobox(boite, values=list(choices.keys()), textvariable=variable_Nebulisation, state='readonly')
champ.pack(fill=X)
tmp = champ.bind('<<ComboboxSelected>>', get_choice_Nebulisation)

# def Selection(EtatCheckButton, resultat):
#     selection = []
#     for i in range (len(resultat)):
#         if EtatCheckButton[i].get() == True :
#             selection.append(resultat [i])
#     showinfo(title=None, message=selection)
    
    
titre = Label(boite, text="Mélange")
titre .pack(fill=X)    
variable_Mélange = StringVar() 
def get_choice_Mélange(event):
    
    instruction["Mélange"] = variable_Mélange.get()
    print(variable_Mélange.get())  
variable_Mélange.set('Mélange')     
choices = {'Sans': 'SansM', 'Fixe': 'Fixe', 'Mobile Vitesse 1': 'MobileMV1', 'Mobile Vitesse 2': 'MobileMV2'}   
champ = Combobox(boite, values=list(choices.keys()), textvariable=variable_Mélange, state='readonly')
champ.pack(fill=X)
champ.bind('<<ComboboxSelected>>', get_choice_Mélange)


# check est une instance de la classe chechbutton
check_1 = IntVar()

def check1Clicked():
    instruction["pulse"] = check_1.get()
    if check_1.get() :
        print('Checkbox 1 selected')
    else :
        print('Checkbox 1 unselected')

check=Checkbutton(boite,text="Pulse", variable = check_1, command=check1Clicked)
check.pack(fill=X)

def Selection(EtatCheckButton, resultat):
    selection = []
    for i in range (len(resultat)):
        if EtatCheckButton[i].get() == True :
            selection.append(resultat [i])
    showinfo(title=None, message=selection)
      

    
titre = Label(boite, text="Temps incubation (minutes)")
titre .pack(fill=X)
variable_Temps_incubation = StringVar()

def get_choice_Temps_incubation(event):
    val_chaine = variable_Temps_incubation.get()
    val_entier = int(val_chaine)
    temps = variable_Temps_incubation.get()
    instruction["temps_incubation"] = temps
    print(temps)

variable_Temps_incubation.set('Temps_incubation')     
choices = {'1' : '60I' , '2' :' 120I','4': '240I', '6 ': '360I', '8 ': '480I', '16': '960I' , '32 ': '1920I'}
champ = Combobox(boite, values=list(choices.keys()), textvariable=variable_Temps_incubation, state='readonly')
champ.pack(fill=X)
tmp = champ.bind('<<ComboboxSelected>>', get_choice_Temps_incubation)  
           
titre = Label(boite, text="Commande")
titre .pack(fill=X)

def eteindre_relais3():
    ser.write(b'\x74')

def run_button_clicked():
    position_N = -2973
    position_N1 = -2625
    position_N2 = -3322
    position_Nm = -1647
    position_Nm1 = -1545
    position_Nm2 = -1749
    position_veille = -4500
    vitesse_deplacement = '5000000'
    print("Run button triggered")
    print(instruction)

    nebulisation(instruction,ser,position_N,position_N1,position_N2,vitesse_deplacement)
    Mélange(instruction,ser,position_Nm,position_Nm1,position_Nm2,position_veille,vitesse_deplacement)

def stop_button_clicked(): 
    initialisation.ticcmd('--deenergize') 
    eteindre_relais3()
    print("Stop button triggered")  
    ser.close()   
    boite1.destroy()
    boite.destroy()
    fenetre.destroy() 


bouton=Button(boite,text="RUN", bg="GREEN", command=run_button_clicked)
bouton.pack(fill=X)
champ.pack(fill=X)


bouton=Button(boite,text="QUIT", bg="RED", command=stop_button_clicked)
bouton.pack(fill=X)
champ.pack(fill=X)

# Boucle mainloop
mainloop()
#root.mainloop()