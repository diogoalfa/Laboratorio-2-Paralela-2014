__author__ = 'FcoHernan'


import Image
import numpy as np
from os import system
import os
import time
import shutil
import sys



starting_point=time.time()
# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
# name = "6MP"
# ext = ".jpeg"
try:
    ruta1=str(sys.argv[1])
except:
    print sys.exit()

im1 = Image.open(ruta1)
imReducir = im1
imAgrandar = im1
rgb = np.array(im1.convert("RGB"))
alto = rgb.shape[0]
ancho = rgb.shape[1]

# COPIAR

try:
    os.mkdir("gif")
except:
    shutil.rmtree("gif")
    os.mkdir("gif")
# FIN COPIAR

im1.save("gif/"+"999"+".jpeg")
im1.save("gif/"+"000"+".jpeg")


i = 001
while ancho > 1 and alto > 1:
    if i <= 9:
        imReducir.save("gif/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imReducir.save("gif/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imReducir.save("gif/"+"0"+str(i)+".jpeg")
            else:
                imReducir.save("gif/"+str(i)+".jpeg")
    i = i + 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imReducir = imReducir.resize((ancho, alto), Image.ANTIALIAS)

alto = rgb.shape[0]
ancho = rgb.shape[1]

i = 998
while ancho > 1 and alto > 1:
    if i <= 9:
        imAgrandar.save("gif/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imAgrandar.save("gif/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imAgrandar.save("gif/"+"0"+str(i)+".jpeg")
            else:
                imAgrandar.save("gif/"+str(i)+".jpeg")
    i = i - 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imAgrandar = imAgrandar.resize((ancho, alto), Image.ANTIALIAS)

nombreSalida = "gifMaster.gif"
delay = 5
fileAgrandar = "gif/*jpeg"
system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))

try:
    # os.remove("nuevo.jpg")
    shutil.rmtree("gif")
    elapsed_time=time.time()-starting_point
    print ""
    print "Tiempo [seconds]: " + str(elapsed_time)
except:
    elapsed_time=time.time()-starting_point
    print ""
    print "Tiempo [seconds]: " + str(elapsed_time)
