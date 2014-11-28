__author__ = 'FcoHernan'


import Image
import numpy as np
from os import system
import os
import time
from mpi4py import MPI

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

im1.save("git/"+"999"+".jpeg")
im1.save("git/"+"000"+".jpeg")


i = 000
while ancho > 1 and alto > 1:
    if i <= 9:
        imReducir.save("git/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imReducir.save("git/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imReducir.save("git/"+"0"+str(i)+".jpeg")
            else:
                imReducir.save("git/"+str(i)+".jpeg")
    i = i + 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imReducir = imReducir.resize((ancho, alto), Image.ANTIALIAS)

alto = rgb.shape[0]
ancho = rgb.shape[1]

i = 998
while ancho > 1 and alto > 1:
    if i <= 9:
        imAgrandar.save("git/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imAgrandar.save("git/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imAgrandar.save("git/"+"0"+str(i)+".jpeg")
            else:
                imAgrandar.save("git/"+str(i)+".jpeg")
    i = i - 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imAgrandar = imAgrandar.resize((ancho, alto), Image.ANTIALIAS)

nombreSalida = "gifMaster.gif"
delay = 5
fileAgrandar = "git/*jpeg"
system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))

elapsed_time=time.time()-starting_point
print ""
print "Total Time [seconds]: " + str(elapsed_time)

