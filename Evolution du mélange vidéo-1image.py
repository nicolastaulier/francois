# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:30:34 2023

@author: deTRAZEGNIES
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import os
import scipy
import skimage.morphology as morpho


def extract_info(frame,r,g,b,bl_corner=None,ur_corner=None,max_thresh=255,min_thresh=0):
    """
    Parameters:
    frame -> np.array RGB format
    r -> weight for red canal
    g -> weight for green canal
    b -> weight for blue canal
    bl_corner, ur_corner -> bottom-left and upper-right corner of the cropped frame

    Output:
    img -> np.array 2D from 0 to 255, intensity function
    """
    img_crop=frame.copy()
    if bl_corner!=None and ur_corner != None:
        img_crop=img_crop[bl_corner[0]:ur_corner[0],bl_corner[1]:ur_corner[1]]
    img=(r*img_crop[:,:,0]+g*img_crop[:,:,1]+b*img_crop[:,:,2])/(r+b+g)
    img = np.logical_and(img<=max_thresh, img>=min_thresh) * img
    return img


def evaluate_mix(img,max_thresh=255,min_thresh=0):
    """
    Parameters:
    img : image in a NxMx3 numpy array, RGB format
    max_thresh :
    min_thresh :

    Return :
    """

    #thresholding
    #img = np.logical_and(img<=max_thresh, img>=min_thresh) * img

    #percentage of green pixels
    N = img.shape[0] * img.shape[1]
    E = np.count_nonzero(img[:,:])/N * 100
    histogramme, niv_green = np.histogram(img[:,:], bins=255, range=(0.01,1))

    """
    fivep_max_thresh =0
    fivep = N/20
    x=0
    i=255
    while x<fivep:
        i-=1
        x+=histogramme[i]
    fivep_max_thresh = niv_green[i]
    for k in range(img.shape[0]):
        for l in range (img.shape[1]):
            if img[k,l,1]>fivep_max_thresh:
                img[k,l,0]=1
    #plt.imsave("front.png",img)
    print("ratio = ", E, "5% max threshold = ", fivep_max_thresh, "x = ",x)

    return E, fivep_max_thresh, x"""
    return E


def evaluate_propagation(img):
    """
    Parameters:
    img -> image in gray format
    
    Output:
    """
    Gx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    Gy=Gx.copy().T
    grad_x=scipy.signal.convolve(img,Gx)
    grad_y=scipy.signal.convolve(img,Gy)
    grad_norm=np.sqrt(np.power(grad_x,2)+np.power(grad_y,2))
    grad_dir=np.arctan2(grad_y,grad_x)
    return grad_norm,grad_dir


def evolution_mix(file,gap1,gap2):
    """
    Parameters:
    file -> path to a video file
    gap -> positive integer, number of frames between two analysis

    Output:
    """
    #Verification of the paths to the input file
    assert os.path.exists(file)
    #opening the capture
    cap = cv2.VideoCapture()
    cap.open(file)
    if (cap.isOpened()== False):
        print("Error opening video stream or file")

    iter=0
    ratio=[]
    ret, frame0 = cap.read()
    while cap.isOpened():
        iter+=1
        ret, frame = cap.read()
        if ret != True:
            break
        frame = cv2.subtract(frame, frame0)
        if iter%gap1==0:
            img_init=extract_info(frame,58/255,1,0,[300,656],[750,1500],255,0)
            #img=scipy.ndimage.gaussian_filter(img,1)
            #img=filter(img_init)
            img=img_init
            ratio.append(evaluate_mix(img))
        if iter%gap2==0:
            print("Compute gradient frame ",iter)
            img=filter(img_init)
            gn,gd=evaluate_propagation(img)
            plt.imsave("gradient_norm_"+str(iter)+".png",gn,cmap="gray")
            plt.imsave("filtre_"+str(iter)+".png",img,cmap="gray")
            plt.imsave("gradient_dir_"+str(iter)+".png",gd)
            plt.imsave("image_init_"+str(iter)+".png",img_init,cmap="gray")

    print("Finished")
    return ratio


def filter(img,N=7):
    """
    Alternate sequential filter with reconstruction

    Parameters:
    img -> image np.array 2D
    N -> size of biggest structuring element

    Output:
    img_f -> filtered image
    """
    for k in range(N):
        se=morpho.disk(k)
        op=morpho.opening(img,se)
        reco1=morpho.reconstruction(op,img,'dilation')
        clo=morpho.closing(reco1,se)
        img_f=morpho.reconstruction(clo,reco1,'erosion')
    return img_f


img=np.array(image.imread("C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/image-1.png"))
Y=evolution_mix("C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/WIN_20221209_115745.avi",50,200)
X=[i for i in range(len(Y))]
plt.plot(X,Y)
plt.show()