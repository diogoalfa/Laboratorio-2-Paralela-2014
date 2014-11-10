__author__ = 'jose'
from PIL import Image,ImageOps
import time
from mpi4py import MPI
import numpy as np
inicio = time.time()
comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
img = Image.open("12.jpg")

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
#---------------------------------------------
if rank ==0:
    ancho,alto = img.size
    for i in range(2,size):
        if i <size-1:
            imgFraccion = img.crop((0,(i-2)*alto/(size-2),ancho,((i-1)*alto/(size-2))-1))
            comm.send(np.array(imgFraccion.convert("RGB")),dest=i)
        else:
            imgFraccion = img.crop((0,(i-2)*alto/(size-2),ancho,(alto-1)))
            comm.send(np.array(imgFraccion.convert("RGB")),dest=i)
if rank >=2:
    imgWork = Image.fromarray(comm.recv(source=0))
    imgWork = sepia(imgWork)
    comm.send(np.array(imgWork.convert("RGB")),dest=0)
if rank==0:
    if size<3:
        imagen = Image.fromarray(comm.recv(source=2))
    else:
        img1 = comm.recv(source=2)
        for i in range(3,size):
            img2 = comm.recv(source=i)
            img1 = np.vstack((img1,img2))
        imagen = Image.fromarray(img1)
    imagen.save("sepiaParalelo.png")
    final = time.time()-inicio
    print "Parallel time [seconds] = " + str(final)