# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:51:43 2023

@author: icv-leite
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


#%% Pas Toucher


def downsample_image(image, scale_percent):
    # Determine the new dimensions based on the scale percent
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)

    # Resize the image using bilinear interpolation
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    return resized_image

def apply_clahe(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)

    return clahe_img


def estimate_optical_flow(prev_frame, curr_frame, prev_flow):
    # Convert frames to grayscale
    prev_gray = apply_clahe(prev_frame)
    curr_gray = apply_clahe(curr_frame)

    # Calculate optical flow using Lucas-Kanade method
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, prev_flow, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Compute magnitude and angle of flow vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    return flow, magnitude, angle

def plot_optical_flow_vectors(image, flow, magnitude, angle, stride=24,coef = 4,save_path=None):
    # Create a meshgrid of coordinates
    y, x = np.mgrid[0:image.shape[0]:stride, 0:image.shape[1]:stride]

    # Extract flow vectors at specified coordinates
    flow_vectors = flow[y, x]
    magnitude_vectors = magnitude[y, x]

    # Filter out zero-valued flow vectors
    non_zero_indices = magnitude_vectors > 0
    flow_vectors = flow_vectors[non_zero_indices]

    # Extract x and y components of flow vectors

    flow_x = flow_vectors[..., 0] * coef
    flow_y = flow_vectors[..., 1] * coef

    # Create a plot with overlaid vector arrows
    plt.figure(figsize=(20,15)) # Taille 20 pouces par 15 pouces
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.quiver(x[non_zero_indices], y[non_zero_indices], flow_x, flow_y,
               color='green', angles='xy', scale_units='xy', scale=1)
    plt.plot([110,150], [50,50], 'w-', linewidth = 5.0) # Ajouter une toise de 100 pixels en haut à gauche
    plt.text(150, 50, ' 1 mm', color = 'white', fontsize ='x-large', fontweight ='bold') # Ecrir "1 mm" en gras, à coté de la toise
    plt.axis('off') # Retirer les ticks des axes x et y
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
        
      
    
    plt.show()
    

#%% Toucher ok
# Provide the path to the folder containing the frames
global_path = "C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/PIV/"

frames_folder = "WIN_20230724_16_10_29_Pro" # nom dossier image

save = True  # True = sauvegarder , False = ne rien faire

version = "_zoom_120" # nom specific pour version

coef = 4 # coeficient de taille des vecteur (taille vecteur * coef)

zoom = 120
#%% Pas Toucher

path = global_path + "data/" # chemin dossier image
path_save =  global_path +"resultat/" # chemin dossier image

if save:
    save_path = path_save+frames_folder+"_etude"+version
    os.mkdir(save_path)

# Assume you have the output of the first frame analysis stored in prev_output
prev_flow = None

# Iterate over the frames in the folder
frame_count = 0
skip_image = 5 # Une tous les 5 images
while True:
    # Construct the paths to the previous and current frames
    prev_frame_path = path + frames_folder + f"/frame{frame_count:05d}.png"
    curr_frame_path = path + frames_folder + f"/frame{frame_count+skip_image:05d}.png"



    # Load the previous and current frames using OpenCV
    prev_frame = cv2.imread(prev_frame_path)
    curr_frame = cv2.imread(curr_frame_path)
    prev_frame = downsample_image(prev_frame,zoom)
    curr_frame = downsample_image(curr_frame,zoom)
    # Check if either of the frames is missing
    if prev_frame is None or curr_frame is None:
        break
  
    # Estimate optical flow between the frames, considering the previous flow vectors
    flow, magnitude, angle = estimate_optical_flow(prev_frame, curr_frame, prev_flow)

    # Plot the optical flow vectors on the current frame
    if save:
        save_frame_path = save_path + f"/frame{frame_count:05d}.png"
    else:
        save_frame_path = None
    plot_optical_flow_vectors(curr_frame, flow, magnitude, angle,coef = coef, save_path= save_frame_path)
    

    # Update the previous flow vectors for the next iteration
    prev_flow = flow
   
    # Increment the frame count
    frame_count += skip_image