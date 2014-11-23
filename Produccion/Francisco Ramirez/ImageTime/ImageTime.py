__author__ = 'cluster'

__author__ = 'francisco'
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 14:31:26 2014

@author: paralela
"""
import numpy as np
from StringIO import StringIO
import time
from mpi4py import MPI
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time

starting_point=time.time()



comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar


def distribuirEnP(size,altura):
    cuoc = (altura) / (size-2) #c : cuociente
    rest = (altura) % (size-2) #r : resto
    conta = 0
    for p in range(size-2):
        if (p+1) != (size-2):
            conta = conta + cuoc
            comm.send(conta, dest = p+2)
        else:
            conta = conta+cuoc+rest
            comm.send(conta, dest = p+2)

def buscarRangoFinal(base,altura):
    if rank==2:
        p=2
        conta=0
        rangos_end=[]
        valor=0
        for i in range(altura):
            for j in range(base):
                if(valor==0):
                    valor=comm.recv(source=p)
                if conta==valor:
                    rangos_end = rangos_end + [i,j]
                    comm.send(rangos_end,dest=p)
                    rangos_end=[]
                    p = p + 1
                    conta = conta + 1
                    valor=0
                else:
                    conta = conta + 1

# convierte una imagen tipo Imagen (de la libreria PIL) en una matriz(ETD) con la informacion RGB de la imagen
def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))



def mezclarRGB(arrImg,r,g,b):
    for i in range(len(arrImg)):
        for j in range(len(arrImg[0])):
            arrImg[i][j][0] = (arrImg[i][j][0]+r)/2
            arrImg[i][j][1] = (arrImg[i][j][1]+g)/2
            arrImg[i][j][2] = (arrImg[i][j][2]+b)/2
    return arrImg


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))


#funcion que recibe la ruta de imagen y distribuye los trozos horizontales a cada procesador excepto el cero
def divisionTareaImagen(ruta):
    img=Image.open(ruta)
    imgSize=img.size
    largo=imgSize[1]
    ancho=imgSize[0]
    tamanoParte=largo/(size-1)  #(size-1) es para no incluir el procesador cero
    xInicio=0
    yInicio=0
    tamPar=tamanoParte
    for i in range(1,size):
        parteImgEnvio=img.crop((xInicio,yInicio,ancho,tamPar))
        tamPar=tamPar+tamanoParte
        yInicio=yInicio+tamanoParte
        #rutaSalida="photoCut"+str(i)+".png"
        #parteImgEnvio.save(rutaSalida)
        arrImg=convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg,dest=i)

def main():
    starting_point=time.time()
    if rank==0:
        ruta="1"
        ext=".jpg"

        openIniTime=time.time()
        img=Image.open(ruta+ext)
        openEndTime=time.time()-openIniTime
        print ""
        print "Image open time: ",openEndTime

        img=np.array(img.convert("RGB"))
        imgContrucFinal=Image.fromarray(img)

        saveIniTime=time.time()
        imgContrucFinal.save(ruta+".png")
        saveEndTime=time.time()-saveIniTime

        saveIniTime=time.time()
        imgContrucFinal.save(ruta+".png")
        saveEndTime=time.time()-saveIniTime
        print ""
        print "Image save time: ",saveEndTime
        print ""

        elapsed_time=time.time()-starting_point
        print ""
        print "Total Time [seconds]: " + str(elapsed_time)



main()
