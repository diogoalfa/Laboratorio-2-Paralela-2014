__author__ = 'fcohernan'
# -*- coding: utf-8 -*-

from mpi4py import MPI
import numpy as np
import time
import sys
import os
from PIL import Image,ImageChops
from os import system
import StringIO

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

def rotar90(img):
    arrImg = convertirImgMatrixRGB(img)
    n = img.size[0]
    m = img.size[1]
    final = np.array(Image.new("RGB",(m,n)))
    for i in range(n): #fila
        for j in range(m): #columna
            final[i][j] = arrImg[::, ((i*-1)-1)][j]
    imgColor = Image.fromarray(final)
    return imgColor

def rotar180(img):
    return rotar90(rotar90(img)) #debido a que el algoritmo de cambio de posicion es el mismo

def rotar270(img):
    return rotar180(rotar90(img))

if __name__ == '__main__':
    starting_point=time.time()
    ruta1=str(sys.argv[1])

    im1=Image.open(ruta1)
    base=Image.open("negro.jpg")

    rgb = np.array(im1.convert("RGB"))
    alto = rgb.shape[0]
    ancho = rgb.shape[1]

    if alto > ancho:
        diferencia= (alto - ancho)/2
        base = base.resize((diferencia, alto), Image.ANTIALIAS)
        nuevo = np.hstack((im1, base))
        nuevo = np.hstack((base, nuevo))
    else:
        if ancho > alto:
            diferencia = (ancho - alto)/2
            base = base.resize((ancho, diferencia), Image.ANTIALIAS)
            nuevo = np.vstack((im1, base))
            nuevo = np.vstack((base, nuevo))
        else:
            diferencia = 0
            nuevo = im1
    if diferencia != 0:

        print(ancho,alto)

    base.save("negro.jpg")
    nuevo=Image.fromarray(nuevo)
    nuevo.save("nuevo.jpg")
    nuevo.save("Gif/00.jpg")
    nuevo.save("Gif/01.jpg")
    nuevo.save("Gif/02.jpg")
    nuevo.save("Gif/03.jpg")

    ## LISTO IMAGEN CUADRADA


    imgTrans = rotar90(nuevo)
    imgTrans.save("Gif/04.jpg")
    imgTrans.save("Gif/05.jpg")
    imgTrans.save("Gif/06.jpg")
    imgTrans.save("Gif/07.jpg")
    imgTrans = rotar180(nuevo)
    imgTrans.save("Gif/08.jpg")
    imgTrans.save("Gif/09.jpg")
    imgTrans.save("Gif/10.jpg")
    imgTrans.save("Gif/11.jpg")
    imgTrans = rotar270(nuevo)
    imgTrans.save("Gif/12.jpg")
    imgTrans.save("Gif/13.jpg")
    imgTrans.save("Gif/14.jpg")
    imgTrans.save("Gif/15.jpg")

    nombreSalida = "gifMaster.gif"
    delay = 4
    fileAgrandar = "Gif/*jpg"
    system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))




    print ruta1

    elapsed_time=time.time()-starting_point
    print ""
    print "Tiempo [seconds]: " + str(elapsed_time)


