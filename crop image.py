# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 18:12:07 2023

@author: deTRAZEGNIES
"""



from PIL import Image
 
# Ouvre une image en mode RVB
chemin = Image.open(r"C:/Users/deTRAZEGNIES/Desktop/test.png")
 
# Taille de l'image en pixels (taille de l'image originale)
width, height = chemin.size
 
# Réglage des points pour l'image recadrée
left = 200 #gauche
top = height / 6 #haut
right = 1215 #droite
bottom = 7 * height / 12 #bas
 
# Image recadrée de la dimension ci-dessus
# (Cela ne changera pas l'image d'origine)
img = chemin.crop((left, top, right, bottom))
 
# Affiche l'image dans la visionneuse d'images
img.show()



