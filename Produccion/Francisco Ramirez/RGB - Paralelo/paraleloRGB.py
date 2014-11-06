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

starting_point=time.time()

#Explicacion paralelo
#Para cada procesador ingresado por el terminal, ya sea "np"=4 o "np"=12 va a funcionar de la misma forma,
#la distribución para que los "np" procesadores, será dividir la cantidad total de datos
#por la cantidad de procesado, dejandolos de forma pareja. En el caso que sobren será asignado para
#el ultimo procesador. A continuación se describiran brevemente que realizarán cada función


comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar

# En esta funcion se mandara a cada procesador la cantidad de datos con la que trabajaran
# Si sobran datos para que sean parejos, se le asignara al ultimo procesador
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

# El procesador 0 recibirá las cantidad de datos con la que trabajará
# cada procesador para devolver los indice i y j hasta donde operará
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

def cortarImagen(data0, x, y, base, r, g, b):
    # im = Image.open('1.jpg')
    region = data0.crop((0, x, base, y))
    # region.save("cut"+str(rank)+".jpg")
    mezclarRGB(region, r, g, b)

def mezclarRGB(img,r,g,b):
    arrImg=convertirImgMatrixRGB(img)
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            arrImg[i][j][0] = (arrImg[i][j][0]+r)/2
            arrImg[i][j][1] = (arrImg[i][j][1]+g)/2
            arrImg[i][j][2] = (arrImg[i][j][2]+b)/2
    imgRGB=Image.fromarray(arrImg)
    imgRGB.save("new"+str(rank)+".jpg")

def unirImagen():
    im1 = Image.open('new'+str(rank)+'.jpg')
    im1 = np.array(im1.convert("RGB"))
    for i in range(3, size):
        im2 = Image.open('new'+str(i)+'.jpg')
        im2 = np.array(im2.convert("RGB"))
        im1=np.vstack((im1, im2))
    im1=Image.fromarray(im1)
    im1.save("end.png")


#-------------MAIN---------------------

# Se sobre entiende que los delimitadores son espacios
if rank != 0 and rank != 1:
    data0 = Image.open("1.jpg")
    data1 = convertirImgMatrixRGB(data0)
    altura = data1.shape[0]
    base = data1.shape[1]
# El procesador 0 estará a cargo de mandar la cantidad de datos
# para cada procesador
if rank == 2:
    print ""
    comm.send(altura, dest=0)
    comm.send(base, dest=1)
    distribuirEnP(size, altura)

if rank == 0:
    print "Altura: ", comm.recv(source=2)

if rank == 1:
    print "Base: ", comm.recv(source=2)

if rank >= 2:
    # Recibe la cantidad de datos en cada procesador
    fin = comm.recv(source=2)
    #fin = fin - 1
    #envia los datos con que finalizan al siguiente procesador para que lo usen como inicio
    if size != 3:
        if rank == 2:
            ini = 0
            i = 1
            if size > 0:
                comm.send(fin, dest=3)
    else:
        ini=0
        comm.send(fin,dest=2)
    # Hasta los p procesadores
    if size != 3:
        if rank !=2:
            ini=comm.recv(source=rank-1)
            if (rank+1)<size:
                comm.send(fin,dest=rank+1)
    else:
        ini=comm.recv(source=2)
    print "rank ",rank,", ini,fin :",ini,",",fin

    #r,g,b componentes del color a mezclar en decimales
    # 255,0,0 rojo
    r=255
    g=0
    b=0

    cortarImagen(data0, ini, fin, base, r, g, b)

if rank==2:
    #intentaremos unir las imagenes, se usa una secuencia try catch porque puede suceder que intentemos
    #unir imagenes que aun no esten listas, para que el programa no se caiga, lo volvemos a intentar
    #hasta que salga bien
    exito=0
    while exito==0:
        try:
            unirImagen()
            exito=1
        except:
            print "imagenes aun no listas, reintentando..."

if rank ==2:
#    Calculo de tiempo
    elapsed_time=time.time()-starting_point
    elapsed_time_int = int(elapsed_time)
    print "Parallel Time [seconds]: " + str(elapsed_time)
    print ""