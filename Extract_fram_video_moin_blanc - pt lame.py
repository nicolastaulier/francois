# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 12:05:13 2023

@author: deTRAZEGNIES
"""

import cv2
import os

#%% pas toucher
def extract_frames(video_path, output_folder):
    # Ouvrez le fichier vidéo
    video = cv2.VideoCapture(video_path)
    
    # Lire la première image
    success, frame = video.read()
    count = 0
    print('LONGUEUR',len(frame))
    
    # Itérer à travers les images jusqu’à la fin de la vidéo
    while success:
        
        # Soustraction image blanc à image mélange itéré
        blanc= cv2.imread('C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/PIV/video/WIN_20230724_16_00_55_Pro.jpg') 
        subtracted = cv2.subtract(frame, blanc)
        
        #print(subtracted)
        
        # Enregistrer l’image actuelle en tant qu’image PNG
        cv2.imwrite(f"{output_folder}/frame{count:05d}.png", subtracted)

        # Lire l’image suivante
        success, frame = video.read()
        count += 1

    # Libérer l’objet vidéo
    video.release()


# %% Toucher ok
# Indiquez le chemin d’accès au fichier vidéo MP4 et au dossier de sortie
global_path = "C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/PIV/"
path = global_path + "video/"
path_save =  global_path + "data/"
video_name = "WIN_20230724_16_10_29_Pro.mp4"


#%% pas toucher
video_path = path + video_name
output_folder = path_save + video_name.replace(".mp4", "/")

os.mkdir(output_folder)

# Appelez la fonction pour extraire les images
extract_frames(video_path, output_folder)