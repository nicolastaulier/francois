# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 14:13:19 2022

@author: deTRAZEGNIES
"""


#Created on Tue Jul 12 11:08:58 2022

#@author: deTRAZEGNIES 

import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

# """ Parametres a régler """

#chemin vers l'image

chemin = r'C:/Users/Image à analyser.png'

# lecture de l'image

img = mpl.image.imread(chemin)

# affichage image originale

fig = plt.figure()

plt.subplot(3,1,1)

plt.title ("Image brute")

plt.imshow(img)

plt.xticks([]) # suprimer les ticks de l'axe des x image mélange

plt.yticks([]) # suprimer les ticks de l'axe des y image mélange

# Extraction des canaux de couleurs
img_red = np.copy(img[:,:,0])

img_green = np.copy(img[:,:,1])

img_blue = np.copy(img[:,:,2])

# Seuils sur le canal vert pour les pixels de fluorescine 

min_tresh, max_tresh = np.float32(0.0), np.float32(1.0)

# Conversion en format hsv

img_hsv = mpl.colors.rgb_to_hsv(img / 255) # Chaque canal est compris dans [0, 1]

# Definition des seuils pour le code couleur hsv

h_min, h_max = (60, 190) # deg (voir https://en.wikipedia.org/wiki/HSL_and_HSV#/media/File:Hsl-hsv_models.svg)

h_min = h_min / 360

h_max = h_max / 360

s_min, s_max = (0, 1) # rayon

v_min, v_max = (0.1, 0.9) # hauteur

# Calcul du mask booleen

mask = np.logical_and(h_min < img_hsv[:,:,0], img_hsv[:,:,0] < h_max) # Creation du masque pour le canal Hue

mask = np.logical_and(mask, s_min < img_hsv[:,:,1], img_hsv[:,:,1] < s_max) # Masque avec le canal de Saturation

mask = np.logical_and(mask, v_min < img_hsv[:,:,2], img_hsv[:,:,2] < v_max) # Masque avec le canal de Value

mask3DPourHSV = np.stack((mask, mask, mask), axis = 2)

# Filtrage de l'image hsv pour garder les pixels de fluorescine

img_hsv_filtree = np.where(mask3DPourHSV, img_hsv, 0)

img_rgb_filtree = mpl.colors.hsv_to_rgb(img_hsv_filtree)

# Proportion de pixel vert dans l'image filtree

N = img_hsv.shape[0] * img_hsv.shape[1] #nombre de pixels dans l'image

E = np.float32(np.count_nonzero(img_hsv_filtree[:,:,2])) / N * 100

# Affichage de l'image filtree

plt.subplot(3,1,2)

plt.imshow(img_rgb_filtree)

plt.title("Pourcentage de mélange " + str(round(E))+'%')

plt.subplots_adjust(hspace=0.5)

plt.xticks([]) # suprimer les ticks de l'axe des x image pourcentage

plt.yticks([]) # suprimer les ticks de l'axe des y image pourcentage

# Calcul de la repartition de l'intensite verte
img_H_filtree = img_hsv_filtree[:,:,1]
histogramme, niv_green = np.histogram(img_hsv_filtree[:,:,0]) #, bins=255, range=(0, 1)

# Affichage de l'histogramme

plt.subplot(3,1,3)

plt.plot(niv_green[:-1], histogramme)

plt.title("Histogramme de valeurs de pixels en niveau d'intensite")

plt.xlabel("Intensite [0; 1]")

plt.ylabel("Nb de pixels")

# plt.xlim(0,1)

plt.show()