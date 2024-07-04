# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:50:35 2022

@author: deTRAZEGNIES
"""

from __future__ import print_function
from __future__ import divisionq
import cv2 
import numpy as np



# Endroit de la sauvegarde
chemin = 'C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/WIN_20220704_141115.MP4'

#Taille des pixels
imgSize = (640,480)
#imgSize = (768,480)
frame_per_second = 100
#imgSize = (720,480)
#frame_per_second = 24
#writer = cv2.VideoWriter(chemin, cv2.VideoWriter_fourcc(*'MJPG'), frame_per_second,imgSize)




cap = cv2.VideoCapture('C:\\FFmpegTool\\bin\\videoN.avi')

while(cap.isOpened()):
#while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()  
    if ret == True:

        # BGR to GrayScale
        #  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Create a mask
        h, w = frame.shape[:2]
        mask = np.zeros((h, w),np.uint8)
        
        framenew = frame-frame[0] 
        
       
            
        
        #Display/Save the resulting frame
        #writer.write(frame)
        cv2.imshow('Treated Video',framenew)
        
        
        
        if cv2.waitKey(100) & 0xFF == ord('q'):  # press q to quit
            break
    else:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()