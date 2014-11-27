__author__ = 'FcoHernan'


import Image
import numpy as np
from os import system
import os
from images2gif import writeGif

# open an image file (.bmp,.jpg,.png,.gif) you have in the working folder
name = "6MP"
ext = ".jpeg"
im1 = Image.open(name+ext)
imReducir = im1
imAgrandar = im1
rgb = np.array(im1.convert("RGB"))
alto = rgb.shape[0]
ancho = rgb.shape[1]
print ancho, alto

base = Image.open("output.jpg")
base = base.resize((ancho, alto), Image.ANTIALIAS)
base.save("gitReducir/"+"999"+".jpeg")
base.save("gitReducir/"+"000"+".jpeg")
base.save("gitAgrandar/"+"999"+".jpeg")
base.save("gitAgrandar/"+"000"+".jpeg")


i = 001
while ancho > 1 and alto > 1:
    if i <= 9:
        imReducir.save("gitReducir/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imReducir.save("gitReducir/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imReducir.save("gitReducir/"+"0"+str(i)+".jpeg")
            else:
                imReducir.save("gitReducir/"+str(i)+".jpeg")
    i = i + 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imReducir = imReducir.resize((ancho, alto), Image.ANTIALIAS)

alto = rgb.shape[0]
ancho = rgb.shape[1]
print ancho, alto
i = 998
while ancho > 1 and alto > 1:
    if i <= 9:
        imAgrandar.save("gitAgrandar/"+"000"+str(i)+".jpeg")
    else:
        if i <= 99:
            imAgrandar.save("gitAgrandar/"+"00"+str(i)+".jpeg")
        else:
            if i <= 999:
                imAgrandar.save("gitAgrandar/"+"0"+str(i)+".jpeg")
            else:
                imAgrandar.save("gitAgrandar/"+str(i)+".jpeg")
    i = i - 001
    alto = int(alto * 0.9)
    ancho = int(ancho * 0.9)
    imAgrandar = imAgrandar.resize((ancho, alto), Image.ANTIALIAS)

nombreSalida = "git/git01.gif"
delay = 3
fileReducir = "gitReducir/*jpeg"
system('convert -delay %d -loop 0 %s %s ' % (delay,fileReducir,nombreSalida))

nombreSalida = "git/gif02.gif"
delay = 3
fileAgrandar = "gitAgrandar/*jpeg"
system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))

nombreSalida = "git/gifMaster.gif"
delay = 3
fileAgrandar = "git/*gif"
system('convert -delay %d -loop 0 %s %s ' % (delay,fileAgrandar,nombreSalida))


