# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 09:47:19 2023

@author: deTRAZEGNIES
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import cv2
from numpy import linspace
from mpl_toolkits import mplot3d
from scipy import signal

# chemin vers l'image1, l'image2 est un blanc, et l'image est la différence

image1 = cv2.imread('C:/Users/image 1.jpg')
image2 = cv2.imread('C:/Users/image 2 blanc.jpg')
image = image2 - image1
fig = plt.figure(0)
plt.subplot(1, 1, 1)
# # Recadrer l'image
y = 360
x = 621
h = 480
w = 700
crop = image[y:y+h, x:x+w]

# Afficher image cropée
plt.title("Image cropée")
plt.imshow(crop)
plt.xticks([])  # suprimer les ticks de l'axe des x image mélange
plt.yticks([])  # suprimer les ticks de l'axe des y image mélange


# Conversion en format hsv

img_hsv = mpl.colors.rgb_to_hsv(crop/255)


# Definition des seuils pour le code couleur hsv

# deg (voir https://en.wikipedia.org/wiki/HSL_and_HSV#/media/File:Hsl-hsv_models.svg)
h_min, h_max = (50, 200)

h_min = h_min / 360

h_max = h_max / 360

s_min, s_max = (0, 1)  # rayon

v_min, v_max = (0, 1)  # hauteur

# Calcul du mask booleen

mask = (h_min <= img_hsv[:, :, 0]) & (img_hsv[:, :, 0] <= h_max) & (s_min <= img_hsv[:, :, 1]) & (
    img_hsv[:, :, 1] <= s_max) & (v_min <= img_hsv[:, :, 2]) & (img_hsv[:, :, 2] <= v_max)

mask3DPourHSV = np.stack((mask, mask, mask), axis=2)

# Filtrage de l'image hsv pour garder les pixels de fluorescine

img_hsv_filtree = np.where(mask3DPourHSV, img_hsv, 0)

img_rgb_filtree = mpl.colors.hsv_to_rgb(img_hsv_filtree)


# Proportion de pixel vert dans l'image filtree

N = img_hsv.shape[0] * img_hsv.shape[1]  # nombre de pixels dans l'image

E = np.float32(np.count_nonzero(img_hsv_filtree[:, :, 2])) / N * 100


# Tracé du résultat RVB en 3D
fig = plt.figure()
canal_vert = img_rgb_filtree[:, :, 1] * 71
prc_pixels_au_dessus_71 = (canal_vert>71).sum()/canal_vert.size*100
X, Y = np.linspace(0, 54, canal_vert.shape[1]), np.linspace(
    0, 26, canal_vert.shape[0])
X, Y = np.meshgrid(X, Y)
Z = np.ones(np.shape(X)) * 71
ax = plt.axes(projection='3d')  # Affichage en 3D
ax.plot_surface(X, Y, canal_vert, cmap=cm.coolwarm, linewidth=0)
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0)  # Tracé d'une surface
titre_graphe = ["Canal vert filtre ",str(round(prc_pixels_au_dessus_71)), '%'];
titre_graphe= ' '.join(titre_graphe)
# ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0)  # Tracé d'une surface
plt.title(titre_graphe)
ax.set_xlabel('Longueur')
ax.set_ylabel('Largeur')
ax.set_zlabel('Intensite en vert (Hauteur)')
# Creating Dataset
t = np.linspace(0, 1, 1000, endpoint = True)
ax.plot3D(t, signal.square(2 * np.pi * 5 * t))
# 360 Degree view
for angle in range(0, 180):
   ax.view_init(angle, 30)
   plt.draw()
   plt.pause(.001)
plt.show()


plt.tight_layout()


# Conversion en niveau de gris
img_gris_filtree = 0.2989 * img_rgb_filtree[:, :, 0] + 0.587 * \
    img_rgb_filtree[:, :, 1] + 0.114 * img_rgb_filtree[:, :, 2]
fig = plt.figure()
X, Y = np.linspace(0, 54, img_gris_filtree.shape[1]), np.linspace(
    0, 26, img_gris_filtree.shape[0])

X, Y = np.meshgrid(X, Y)
ax = plt.axes(projection='3d')  # Affichage en 3D
ax.plot_surface(Y, X, img_gris_filtree, linewidth=0)
plt.title("Img en niveau de gris filtre")
ax.set_xlabel('Longueur lame')
ax.set_ylabel('Largeur lame')
ax.set_zlabel('Intensite en gris (Hauteur)')
plt.tight_layout()

# dans PowerShell: "python'C:/Users/deTRAZEGNIES/Desktop/Projet IHC Infrasson/Code pyton spyder/Analyse hauteur ligne 3D HSV RVB.py"

Y = canal_vert[200, :] # Axe horizontal
#Y = canal_vert[:,340] # Axe verticale

X = np.arange(0, len(Y)).astype(float)
print(canal_vert[218][340])
print(len(img_gris_filtree))
fig = plt.figure(4)
plt.title("Profile hauteurs")
plt.scatter(X, Y)
plt.show()# Afficher
# 360 Degree view

# Pour l'exportation sur Excel, changer le nom "test.csv"
np.savetxt("21,6.csv", canal_vert, fmt='%d', delimiter=";") # (Nombres réels d)


