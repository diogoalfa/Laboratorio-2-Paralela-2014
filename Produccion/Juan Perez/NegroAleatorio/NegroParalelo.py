# coding=utf-8
__author__ = 'juank'

import numpy as np
from PIL import ImageEnhance
import numpy as np
from StringIO import StringIO
import time
from mpi4py import MPI
from PIL import Image,ImageChops
import StringIO
import numpy as np
from PIL import Image
from PIL import ImageEnhance
import time
import random as rnd
from os import system
import math

starting_point=time.time()

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar

# convierte una imagen tipo Imagen (de la libreria PIL) en una matriz(ETD) con la informacion RGB de la imagen
def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

def oscurecer(arr,rango):

    #ini = rnd.randint(0,imagen.size[1]-1)
    #fin= rnd.randint(0,imagen.size[0]-1)
    hasta = (int)((len(arr[0])*(len(arr[1]))/rango))
    for i in range (hasta):
        ini = rnd.randint(0,len(arr[1])-1)
        fin= rnd.randint(0,len(arr[0])-1)
        arr[ini][fin] = 0
    return arr

def cicloOscurecer(imagen, rango):
    resultadoOscuro = oscurecer(imagen,rango)
    resultadoOscuro.save('CopiasCache/resultadoCache'+str(0)+'.jpg')
    #img = Image.open('CopiasCache/resultadoCache00'+str(0)+'.jpg')
    for i in range(rango):
        img = Image.open('CopiasCache/resultadoCache'+str(i)+'.jpg')
        resultadoOscuro = oscurecer(img,rango)
        resultadoOscuro.save('CopiasCache/resultadoCache'+str(i+1)+'.jpg')
        #-----guarda la imagen obtenida----

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
        rutaSalida="photoCut"+str(i)+".png"
        parteImgEnvio.save(rutaSalida)
        arrImg=convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg,dest=i)

def main():
    starting_point=time.time()

    if rank==0:
        ruta="nelson.gif"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=oscurecer(arrTrabajo)    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida,dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("IMAGENFINAL.png")

    elapsed_time=time.time()-starting_point
    print ""
    print "Tiempo paralelo [s]: " + str(elapsed_time)


main()
