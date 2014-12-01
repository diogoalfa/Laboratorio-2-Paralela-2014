__author__ = 'chris'

from PIL import Image
import numpy as np
from PIL import ImageEnhance
from os import system
import time

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

#aplicar reflejo
def aplicarReflejo(img): #arreglo):
    #img = Image.fromarray(arreglo)
    arrImg=convertirImgMatrixRGB(img)
    arrSize=arrImg.shape
    largo=arrSize[1]
    ancho=arrSize[0]
    arrFinal = np.array(Image.new("RGB",(largo,ancho)))
    i=ancho-1
    j=0
    u=0
    v=0
    while i>=0:
        while j<largo:
            aux=arrImg[i][j]
            arrFinal[u][v]=aux
            j+=1
            v+=1
        i-=1
        j=0
        u+=1
        v=0
    #imgFinal =np.vstack((arrImg,arrFinal))
    imgFinal= arrFinal
    imgReflejo = Image.fromarray(imgFinal)
    return imgReflejo
    #return imgFinal

def toGif(fp,delay,output):
  #el delay representa la pausa entre una imagen y otra y loop 0 especifica que el gif se repite en un bucle. *jpg tomara todos los archivos *jpg (para este caso, puede ser cualquier formato de imagen)
  system('convert -delay %d -loop 0 %s %s ' % (delay,fp,output))



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

def generarImagenArriba(img,cantImagenes):
    arrImg=convertirImgMatrixRGB(img)
    fila = img.size[1]
    columna = img.size[0]
    nueva = Image.new("RGB",(fila,columna))# generamos una imagen nueva como base
    arrNuevo = convertirImgMatrixRGB(nueva)
    k =0
    z =0
    for i in range(cantImagenes,fila):
        z=0
        for j in range(0,columna):
            arrNuevo[z][k] = arrImg[i][j]
            z=z+1
        k=k+1
    imagen = Image.fromarray(arrNuevo)
    imagenRotada = rotar270(imagen)
    return imagenRotada


def generarImagen(img,cantImagenes): #para la imagen original se va moviendo hacia abajo
    arrImg=convertirImgMatrixRGB(img)
    largo = img.size[1]
    ancho = img.size[0]
    nueva = Image.new("RGB",(largo,ancho))# generamos una imagen nueva como base
    arrNuevo = convertirImgMatrixRGB(nueva)
    k = 0
    z = 0
    for i in range(0,ancho):
        z=0
        for j in range (cantImagenes,largo):#para generar imagen partiendo desde mas abajo en la matriz
            #print j #para comprobar que esta partiendo desde otro valor
            arrNuevo[i][j] = arrImg[z][k]
            z = z+1
        k = k+1
    imagen = Image.fromarray(arrNuevo) #retorna la imagen girada no se porque por lo tanto debo rotarla
    imagenRotada = rotar270(imagen)
    return imagenRotada

def main():
    img=Image.open("imagenes/1.jpg")
    imgReflejo = aplicarReflejo(img) #se tiene la imagen con el reflejo aplicado
    imgReflejo.save("reflejo.png") #Se guarda la imagen reflejada

    #una vez que ya tenemos la imagen reflejada vamos a generar imagenes corridas para luego hacer el efecto de movimiento al juntarlas
    largoTotal = img.size[1]
    anchoTotal = img.size[0]

    #trabajaremos con 20 imagenes para hacer el gif

    cantImagenes = int(largoTotal/30)
    separar = cantImagenes
    #para la imagen original

    for index in range(0,31):
        cantImagenes = cantImagenes + separar
        imagenCorrida = generarImagen(img,cantImagenes)
        numero = str(index)
        imagenCorrida.save("imagenes/imagen"+numero+".png") #Se va corriendo la imagen y se va guardando
        print "generando imagen "+numero


    var =59
    #para la imagen reflejada
    cantImagenes = int(largoTotal/30)
    separar = cantImagenes
    for index in range(0,30):
        cantImagenes = cantImagenes + separar
        imagenCorrida = generarImagenArriba(imgReflejo,cantImagenes)
        numero = str(var)
        imagenCorrida.save("imagenes/imagen"+numero+".png") #Se va corriendo la imagen y se va guardando
        var = var -1
        print "generando imagen "+numero

    nombreSalida="imagenes/animacion.gif"
    delay=10
    filepath="imagenes/*png"
    toGif(filepath,delay,nombreSalida)

starting_point=time.time() #Donde quiere empezar a calcular el tiempo
main()
elapsed_time=time.time()-starting_point #calculo
print "reflejoGif Time [seconds]: " + str(elapsed_time) #segundos
