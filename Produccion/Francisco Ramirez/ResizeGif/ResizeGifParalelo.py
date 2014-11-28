__author__ = 'FcoHernan'


import Image
import numpy as np
from os import system
import os
import time
from mpi4py import MPI

def numero(num,cant):
    while len(num)!=len(cant):
        # print "entra"
        num="0"+num
    # print num
    return num

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores
rank = comm.rank     # id procesador actual
size = comm.size     # cantidad de procesadores a usar

starting_point=time.time()
# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
name = "6MP"
ext = ".jpeg"
im1 = Image.open(name+ext)
imReducir = im1
imAgrandar = im1
rgb = np.array(im1.convert("RGB"))
alto = rgb.shape[0]
ancho = rgb.shape[1]
cantidad = str(size)

if rank == 0:
    resize = float(100/size)
    #print resize
    n = resize

    for i in range(0, size):
        # print i
        # print "mandar a "+str(i)+" el n :"+str(n)
        comm.send(n, dest=size-i-1)
        n = n + resize

if rank != size-1:
    factor = comm.recv(source = 0)
    alto = int(alto * factor/100)
    ancho = int(ancho * factor/100)
    imReducir = imReducir.resize((ancho, alto), Image.ANTIALIAS)
    # imReducir.save("gif/"+str(rank)+".jpeg")
    n=numero(str(rank),str(size*2))

    imReducir.save("gifp/"+n+".jpeg")
    imReducir.save("gifp/"+str(9998-int(n))+".jpeg")
    if rank != 0:
        op = 0
        comm.send(op, dest=0)
if rank == 0:
    n=numero(str(0), str(size*2))
    for i in range (1, size-1):
        op=comm.recv(source=i)
    nombreSalida = "gifMasterP.gif"
    delay = 5
    fileAgrandar = "gifp/*jpeg"
    system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))

    elapsed_time=time.time()-starting_point
    print ""
    print "Total Time [seconds]: " + str(elapsed_time)

