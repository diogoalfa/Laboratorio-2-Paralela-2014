__author__ = 'jose'

from mpi4py import MPI
import numpy as np
from PIL import Image,ImageChops,ImageOps
import StringIO
import time
inicio = time.time()
comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #

rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #

def make_linear_ramp(white):
     ramp = []
     r, g, b = white
     for i in range(255):
         ramp.extend((r*i/255, g*i/255, b*i/255))
     return ramp
def sepia(im):
    sepia = make_linear_ramp((255, 240, 192))
    if im.mode != "L":
        im = im.convert("L")
    # optional: apply contrast enhancement here, e.g.
    im = ImageOps.autocontrast(im)
    # apply sepia palette
    im.putpalette(sepia)
    return im

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
        rutaSalida="photoCut"+str(i)+".png"
        parteImgEnvio.save(rutaSalida)
        arrImg=convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg,dest=i)

def main():
    if rank==0:
        ruta="12.jpg"
        divisionTareaImagen(ruta)
    if rank!=0:
        arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        arrImgSalida=sepia(Image.fromarray(arrTrabajo))    #enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(convertirImgMatrixRGB(arrImgSalida),dest=0)
    if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
        for i in range(1,size):
            if i > 1:
                construcImg = np.concatenate((construcImg,comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal=Image.fromarray(construcImg)
        imgContrucFinal.save("SepiaImage.png")
        print "Parallel Time : "+str(time.time()-inicio)+" seconds"

main()
