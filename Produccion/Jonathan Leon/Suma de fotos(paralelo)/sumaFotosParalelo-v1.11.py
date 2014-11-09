__author__ = 'jonathan'
# -*- coding: utf-8 -*-

from mpi4py import MPI
import numpy as np
import time
import sys
import os
from PIL import Image,ImageChops
import StringIO


comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #

rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

#funcion que recibe la ruta de imagen y distribuye los trozos horizontales a cada procesador excepto el cero
def divisionTareaImagen(ruta1,ruta2):
    img1=Image.open(ruta1)
    img2=Image.open(ruta2).resize(img1.size)
    img1Size=img1.size
    largo1=img1Size[1]
    ancho1=img1Size[0]
    tamanoParte=largo1/(size-1)  #(size-1) es para no incluir el procesador cero
    xInicio=0
    yInicio=0
    tamPar=tamanoParte
    for i in range(1,size):
        parteImgEnvio1=img1.crop((xInicio,yInicio,ancho1,tamPar))
        parteImgEnvio2=img2.crop((xInicio,yInicio,ancho1,tamPar))
        tamPar=tamPar+tamanoParte
        yInicio=yInicio+tamanoParte
        arrImg1=convertirImgMatrixRGB(parteImgEnvio1)
        arrImg2=convertirImgMatrixRGB(parteImgEnvio2)
        tuplaImgs=(arrImg1,arrImg2)
        comm.send(tuplaImgs,dest=i)

def sumarImagenes(arrImg1,arrImg2,alfa):
    img1=Image.fromarray(arrImg1)
    img2=Image.fromarray(arrImg2)
    suma=Image.blend(img1,img2,alfa)
    return convertirImgMatrixRGB(suma)



if __name__ == '__main__':


   if rank==0: #el maestro comprueba que se ingresa la cantidad de paramentros correspondientes para trabajar
       if len(sys.argv)!=4:
           print "\n ERROR: este script recibe exactamente 3 paramentros ,%d dado(s)." % (len(sys.argv)-1)
           print "\n<ruta de archivo> <ruta de otro archivo> <valor canal alfa (entre 0 y 1)> "
           print "\nejemplo : python SumaFotosParalelo-v1.1.py archivo1.jpg archivo2.jpg 0.45"
           print "\n\n Terminando..."
           for i in range(1,size):
                comm.send(False,dest=i)  # si hay un problema con los paramentros envio un valor false a los nodos
                                         # esto los obligara a matar la ejecuccion de los programas en todos los nodos

           sys.exit(2) #tambien terminamos la ejeccion en el maestro

       ruta1=str(sys.argv[1])
       ruta2=str(sys.argv[2])


       if os.path.exists(ruta1)==False:
           print ruta1+" ->No existe archivo o directorio."
           print "\n\n Terminando..."
           for i in range(1,size):
                comm.send(False,dest=i)
           sys.exit(2)

       if os.path.exists(ruta2)==False:
           print ruta2+" ->No existe archivo o directorio."
           print "\n\n Terminando..."
           for i in range(1,size):
                comm.send(False,dest=i)
           sys.exit(2)

       try:
            alfa=float(sys.argv[3])  #ciclo try catch para obtener el valor alfa en formato flotante
       except ValueError:
            print "Valor alfa no reconocido (%s), usando valor por defecto :0.5" % sys.argv[3]
            alfa=0.4                 #si el usuario no ingresa cualquier cosa, tomo el alfa por defecto=.5
       else:
           for i in range(1,size):
                comm.send(True,dest=i) #si todo esta en orden enviamos una señal de True, que significa que los nodos
                                       #                                                          seguiran trabajando

       starting_point=time.time()        #cronometramos tiempo despues de ingresar todos los datos necesarios.

       divisionTareaImagen(ruta1,ruta2)  #dividimos la imagen y la distribuimos en los nodos

       for i in range(1,size):
           comm.send(alfa,dest=i)        #enviamos el valor alfa a los nodos tambien.

   if rank!=0:
        trabajar=comm.recv(source=0)  #variable para controlar si el nodo maestro termino el programa o no.
        if trabajar!=True:
            sys.exit(2)     #si el maestro no nos pasa un True, terminamos la ejecución

        tuplaTrabajo=comm.recv(source=0)     #recibimos la tupla de datos (fragmento de imagenes, valor alfa)
        alfa=comm.recv(source=0)             #recibimos alfa
        arrImgSalida=sumarImagenes(tuplaTrabajo[0],tuplaTrabajo[1],alfa) #sumamos los fragmentos de imagenes
        comm.send(arrImgSalida,dest=0) #enviamos elresultado al maestro
   if rank==0:
        for i in range(1,size):
            if i>1:
                constructImg=np.concatenate((constructImg,comm.recv(source=i))) #el maestro recibe las imagenes y las arma en una
            if i==1:
                constructImg=comm.recv(source=i)
        imgContructFinal=Image.fromarray(constructImg)
        imgContructFinal.save("OUTPUT.png") #archivo de salida.
        elapsed_time=time.time()-starting_point
        print ""
        print "Tiempo Paralelo [seconds]: " + str(elapsed_time)





