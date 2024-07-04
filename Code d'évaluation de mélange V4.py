

#Created on Tue Jul 12 11:08:58 2022

#@author: deTRAZEGNIES


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image


# """ Parametres a régler """
#chemin vers l'image
chemin = r'C:/Users/photo à analyser.png'

# filtrer les pixels qui appartiennent pas a la flurecine
min_tresh = np.float32(0.0)  # 30


#seuil haut et bas pour enlever les pixels qu'on veut pas garder
max_tresh = np.float32(1.0)  #200

# lecture de l'image
img = image.imread(chemin)
fig = plt.figure()


img_green = np.copy(img[:,:,1])
img_red = np.copy(img[:,:,0])

#on soustrait à l'image canal vert le canal rouge = enelver tout ce qui est blanc 
# img_green = img_green - img_red

#on utilse les seuils
# img_green = np.logical_and(img_green <max_tresh, img_green>min_tresh) * img_green
img_green = np.where(np.logical_and(min_tresh <= img_green, img_green <= max_tresh), img_green, 0);

# #affichage image originale
plt.subplot(3,1,1)

# #titre image originale
plt.title ("Image brut")
plt.imshow(img)
plt.xlabel("Pourcentage de mélange")
plt.xticks([]) # suprimer les ticks de l'axe des x image mélange
plt.yticks([]) # suprimer les ticks de l'axe des y image mélange

# #affichage image originale
plt.subplot(3,1,2)


# #nombre de pixels dans l'image
N = img_green.shape[0] * img_green.shape[1]

# #proportion de pixels vert
E=int((np.count_nonzero(img_green)/N * 100)) 
print('E\%')


plt.imshow(np.stack([np.zeros_like(img_green), img_green, np.zeros_like(img_green)], axis = 2))
plt.subplots_adjust(hspace=0.5)

# #afficher pourcentage arrondi sous image
plt.xlabel(str(round(E))+'%') #arrondie et ajout du symbole %
plt.xticks([]) # suprimer les ticks de l'axe des x image pourcentage
plt.yticks([]) # suprimer les ticks de l'axe des y image pourcentage

histogramme, niv_green = np.histogram(img_green, bins=256, range=(0, 1))
print(niv_green)

# # Figure
plt.subplot(3,1,3)
plt.title("Histogramme de valeurs de pixels en niveau de gris")
plt.xlabel("Niveau de gris")
plt.ylabel("Nbre de pixels")

plt.plot(niv_green[:-1], histogramme)
plt.xlim(0,1)

plt.show()
