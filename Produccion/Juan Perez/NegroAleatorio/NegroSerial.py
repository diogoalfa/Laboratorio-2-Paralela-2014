__author__ = 'juank'

import numpy as np
from PIL import Image
from PIL import ImageEnhance
import time
import random as rnd
from os import system
import math

oscurecimiento = 0

# convierte una imagen tipo Imagen (de la libreria PIL) en una matriz(ETD) con la informacion RGB de la imagen
def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))
# convierte una imagen tipo Imagen (de la libreria PIL) a imagen en Negativo
# procedimiento : multiplica por base 255 cada casilla de la matriz RGB para convertir la imagen en negativo

def oscurecer(imagen,rango):
    matrix = convertirImgMatrixRGB(imagen)
    ran = (int)(math.sqrt((imagen.size[0]*imagen.size[1])/rango))
    ini = rnd.randint(0,imagen.size[1]-ran)
    fin= rnd.randint(0,imagen.size[0]-ran)
    for i in range(ini,ini+ran):
        for j in range(fin,fin+ran):
            a = matrix[i][j]
            if(a.any() != 0):
                matrix[i][j] = 0
    imagenFade = Image.fromarray(matrix)
    return imagenFade

#---------------------------------------------------------------------------------------
#-----------ciclo encargado de iterar la imagen para que se trabaje --------------------
#-----------se generaran multiples copias-----------------------------------------------
#---------------------------------------------------------------------------------------
def cicloOscurecer(imagen, rango):
    resultadoOscuro = oscurecer(imagen,rango)
    resultadoOscuro.save('CopiasCache/resultadoCache'+str(0)+'.jpg')
    #img = Image.open('CopiasCache/resultadoCache00'+str(0)+'.jpg')
    for i in range(rango):
        img = Image.open('CopiasCache/resultadoCache'+str(i)+'.jpg')
        resultadoOscuro = oscurecer(img,rango)
        resultadoOscuro.save('CopiasCache/resultadoCache'+str(i+1)+'.jpg')
        #-----guarda la imagen obtenida----
        '''if i<9:
            resultadoOscuro = oscurecer(img)
            resultadoOscuro.save('CopiasCache/resultadoCache'+str(i+1)+'.jpg')
            else:
            if i<99:
                resultadoOscuro = oscurecer(img)
                resultadoOscuro.save('CopiasCache/resultadoCache'+str(i+1)+'.jpg')
            else:
                resultadoOscuro = oscurecer(img)
                resultadoOscuro.save('CopiasCache/resultadoCache'+str(i+1)+'.jpg')'''

def main():
    starting_point=time.time()
    """las siguientes dos lineas corresponden al nombre del archivo y la extension con el fin de
    nombrar el archivo de salida como <nombreArchivo>Noche.<extension>
    ejemplo: paisaje.jpg -> paisajeNoche.jpg"""
    nombreImg = "2,1"
    extension = ".jpg"
    img=Image.open(nombreImg + extension)

    rango = 100

    cicloOscurecer(img,rango)
    nombreSalida="Fade.gif"
    delay=20

    filepath="CopiasCache/resultadoCache%d.jpg[0-"+rango+"]"
    system('convert -delay %d -loop 0 %s %s ' % (delay,filepath,nombreSalida))
    elapsed_time=time.time()-starting_point
    print ""
    print "Serial Time [seconds]: " + str(elapsed_time)

main()