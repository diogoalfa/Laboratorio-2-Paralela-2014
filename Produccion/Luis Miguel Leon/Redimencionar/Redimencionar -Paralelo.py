# -*- coding: cp1252 -*-
__author__ = 'Luis Miguel leon'

from mpi4py import MPI
import numpy as np
from PIL import Image
import time

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

def redimencionarImg(img,img2):
    ancho=img.size[0]
    alto=img.size[1]
    finalAncho=img2.size[0]
    finAlto= img2.size[1]
    distanX = (ancho-1)/float(finalAncho)
    distanY = (alto-1) /float(finAlto)
    arrImg=convertirImgMatrixRGB(img)
    arrImg2=convertirImgMatrixRGB(img2)
    print "*********************"
    print "*********************"
    print distanX
    print distanY

    tamanoParte = largo/(size)
    inicio = (finAlto/size)*rank; #defino la fila de inicio que procesar� el nodo
    fin = (finAlto/size)*(rank+1); #defino el fin del ciclo que recorre las filas de la matriz
#   Proceso de redimensionado
    for i in range(fin-1,inicio ):
        for j in range(finalAncho-1 ):
            #Variables x y dependiendo de resolucion de salida.

            x = (distanX * j);
            y = (distanY * i);
            #Tomo pixeles adyacentes, dependiendo de la resolucion que debo entregar.
            a = arrImg[y] [x]
            b = arrImg[y+1][x]
            c = arrImg[y][x+1]
            d = arrImg[y+1][x+1]
            #Direfencia entre distancia y el pixel que esta.
            diferX = (distanX * j) - x;
            diferY = (distanY * i) - y;
            # color azul
            blue =  ((a[2])&0xff)*(1-diferX)*(1-diferY) + ((b[2])&0xff)*(diferX)*(1-diferY) + ((c[2])&0xff)*(diferY)*(1-diferX) + ((d[2])&0xff)*(diferX*diferY)
            # color verde
            green = ((a[1])&0xff)*(1-diferX)*(1-diferY) + ((b[1])&0xff)*(diferX)*(1-diferY) + ((c[1])&0xff)*(diferY)*(1-diferX) + ((d[1])&0xff)*(diferX*diferY)
            # color rojo
            red =   ((a[0])&0xff)*(1-diferX)*(1-diferY) + ((b[0])&0xff)*(diferX)*(1-diferY) + ((c[0])&0xff)*(diferY)*(1-diferX) + ((d[0])&0xff)*(diferX*diferY)
            nuevoPixel = arrImg2[i][j]
            nuevoPixel[0]=red 
            nuevoPixel[1]=green 
            nuevoPixel[2]=blue 

            arrImg2[i][j] = nuevoPixel;
    if rank == 0:
        imgRedimencionada=Image.fromarray(arrImg2)
        return imgRedimencionada

def main():
    if rank == 0:
        starting_point=time.time()
    imag = Image.open("base.png")
    #Tamaño de imagen tiene que estar en la misma escala que la original.
    imag = imag.resize((500, 540), Image.ANTIALIAS)#para crear una imagen en blanco con la cual obtengo el tamaño de la final de la imagen redimencionada.
    imag.save("output1.jpg")

    img=Image.open("tatuajr.jpg")
    img2=Image.open("output1.jpg")
    
    imgRedimencionada=redimencionarImg(img,img2)
    if rank == 0:
        imgRedimencionada.save("salidaFinal2.jpg")
        #saludo = raw_input("Escribe lo que sea")
        #print saludo
        elapsed_time=time.time()-starting_point
        print ""
        print "Serial Time [seconds]: " + str(elapsed_time)
main()







