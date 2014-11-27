__author__ = 'Francisca'
# -*- coding: utf-8 -*-

import numpy as np
import time
from PIL import Image
from os import system


#Nivel de transparencia de imagen 1, para que queden igualmete mezcladas se debe usar un alfa=0.5
transp=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
sec=11

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

#mezcla 2 imagenes en una,el alfa es usado para definir el nivel de transparencia de las imagenes.
def sumarImagenes(fpImg1,fpImg2,alfa,alfa2):

    img1=Image.open(fpImg1)
    img2=Image.open(fpImg2).resize(img1.size) #redimensiono la segunda imagen al tamaño del fondo
                                              #el fondo rules!.
    arrImg1=convertirImgMatrixRGB(img1)
    arrImg2=convertirImgMatrixRGB(img2)
    for i in range(img1.size[1]):
        for j in range(img1.size[0]):
            sumaPixel= (arrImg1[i][j]*(alfa))+(arrImg2[i][j]*(alfa2))
            arrImg1[i][j]=sumaPixel
    imgSuma=Image.fromarray(arrImg1)
    return imgSuma

def toGif(fp,delay,output):
    #el delay representa la pausa entre una imagen y otra y loop 0 especifica que el gif se repite en un bucle. *jpg tomara todos los archivos *jpg (para este caso, puede ser cualquier formato de imagen)
    system('convert -delay %d -loop 0 %s %s ' % (delay,fp,output))

def main():
    copy=20
    starting_point=time.time()
    #ahora en vez de pasar la imagen en memoria a la funcion
    #se le pasa el filepath y la funcion se encarga de cargar en memoria.
    for k in range (sec):
        ALFA=transp[k]
        ALFA2=1.0-transp[k]
        imagenSumada=sumarImagenes('barco.jpg','galaxia.jpg',ALFA,ALFA2)
        if(k<10):
            imagenSumada.save('Imagenes2/resultado00'+str(k)+'.jpg')
        if(copy>9):
            imagenSumada.save('Imagenes2/resultado0'+str(copy)+'.jpg')
            copy=copy-1
        if(k>9):
            imagenSumada.save('Imagenes2/resultado0'+str(k)+'.jpg')
        if(copy<10):
            imagenSumada.save('Imagenes2/resultado00'+str(copy)+'.jpg')
            copy=copy-1

    nombreSalida='Imagenes2/sumaAnimacion.gif'
    delay=1
    filepath='Imagenes2/*jpg'
    toGif(filepath,delay,nombreSalida)
    
    elapsed_time=time.time()-starting_point
    print ""
    print "Serial Time [seconds]: " + str(elapsed_time)

main()

