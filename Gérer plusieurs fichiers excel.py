# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:26:20 2022

@author: deTRAZEGNIES
"""

import os
import csv
import glob

import numpy

###############################################################################
def readFile(filename):
    if filename[-3:] == 'CSV' or filename[-3:] == 'csv':
        with open(filename,'r') as f:
            reader = csv.reader(f,skipinitialspace=True,delimiter=';')
            data = [[x.strip() for x in row] for row in reader]
            N = len(data)
            x = numpy.zeros(N)
            y = numpy.zeros(N)
            for i in range(4,N):
                x[i] = float(data[i][0].replace(',','.'))
                y[i] = float(data[i][1].replace(',','.'))
        f.close()
    return (x,y)
###############################################################################

###############################################################################
def average(directory,resultsFile):
    N = len( [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f[-3:]=='csv'])
    name = []
    mean = numpy.zeros(N)
    std = numpy.zeros(N)
    i = 0
    for path in glob.glob(os.path.join(directory, '*.csv')):
        (directoryName, fileName) = os.path.split(path)
        name[i:] = [fileName]
        print(fileName)
        x,y = readFile(path)
        #mean[i] =round(y.mean(),3)
        Volts=numpy.power(y,2)
        
       # std[i] = round(y.std(),3)
        resultsFile.write(directory + ',' + str(name[i]) + ',' + str(Volts) + '\n')
        i += 1
    resultsFile.write(directory + ',' + 'mean' + ',' + str(round(mean.mean(),3)) + ',' + str(round(mean.std(),3)) + '\n')
    return (directory,name,mean,std)
###############################################################################

pathList = [r'C:/Users/deTRAZEGNIES/Desktop/Projet IHC infrasson/Code pyton spyder/Extrait mesure 19.10.2022'] # Liste des répertoires dans lesquels sont localisés les fichier à traiter.

nameFileResult = 'results.csv' # fichier contenant les résultats avec des point à remplacer par des virgules

resultsFile = open(nameFileResult,'w+')
resultsFile.write('directory,filename,mean,std\n')

for path in pathList:
    average(path,resultsFile)

resultsFile.close()


